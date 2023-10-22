abstract class User {
  final String id;
  final String name;
  final UserType userType;
  final String email;
  final Profile profile;

  const User({
    required this.id,
    required this.name,
    required this.userType,
    required this.email,
    required this.profile,
  });
}

class KoreanUser extends User {
  final List<Language> wantedLanguages;

  KoreanUser({
    required super.id,
    required super.name,
    required super.userType,
    required super.email,
    required this.wantedLanguages,
    required super.profile,
  });
}

class ForeignUser extends User {
  final int nationCode;
  final Language mainLanguage;
  final List<Language> subLanguages;

  ForeignUser({
    required super.id,
    required super.name,
    required super.userType,
    required super.email,
    required this.nationCode,
    required this.mainLanguage,
    required this.subLanguages,
    required super.profile,
  });
}

enum UserType {
  korean,
  foreign,
}

enum Language {
  english,
  spanish,
  chinese,
  arabic,
  french,
  german,
  japanese,
  russian,
  portuguese,
  korean,
  italian,
  dutch,
  swedish,
  turkish,
  hebrew,
  hindi,
  thai,
  greek,
  vietnamese,
  finnish,
}

enum Mbti {
  intj,
  intp,
  entj,
  entp,
  infj,
  infp,
  enfj,
  enfp,
  istj,
  isfj,
  estj,
  esfj,
  istp,
  isfp,
  estp,
  esfp,
  unknown,
}

class Profile {
  final DateTime birth;
  final Sex sex;
  final String major;
  final int admissionYear;
  final String aboutMe;
  final Mbti mbti;
  final List<Hobby> hobbies;
  final List<FoodCategory> foodCategories;
  final List<MovieGenre> movieGenres;
  final List<Location> locations;
  final String? imgUrl;

  const Profile({
    required this.birth,
    required this.sex,
    required this.major,
    required this.admissionYear,
    required this.aboutMe,
    required this.mbti,
    required this.hobbies,
    required this.foodCategories,
    required this.movieGenres,
    required this.locations,
    this.imgUrl,
  });
}

enum Sex {
  male,
  female,
  nonBinary,
}

enum FoodCategory {
  korean,
  spanish,
  american,
  italian,
  thai,
  chinese,
  japanese,
  indian,
  mexican,
  vegan,
  dessert,
}

enum MovieGenre {
  action,
  adventure,
  animation,
  comedy,
  drama,
  fantasy,
  horror,
  mystery,
  romance,
  scienceFiction,
  thriller,
  western,
}

enum Hobby {
  painting,
  gardening,
  hiking,
  reading,
  cooking,
  photography,
  dancing,
  swimming,
  cycling,
  traveling,
  gaming,
  fishing,
  knitting,
  music,
  yoga,
  writing,
  shopping,
  teamSports,
  fitness,
  movie,
}

enum Location {
  humanity,
  naturalScience,
  dormitory,
  socialScience,
  humanEcology,
  agriculture,
  highEngineering,
  lowEngineering,
  business,
  jahayeon,
  studentUnion,
  seolYeep,
  nockDoo,
  bongcheon,
}