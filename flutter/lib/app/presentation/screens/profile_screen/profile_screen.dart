import 'package:get/get.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/app/domain/models/user.dart';
import 'package:mobile_app/app/presentation/widgets/app_bars.dart';
import 'package:mobile_app/app/presentation/widgets/buttons.dart';
import 'package:mobile_app/core/themes/color_theme.dart';

// ignore: unused_import
import 'profile_screen_controller.dart';

class ProfileScreen extends GetView<ProfileScreenController> {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: const NotiAppBar(
        title: Text(
          "프로필",
          style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w700,
              color: Color(0xff2d3a45)),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.only(top: 16, left: 24, right: 24),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildSimpleProfile(),
              const SizedBox(height: 20),
              MainButton(mainButtonType: MainButtonType.key, text: "로그아웃", onPressed: controller.onLogOutButtonTap),
              const SizedBox(height: 24),

              if (controller.userController.userProfile.nationCode != 82)
                _buildMainLanguageContainer(),
              Text(
                (controller.userController.userProfile.nationCode == 82)
                    ? "희망 교환 언어"
                    : "주 언어 외 구사 가능 언어",
                style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: MyColor.textBaseColor.withOpacity(0.8)),
              ),
              const SizedBox(height: 8),
              _buildLanguageList(),
              SizedBox(height: 24),
              Text(
                "좋아하는 것들",
                style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: MyColor.textBaseColor.withOpacity(0.8)),
              ),
              SizedBox(height: 8),
              _buildLikeContainer()

            ],
          ),
        ),
      ),

    );
  }

  Row _buildSimpleProfile() {
    return Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: SizedBox.fromSize(
                    size: const Size.fromRadius(70),
                    child: Image.asset('assets/images/snek_profile_img_1.webp'),
                  ),
                ),
                const SizedBox(width: 20),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(controller.userController.userName,
                        style: const TextStyle(
                            color: Color(0xff2d3a45),
                            fontWeight: FontWeight.w700,
                            fontSize: 24)),
                    const SizedBox(height: 10),
                    Wrap(
                      children: [
                        Container(
                          width: 120,
                          decoration: BoxDecoration(border: Border.all(color: Colors.white, width: 2), borderRadius: BorderRadius.circular(10)),
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          child: Text(controller.userController.userAboutMe,
                              style: const TextStyle(
                                  color: Color(0xff2d3a45),
                                  fontWeight: FontWeight.w700,
                                  fontSize: 20)),
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            );
  }

  Container _buildLikeContainer() {
    return Container(
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.black.withOpacity(0.1))),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("# 취미",
                        style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: MyColor.textBaseColor.withOpacity(0.8))),
                    SizedBox(height: 6),
                    _buildHobbyContainer(),
                    SizedBox(height: 6),
                    Divider(
                        color: Colors.black.withOpacity(0.1), thickness: 1),
                    SizedBox(height: 6),
                    Text("# 음식",
                        style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: MyColor.textBaseColor.withOpacity(0.8))),
                    SizedBox(height: 6),
                    _buildFoodContainer(),
                    SizedBox(height: 6),
                    Divider(
                        color: Colors.black.withOpacity(0.1), thickness: 1),
                    SizedBox(height: 6),
                    Text("# 영화 장르",
                        style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: MyColor.textBaseColor.withOpacity(0.8))),
                    SizedBox(height: 6),
                    _buildMovieContainer(),
                    SizedBox(height: 6),
                    Divider(
                        color: Colors.black.withOpacity(0.1), thickness: 1),
                    SizedBox(height: 6),
                    Text("# 주로 출몰하는 장소",
                        style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: MyColor.textBaseColor.withOpacity(0.8))),
                    SizedBox(height: 6),
                    _buildLocationContainer()
                  ],
                ),
              ),
            );
  }


  Container _buildAboutMeContainer() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 12),
      decoration: const BoxDecoration(
          border: Border(
              left: BorderSide(width: 3, color: MyColor.purple))),
      child: Column(
        children: [
          Text(
            controller.userController.userAboutMe,
            style: TextStyle(fontSize: 13),
          ),
        ],
      ),
    );
  }

  Container _buildMainLanguageContainer() {
    return Container(
      child: Column(
        children: [
          Text(
            "사용하는 주언어",
            style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                color: MyColor.textBaseColor.withOpacity(0.8)),
          ),
          const SizedBox(height: 8),
          Container(
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                border:
                Border.all(color: Colors.black.withOpacity(0.1), width: 1)),
            padding: const EdgeInsets.all(6),
            margin: const EdgeInsets.all(4),
            child: Text(
              controller.languageFlagMap[controller.userController.userMainLanguage]!,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: MyColor.textBaseColor,
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Container _buildHobbyContainer() {
    return Container(
        child: Wrap(
          children: [
            for (Hobby hobby in controller.userController.userProfile.hobbies)
              Container(
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Color(0xfff8f1fb)),
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                margin: const EdgeInsets.all(4),
                child: Text(
                  controller.hobbyKoreanMap[hobby]!,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: MyColor.textBaseColor,
                  ),
                ),
              ),
          ],
        ));
  }

  Container _buildFoodContainer() {
    return Container(
        child: Wrap(
          children: [
            for (FoodCategory foodCategory
            in controller.userController.userProfile.foodCategories)
              Container(
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Color(0xfff8f1fb)),
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                margin: const EdgeInsets.all(4),
                child: Text(
                  controller.foodKoreanMap[foodCategory]!,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: MyColor.textBaseColor,
                  ),
                ),
              ),
          ],
        ));
  }

  Container _buildMovieContainer() {
    return Container(
        child: Wrap(
          children: [
            for (MovieGenre moviegenre in controller.userController.userProfile.movieGenres)
              Container(
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Color(0xfff8f1fb)),
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                margin: const EdgeInsets.all(4),
                child: Text(
                  controller.movieKoreanMap[moviegenre]!,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: MyColor.textBaseColor,
                  ),
                ),
              ),
          ],
        ));
  }

  Container _buildLocationContainer() {
    return Container(
        child: Wrap(
          children: [
            for (Location location in controller.userController.userProfile.locations)
              Container(
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Color(0xfff8f1fb)),
                padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                margin: const EdgeInsets.all(4),
                child: Text(
                  controller.locationKoreanMap[location]!,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: MyColor.textBaseColor,
                  ),
                ),
              ),
          ],
        ));
  }

  Wrap _buildLanguageList() {
    return Wrap(
      children: [
        for (Language language in controller.userController.userLanguages)
          Container(
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10),
                border:
                Border.all(color: Colors.black.withOpacity(0.1), width: 1)),
            padding: const EdgeInsets.all(6),
            margin: const EdgeInsets.all(4),
            child: Text(
              controller.languageFlagMap[language]!,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
                color: MyColor.textBaseColor,
              ),
            ),
          ),
      ],
    );
  }
}

// GetPage(
//   name: ,
//   page: () => const ProfileScreen(),
//   binding: ProfileScreenBinding(),
// )
