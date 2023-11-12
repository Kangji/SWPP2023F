from datetime import timedelta
import unittest
from unittest.mock import patch, Mock

from sqlalchemy import insert, delete

from src.database import Base, DbConnector
from src.chatting.dependencies import *
from src.chatting.models import *
from src.chatting.service import *
from tests.utils import *


class TestDependencies(unittest.TestCase):
    email = "test@snu.ac.kr"
    invalid = "hello@snu.ac.kr"

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=DbConnector.engine)
        for db in DbConnector.get_db():
            cls.profile_id = setup_user(db, cls.email)
            db.commit()

    @classmethod
    @inject_db
    def tearDownClass(cls, db: DbSession) -> None:
        teardown_user(db)
        db.commit()

    @inject_db
    def test_get_user_id(self, db: DbSession) -> None:
        valid_req = CreateChattingRequest(counterpart=self.email)
        invalid_req = CreateChattingRequest(counterpart=self.invalid)

        self.assertEqual(self.profile_id, get_user_id(valid_req, db))
        with self.assertRaises(InvalidUserException):
            get_user_id(invalid_req, db)


class TestService(unittest.TestCase):
    initiator = "test@snu.ac.kr"
    responder = "hello@snu.ac.kr"

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=DbConnector.engine)
        for db in DbConnector.get_db():
            cls.initiator_id = setup_user(db, cls.initiator)
            cls.responder_id = setup_user(db, cls.responder)
            db.commit()

    @classmethod
    @inject_db
    def tearDownClass(cls, db: DbSession) -> None:
        teardown_user(db)
        db.commit()

    @inject_db
    def tearDown(self, db: DbSession) -> None:
        db.execute(delete(Topic))
        db.execute(delete(Intimacy))
        db.execute(delete(Text))
        db.execute(delete(Chatting))
        db.commit()

    @inject_db
    def test_chatting(self, db: DbSession):
        chatting = create_chatting(self.initiator_id, self.responder_id, db)
        chatting_id = chatting.id
        self.assertIsNotNone(chatting)
        self.assertEqual(chatting.is_approved, False)
        self.assertEqual(chatting.is_terminated, False)
        db.commit()

        self.assertEqual(get_all_chattings(self.initiator_id, True, db), [])
        self.assertEqual(len(get_all_chattings(
            self.initiator_id, False, db)), 1)
        self.assertEqual(len(get_all_chattings(
            self.responder_id, False, db)), 1)

        with self.assertRaises(ChattingNotExistException):
            approve_chatting(self.initiator_id, chatting_id, db)
        with self.assertRaises(ChattingNotExistException):
            approve_chatting(self.responder_id, -1, db)
        chatting = approve_chatting(self.responder_id, chatting_id, db)
        db.commit()

        self.assertEqual(chatting.id, chatting_id)
        self.assertEqual(
            len(get_all_chattings(self.initiator_id, True, db)), 1)
        self.assertEqual(len(get_all_chattings(
            self.initiator_id, False, db)), 0)

        intimacy = get_all_intimacies(self.initiator_id, None, None, None, db)
        self.assertEqual(len(intimacy), 1)
        intimacy = get_all_intimacies(self.responder_id, None, None, None, db)
        self.assertEqual(len(intimacy), 1)

        with self.assertRaises(ChattingNotExistException):
            terminate_chatting(-1, chatting_id, db)
        with self.assertRaises(ChattingNotExistException):
            terminate_chatting(self.initiator_id, -1, db)
        chatting = terminate_chatting(self.initiator_id, chatting_id, db)
        self.assertEqual(chatting.is_terminated, True)
        chatting = terminate_chatting(self.responder_id, chatting_id, db)
        db.commit()

    @inject_db
    def test_get_all_texts(self, db: DbSession):
        timestamp = datetime.now()

        chatting = create_chatting(self.initiator_id, self.responder_id, db)
        seq_ids = list(
            db.scalars(
                insert(Text)
                .values(list(
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.initiator_id,
                        "msg": "hello",
                        "timestamp": timestamp + timedelta(milliseconds=i),
                    } for i in range(5)
                ))
                .returning(Text.id)
            )
        )
        db.commit()

        self.assertEqual(
            get_all_texts(-1, chatting.id, -1, None, None, db), [])
        self.assertEqual(get_all_texts(-1, None, -1, None, None, db), [])
        self.assertEqual(get_all_texts(
            self.initiator_id, -1, -1, None, None, db), [])
        self.assertEqual(
            len(get_all_texts(self.initiator_id, chatting.id, -1, None, None, db)), 5
        )
        self.assertEqual(
            len(get_all_texts(self.initiator_id, None, -1, None, None, db)), 5
        )
        self.assertEqual(
            len(get_all_texts(self.initiator_id,
                None, seq_ids[1], None, None, db)), 3
        )

        texts = get_all_texts(self.initiator_id, None, seq_ids[1], 2, None, db)
        self.assertEqual(len(texts), 2)
        self.assertEqual(texts[0].id, seq_ids[4])
        self.assertEqual(texts[1].id, seq_ids[3])

        texts = get_all_texts(
            self.initiator_id, None, seq_ids[1], None, timestamp + timedelta(milliseconds=3), db)
        self.assertEqual(len(texts), 2)
        self.assertEqual(texts[0].id, seq_ids[3])
        self.assertEqual(texts[1].id, seq_ids[2])

    @inject_db
    def test_get_all_intimacies(self, db: DbSession):
        chatting = create_chatting(self.initiator_id, self.responder_id, db)
        timestamp = datetime.now()
        db.execute(
            insert(Intimacy)
            .values(list({
                "user_id": self.initiator_id,
                "chatting_id": chatting.id,
                "intimacy": i,
                "timestamp": timestamp + timedelta(seconds=i)
            } for i in range(5)))
        )

        intimacies = get_all_intimacies(self.responder_id, None, None, None, db)
        self.assertEqual(len(intimacies), 0)
        
        intimacies = get_all_intimacies(self.initiator_id, None, None, None, db)
        self.assertEqual(len(intimacies), 5)
        self.assertEqual(intimacies[1].intimacy, 3)
        self.assertEqual(intimacies[3].intimacy, 1)
        self.assertEqual(intimacies[4].intimacy, 0)

        intimacies = get_all_intimacies(self.initiator_id, -1, None, None, db)
        self.assertEqual(len(intimacies), 0)

        intimacies = get_all_intimacies(self.initiator_id, None, 3, None, db)
        self.assertEqual(len(intimacies), 3)
        
        intimacies = get_all_intimacies(self.initiator_id, None, None, timestamp + timedelta(seconds=2.5), db)
        self.assertEqual(len(intimacies), 3)

    @patch("src.chatting.service.requests.post")  # patch for clova
    @inject_db
    def test_create_intimacy(self, mock_post, db: DbSession):
        papago_mock_response = Mock()
        clova_mock_response = Mock()
        papago_mock_response.status_code = 200
        clova_mock_response.status_code = 200
        clova_mock_response.text = json.dumps({'document': {'sentiment': 'positive', 'confidence': {'negative': 0.030769918, 'positive': 99.964096, 'neutral': 0.00513428}}, 'sentences': [
                                              {'content': 'translated text', 'offset': 0, 'length': 11, 'sentiment': 'positive', 'confidence': {'negative': 0.0018461951, 'positive': 0.99784577, 'neutral': 0.0003080568}, 'highlights': [{'offset': 0, 'length': 10}]}]})
        papago_mock_response.json.return_value = {'message': {'result': {
            'srcLangType': 'en', 'tarLangType': 'ko', 'translatedText': 'translated text'}}}
        mock_post.side_effect = [papago_mock_response, clova_mock_response]

        chatting = create_chatting(self.initiator_id, self.responder_id, db)
        chatting = approve_chatting(self.responder_id, chatting.id, db)

        timestamp = datetime.now()
        db.scalars(
            insert(Text)
            .values(
                [
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.initiator_id,
                        "msg": "hello",
                        "timestamp": timestamp,
                    },
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.initiator_id,
                        "msg": "hello",
                        "timestamp": timestamp - timedelta(seconds=1),
                    },
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.responder_id,
                        "msg": "you",
                        "timestamp": timestamp - timedelta(seconds=2),
                    },
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.initiator_id,
                        "msg": "what",
                        "timestamp": timestamp - timedelta(seconds=3),
                    },
                    {
                        "chatting_id": chatting.id,
                        "sender_id": self.responder_id,
                        "msg": "bye",
                        "timestamp": timestamp - timedelta(seconds=4),
                    },
                ]
            )
            .returning(Text.id)
        )
        db.commit()

        intimacy = create_intimacy(self.initiator_id, chatting.id, db)
        self.assertEqual(intimacy.intimacy, 41.99933326082)

    @inject_db
    def test_get_topic(self, db: DbSession):
        db.execute(
            insert(Topic).values(
                [
                    {"topic": "I'm so good", "tag": "A"},
                    {"topic": "I'm so mad", "tag": "B"},
                    {"topic": "I'm so sad", "tag": "C"},
                    {"topic": "I'm so happy", "tag": "C"}
                ]
            )
        )
        db.commit()
        self.assertIn(get_topic('C', db).topic, ["I'm so sad", "I'm so happy"])
        self.assertEqual(get_topic('B', db).topic, "I'm so mad")
        self.assertEqual(get_topic('A', db).topic, "I'm so good")

    def test_flatten_texts(self):
        texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        expected_result = "Hello"
        result = flatten_texts(texts)
        self.assertEqual(result, expected_result)

    @unittest.skip("This test actually calls external API")
    def test_call_clova_api(self):
        with self.assertRaises(ExternalApiError):
            call_clova_api("")
        response = call_clova_api("I am Happy!")
        self.assertEqual(response.status_code, 200)

    @unittest.skip("This test actually calls external API")
    def test_call_papago_api(self):
        with self.assertRaises(ExternalApiError):
            call_papago_api("")
        response = call_papago_api("I am Happy!")
        self.assertEqual(response.status_code, 200)

    @patch("src.chatting.service.requests.post")
    def test_translate_text(self, mock_papago):
        mock_response = Mock()
        mock_response.status_code = 200
        data = {
            'message': {'result':
                        {'srcLangType': 'en', 'tarLangType': 'ko',
                            'translatedText': '나는 행복해!'}
                        }
        }

        mock_response.json.return_value = data
        mock_papago.return_value = mock_response

        response = translate_text("I'm so sad..")
        self.assertEqual(response, "나는 행복해!")

    @patch("src.chatting.service.requests.post")
    def test_get_sentiment(self, mock_clova):
        mock_response = Mock()
        mock_response.status_code = 200
        data = {
            'document': {'sentiment': 'positive',
                         'confidence': {'negative': 0.030769918, 'positive': 99.964096, 'neutral': 0.00513428}},
            'sentences': [{'content': 'I am Happy!', 'offset': 0, 'length': 11, 'sentiment': 'positive',
                           'confidence': {'negative': 0.0018461951, 'positive': 0.99784577, 'neutral': 0.0003080568},
                           'highlights': [{'offset': 0, 'length': 10}]}]
        }
        mock_response.text = json.dumps(data)
        mock_clova.return_value = mock_response

        response = get_sentiment("I am Happy!")
        self.assertEqual(response, 9.9933326082)

    def test_get_frequency(self):
        timestamp = datetime.now()
        texts = [
            Text(id=1, chatting_id=1, sender_id=1, msg="",
                 timestamp=timestamp - timedelta(seconds=1)),
            Text(id=1, chatting_id=1, sender_id=1, msg="",
                 timestamp=timestamp - timedelta(seconds=2)),
            Text(id=1, chatting_id=1, sender_id=1, msg="",
                 timestamp=timestamp - timedelta(seconds=3)),
            Text(id=1, chatting_id=1, sender_id=1, msg="",
                 timestamp=timestamp - timedelta(seconds=8)),
        ]
        result = get_frequency(texts)
        self.assertGreaterEqual(result, 39.9)
        self.assertLessEqual(result, 40.1)

        self.assertIsNone(get_frequency([]))

    def test_get_frequency_delta(self):
        self.assertIsNone(get_frequency_delta([], []))

    def test_score_frequency(self):
        text = Text(id=1, chatting_id=1, sender_id=1, msg="",
                    timestamp=datetime.now() - timedelta(seconds=1))
        self.assertEqual(score_frequency([text]), 10)

        text.timestamp = datetime.now() - timedelta(seconds=31)
        self.assertEqual(score_frequency([text]), 5)

        text.timestamp = datetime.now() - timedelta(seconds=61)
        self.assertEqual(score_frequency([text]), 3)

        text.timestamp = datetime.now() - timedelta(seconds=91)
        self.assertEqual(score_frequency([text]), 0)

        text.timestamp = datetime.now() - timedelta(seconds=121)
        self.assertEqual(score_frequency([text]), -2)

        text.timestamp = datetime.now() - timedelta(seconds=151)
        self.assertEqual(score_frequency([text]), -4)

        text.timestamp = datetime.now() - timedelta(seconds=181)
        self.assertEqual(score_frequency([text]), -5)

        self.assertEqual(score_frequency([]), 0)

    def test_score_frequency_delta(self):
        prev_texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        curr_texts = [
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now())
        ]
        self.assertEqual(score_frequency_delta(prev_texts, curr_texts), 0)

        self.assertEqual(score_frequency_delta([], []), 0)

    def test_score_avg_length(self):
        texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        expected_result = 0
        result = score_avg_length(texts)
        self.assertEqual(result, expected_result)

    def test_score_avg_length_delta(self):
        # Test case 1: Score average length delta of texts
        prev_texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        curr_texts = [
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now())
        ]
        expected_result = 0
        result = score_avg_length_delta(prev_texts, curr_texts)
        self.assertEqual(result, expected_result)

    def test_get_turn(self):
        texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            ),
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now()),
        ]
        self.assertEqual(get_turn(texts, 1), 0.5)

        self.assertIsNone(get_turn([], -1))

    def test_get_turn_delta(self):
        # Test case 1: Get turn delta of texts
        prev_texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        curr_texts = [
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now())
        ]
        self.assertEqual(get_turn_delta(prev_texts, curr_texts, 1), 0)

        self.assertIsNone(get_turn_delta([], [], -1))

    def test_score_turn(self):
        # Test case 1: Score turn rate of texts
        texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            ),
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now()),
        ]
        user_id = 1
        expected_result = 10
        result = score_turn(texts, user_id)
        self.assertEqual(result, expected_result)

    def test_score_turn_delta(self):
        # Test case 1: Score turn delta of texts
        prev_texts = [
            Text(
                id=1, chatting_id=1, sender_id=1, msg="Hello", timestamp=datetime.now()
            )
        ]
        curr_texts = [
            Text(id=2, chatting_id=1, sender_id=2,
                 msg="Hi", timestamp=datetime.now())
        ]
        user_id = 1
        expected_result = 0
        result = score_turn_delta(prev_texts, curr_texts, user_id)
        self.assertEqual(result, expected_result)

    def test_set_weight(self):
        # Test case 1: Change weight of parameters
        my_profile = Profile(
            name="sangin", birth=date(1999, 5, 14), sex="male", major="CLS", admission_year=2018, about_me="alpha male",
            mbti="isfj", nation_code=82,
            foods=["korean_food", "thai_food"],
            movies=["horror", "action", "comedy"],
            locations=["up", "down"],
            hobbies=["soccer", "golf"]
        )

        your_profile1 = Profile(
            name="sangin", birth=date(1999, 5, 14)
            , sex="male", major="CLS", admission_year=2018, about_me="alpha male",
            mbti=None, nation_code=82,
            foods=["italian_food", "japan_food"], movies=["romance", "action"],
            locations=["up", "jahayeon"],
            hobbies=["golf"])

        your_profile2 = Profile(
            name="abdula", birth=date(1999, 5, 14)
            , sex="male", major="CLS", admission_year=2018, about_me="alpha male",
            mbti=None, nation_code=0,
            foods=["korean_food", "japan_food", "italian_food"], movies=["horror", "action", "romance"],
            locations=['up', "down", "jahayeon"],
            hobbies=["soccer"])

        your_profile3 = Profile(
            name="jiho", birth=date(1999, 5, 14)
            , sex="male", major="CLS", admission_year=2018, about_me="alpha male",
            nation_code=1, mbti=None,
            foods=["japan_food"], movies=["action"],
            locations=["jahayeon"],
            hobbies=["golf", "soccer", "book"])

        me = User(user_id=0, verification_id=1, lang_id=1, salt="1", hash="1", profile=my_profile)
        you1 = User(user_id=1, verification_id=2, lang_id=2, salt="2", hash="2", profile=your_profile1)
        you2 = User(user_id=2, verification_id=3, lang_id=3, salt="3", hash="3", profile=your_profile2)
        you3 = User(user_id=3, verification_id=4, lang_id=4, salt="4", hash="4", profile=your_profile3)

        # 0.3780, 0.6324, 0.4082
        weight_1 = set_weight(me, you1)
        weight_2 = set_weight(me, you2)
        weight_3 = set_weight(me, you3)
        #
        expected_weight1 = np.array([0.1, 0.19, 0.11, 0.19, 0.11, 0.19, 0.11])
        expected_weight2 = np.array([0.1, 0.18, 0.12, 0.18, 0.12, 0.18, 0.12])
        expected_weight3 = np.array([0.1, 0.17, 0.13, 0.17, 0.13, 0.17, 0.13])

        self.assertEqual(weight_1.all(), expected_weight1.all())
        self.assertEqual(weight_2.all(), expected_weight2.all())
        self.assertEqual(weight_3.all(), expected_weight3.all())


if __name__ == "__main__":
    unittest.main()
