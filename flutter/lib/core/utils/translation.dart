import 'dart:ui';

import 'package:get/get.dart';

class MyTranslation extends Translations {
  @override
  Map<String, Map<String, String>> get keys => {
    "en" : {
      "간식보다 재밌는 언어교환" : "Language exchange platform\nBetter than snacks",
      "로그인" : "Login",
      "회원가입" : "Sign up",
      "이메일 입력" : "Your email",
      "학교 이메일 (university email)" : "University email (학교 이메일)",
      "비밀번호 입력" : "Your password",
      "비밀번호 (password)" : "Password (비밀번호)",
      "로그인에 실패했어요. 이메일, 비밀번호를 다시 확인해주세요!" : "Failed Login. Please check your credentials again",
      "아직 회원이 아닌신가요?" : "Have you not signed up yet?",
      '저는\n한국 학생입니다.' : "I'm a\nKorean student",
      "I'm a Korean student" : "저는 한국 학생입니다",
      "I'm a\nforeign exchange student" : "I'm a\nforeign exchange student",
      "저는 외국인 교환학생입니다." : "저는 외국인 교환학생입니다.",
      '다음' : "Next",
      "한국 학생이신가요,\n아니면 외국인 교환 학생이신가요?" : "Are you a Korean student,\n or a foreign exchange student?",
      "Are you a Korean student,\n or a foreign exchange student?" : "한국 학생이신가요,\n아니면 외국인 교환 학생이신가요?",
      '회원가입을 위해\n학교 이메일을 인증해주세요' : "To sign up,\nplease verify your SNU email",
      "학교 이메일 입력" : "Your snu.ac.kr email",
      '인증하기' : "Send",
      "서울대학교 계정을 사용해주세요 :)" : "Please enter your SNU email :)",
      "이메일로 전송된 코드를 입력해주세요." : "A verification code has been sent to your email",
      "코드 6자리 입력" : "6-digit code",
      "확인" : "Confirm",
      "잘못된 코드에요. 다시 한번 확인해주세요!" : "Wrong code. Please check again!",
      "성공적으로 인증되었어요!" : "Verification complete!",
      '회원정보 입력' : "Account info",
      "*입력하신 회원정보는 다른 사용자들에게 공개되지 않고 회원관리 및 언어교환 상대 추천을 위해 내부적으로만 이용됩니다." : "*The information you enter in this page will remain secret from other users, and will only be used for recommendation / personalized roadmap services",
      '사용할 비밀번호를\n입력해주세요' : "Create your password",
      "*6자 이상, 20자 이하의 숫자/영문" : "*Use alphabet or numbers, with at least 6 to maximum 20 characters",
      "비밀번호를 재입력해주세요." : "Confirm password",
      "비밀번호 재입력" : "Your password (again)",
      "비밀번호가 일치해요!" : "Confirm complete!",
      "비밀번호가 일치하지 않아요" : "The two are different. Check again",
      "생년월일" : "Date of birth",
      "  YYYYMMDD         예시) 19990131" : "  YYYYMMDD         ex) 19990131",
      "성별" : "Gender",
      "성별 선택" : "Select gender",
      "입학 연도" : "Uni admission year",
      "입학 연도 선택" : "Select year",
      "학과" : "Major",
      "Mbti" : "Mbti",
      '학과 선택' : "Select major",
      '단과대학 선택' : "Select dept",
      '공과대학' : "Engineering",
      '컴퓨터공학부' : "CSE",
      '기계공학부' : "ME",
      '전기정보공학부' : "ECE",
      "mbti 선택" : "Select mbti",
      "잘 모르겠어요" : "I dunno",

      "프로필 생성" : "Create profile",
      "작성된 프로필은 다른 유저들이 볼 수 있어요" : "Other users can see your profile page",
      "활동할 닉네임을 입력해주세요" : "Choose a nickname :)",
      "닉네임 입력" : "Your nickname",
      "닉네임은 한글/영문/숫자로, 최대 8자까지 가능해요" : "Up to 8 characters, alphabet/Korean/numbers",
      "자신을 소개하는 문장 하나를 입력해주세요" : "A sentence that best describes you",
      "자기소개 입력" : "About me...",
      "프로필은 나중에도 수정이 가능하니 부담 갖지 말고 적어주세요!" : "You can edit your profile page later, so feel no pressure!",
      "주로 사용하는 언어" : "I am most comfortable in...",
      "주언어 외 사용 가능 언어" : "I can also speak...",
      "교환을 희망하는 언어" : "Languages I want to learn",

      "영어": "English",
      "스페인어": "Spanish",
      "중국어": "Chinese",
      "아랍어": "Arabic",
      "프랑스어": "French",
      "독일어": "German",
      "일본어": "Japanese",
      "러시아어": "Russian",
      "포르투갈어": "Portuguese",
      "이탈리아어": "Italian",
      "네덜란드어": "Dutch",
      "스웨덴어": "Swedish",
      "핀란드어": "Finnish",
      "터키어": "Turkish",
      "히브리어": "Hebrew",
      "힌디어": "Hindi",
      "태국어": "Thai",
      "그리스어": "Greek",
      "베트남어": "Vietnamese",

      "선택 완료 시 우측 보내기 버튼 클릭" : "Tap send icon when done",
      '프로필 작성 완료' : "Nice work!",
      "제출하기" : "Submit",
      '키워드를 선택해주세요' : "Select keyword(s)",
      "SNEK에 온 걸 환영해요!" : "Welcome to SNEK!",
      "우선 몇가지를 물어보려 해요!\n 금방 끝날테니 안심하세요 :)" : "Ooh, I have some questions!\nDon't worry, I'll be quick :)",
      "첫번째, 좋아하는 취미 몇 가지를 골라주세요." : "First, what are some of your favorite hobbies?",
      "감사해요!" : "Thanks!",
      "두번째로, 좋아하는 음식 종류를 몇 개 골라주세요." : "And next, what cuisines do you usually enjoy?",
      "이제 거의 다 왔어요!" : "Almost there!",
      "어떤 영화 장르를 좋아하시나요? 몇 개 골라주세요!" : "Do you have any movie genre(s) that you prefer?",
      "마지막이에요!" : "And the final question...",
      "주로 학교에서 출몰하는 장소를 골라주세요" : "Where do you usually hang around in school?",
      "현재 검색되는 유저가 존재하지 않습니다" : "Currently, no user is being searched",
      "희망 언어" : "Language of hope",
      "채팅 신청" : "Request a chat",
      "사용하는 주언어": "The main language",
      "# 주로 출몰하는 장소" : "# Mainly haunting places",
      "# 영화 장르" : "# Movie genre",
      "# 음식" : "# Food",
      "# 취미": "# Hobby",
      "좋아하는 것들" :"What you like",
      "희망 교환 언어" : "Hope exchange language",
      "주 언어 외 구사 가능 언어" : "Language that you can speak\nother than your main language",









    },
  };
}

abstract class MyLanguageUtil {
  static LanguageMode _currentLanguage = LanguageMode.kr;
  static Locale get getLocale => Locale(_currentLanguage.name);
  static void toggle(){
    if (_currentLanguage==LanguageMode.kr) {
      _currentLanguage = LanguageMode.en;
      Get.updateLocale(Locale(LanguageMode.en.name));
    } else {
      _currentLanguage = LanguageMode.kr;
      Get.updateLocale(Locale(LanguageMode.kr.name));
    }

  }
}

enum LanguageMode {
  en,
  kr
}