import base64
from email.message import EmailMessage
import hmac, hashlib
import numpy as np
import pandas as pd
import random
from smtplib import SMTP_SSL
from sqlalchemy import insert, select, alias, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession
from typing import List

from src.constants import HASH_SECRET
from src.user.constants import *
from src.user.exceptions import *
from src.user.schemas import *
from src.user.models import *


def create_verification_code(email: str, db: DbSession) -> int:
    # 100000 ≤ code ≤ 999999
    code = 100000 + max(0, min(int(random.random() * 900000), 900000))

    obj = db.query(Email).where(Email.email == email).first()
    if obj is None:
        db.add(EmailCode(email=Email(email=email), code=code))
        db.flush()
    elif obj.code is None:
        db.execute(insert(EmailCode).values({"email_id": obj.id, "code": code}))
    else:
        db.execute(update(EmailCode).values(code=code).where(EmailCode.email_id == obj.id))

    return code


def send_code_via_email(email: str, code: int) -> None:
    msg = EmailMessage()
    msg["Subject"] = "SNEK verification code"
    msg["From"] = MAIL_ADDRESS
    msg["To"] = email
    msg.set_content(f"Please enter your code: {code}")

    with SMTP_SSL(MAIL_SERVER, MAIL_PORT) as smtp:
        smtp.login(MAIL_ADDRESS, MAIL_PASSWORD)
        smtp.send_message(msg)


def check_verification_code(req: VerificationRequest, db: DbSession) -> int:
    code = db.query(EmailCode).join(EmailCode.email).filter(Email.email == req.email).first()
    if code is None or code.code != req.code:
        raise InvalidEmailCodeException()

    return code.email_id


def create_verification(email: str, email_id: int, db: DbSession) -> str:
    payload = bytes(email, 'utf-8')
    signature = hmac.new(HASH_SECRET, payload, digestmod=hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(signature).decode('utf-8')

    verification = db.query(EmailVerification).where(EmailVerification.email_id == email_id).first()
    if verification is None:
        db.execute(insert(EmailVerification).values({"token": token, "email_id": email_id}))
    elif verification.user is None:
        db.execute(update(EmailVerification).values(token=token).where(EmailVerification.email_id == email_id))
    else:
        raise EmailVerification(email)

    return token


def check_verification_token(req: CreateUserRequest, db: DbSession) -> int:
    verification = db.query(EmailVerification).join(EmailVerification.email).filter(Email.email == req.email).first()
    if verification is None or verification.token != req.token:
        raise InvalidEmailTokenException()
    
    return verification.id


def create_user(req: CreateUserRequest, verification_id: int, db: DbSession) -> int:
    # Add foreign user's main language to available languages list
    if req.profile.nation_code != KOREA_CODE and req.main_language not in req.languages:
        req.languages.append(req.main_language)

    salt, hash = create_salt_hash(req.password)
    profile_id = create_profile(req.profile, db)
    create_user_item(profile_id, user_food, "food_id", Food, req.profile.foods, InvalidFoodException, db)
    create_user_item(profile_id, user_movie, "movie_id", Movie, req.profile.movies, InvalidMovieException, db)
    create_user_item(profile_id, user_hobby, "hobby_id", Hobby, req.profile.hobbies, InvalidHobbyException, db)
    create_user_item(profile_id, user_location, "location_id", Location, req.profile.locations, InvalidLocationException, db)

    lang_id = db.scalar(select(Language.id).where(Language.name == req.main_language))
    if lang_id is None:
        raise InvalidLanguageException()

    try:
        db.execute(insert(User).values({
                "user_id": profile_id,
                "verification_id": verification_id,
                "lang_id": lang_id,
                "salt": salt,
                "hash": hash,
            }))
    except IntegrityError:
        raise EmailInUseException(req.email)
    
    create_user_item(profile_id, user_lang, "lang_id", Language, req.languages, InvalidLanguageException, db)

    return profile_id


def create_salt_hash(password: str) -> (str, str):
    salt = base64.b64encode(random.randbytes(16)).decode()
    payload = bytes(password + salt, 'utf-8')
    signature = hmac.new(HASH_SECRET, payload, digestmod=hashlib.sha256).digest()
    hash = base64.b64encode(signature).decode()

    return (salt, hash)


def create_profile(profile: ProfileData, db: DbSession) -> int:
    return db.scalar(insert(Profile).values({
            "name": profile.name,
            "birth": profile.birth,
            "sex": profile.sex,
            "major": profile.major,
            "admission_year": profile.admission_year,
            "about_me": profile.about_me,
            "mbti": profile.mbti,
            "nation_code": profile.nation_code,
        }).returning(Profile.id))


def create_user_item(profile_id: int, table: Table, column: str, model: type[Base], items: List[str], exception: type[HTTPException], db: DbSession):
    if len(items) == 0:
        return
    try:
        db.execute(insert(table).values([{
            "user_id": profile_id,
            column: select(model.id).where(model.name == item)
        }for item in items]))
    except IntegrityError:
        raise exception()


def get_target_users(user: User, db: DbSession) -> List[User]:
    filter = (Profile.nation_code != KOREA_CODE) if user.profile.nation_code == KOREA_CODE else (Profile.nation_code == KOREA_CODE)
    me = alias(user_lang, 'M')
    you = alias(user_lang, 'Y')
    return list(db.query(User).join(User.profile).where(filter).where(
        User.user_id.in_(
            select(you.c.user_id).join(me, you.c.lang_id == me.c.lang_id).where(me.c.user_id == user.user_id))))


def sort_target_users(user: User, targets: List[User]) -> List[User]:
    if len(targets) == 0:
        return targets

    user_dict = {}
    for target in targets:
        user_dict[target.user_id] = target

    targets_sorted = []

    df_me = get_user_dataframe(user)
    df_targets = pd.DataFrame()
    for target in targets:
        df_target = get_user_dataframe(target)
        df_target["count"] = count_intersection(df_me, df_target)
        df_targets = pd.concat([df_targets, df_target])

    user_ids = df_targets.sort_values(by=["count"], ascending=False).loc[:, "id"]

    for user_id in user_ids:
        targets_sorted.append(user_dict[user_id])
    return targets_sorted


def get_user_dataframe(user: User) -> pd.DataFrame:
    my_dict = {
        "id": user.user_id,
        "foods": list([food for food in user.profile.foods]),
        "movies": list([movie for movie in user.profile.movies]),
        "hobbies": list([hobby for hobby in user.profile.hobbies]),
        "locations": list([location for location in user.profile.locations])
    }
    return pd.DataFrame.from_dict(my_dict, orient="index").T


def count_intersection(df_me: pd.DataFrame, df_target: pd.DataFrame) -> int:
    cnt = 0
    features = ["foods", "movies", "hobbies", "locations"]

    for feature in features:
        my_list = np.array(df_me.loc[:, feature].to_list()).flatten()
        target_list = np.array(df_target.loc[:, feature].to_list()).flatten()
        cnt += len(set(my_list) & set(target_list))

    return cnt