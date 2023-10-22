import 'package:get/get.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/app/presentation/widgets/app_bars.dart';
import 'package:mobile_app/app/presentation/widgets/buttons.dart';
import 'package:mobile_app/app/presentation/widgets/text_form_fields.dart';

// ignore: unused_import
import 'email_screen_controller.dart';

class EmailScreen extends GetView<EmailScreenController> {
  const EmailScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
        appBar: const SimpleAppBar(),
        body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Padding(
                  padding:
                      EdgeInsets.symmetric(horizontal: 4).copyWith(top: 16),
                  child: const Text(
                    '회원가입을 위해\n학교 이메일을 인증해주세요',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Expanded(
                      child: MainTextFormField(
                        textEditingController: controller.emailCon,
                        hintText: "학교 이메일 입력",
                        textStyle: TextStyle(
                            fontSize: 14, fontWeight: FontWeight.w400),
                        verticalPadding: 15,
                      ),
                    ),
                    const SizedBox(width: 12),
                    SmallButton(
                        text: '인증하기', onPressed: () => {},),
                  ],
                ),
                SizedBox(height: 20),
                if (controller.emailSent) _buildCodeContainer()
              ],
            ),
          ),
        ),
        bottomNavigationBar: BottomNextButton(onPressed: controller.temporaryOnTap),
    );
  }

  Widget _buildCodeContainer() {
    return Container(
      decoration: BoxDecoration(
          border: Border(
              top: BorderSide(width: 1, color: Colors.black.withOpacity(0.1)))),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          SizedBox(height: 20),
          Text("이메일로 전송된 코드를 입력해주세요.",
              style: TextStyle(
                  color: Color(0xff2d3a45).withOpacity(0.8),
                  fontWeight: FontWeight.w500,
                  fontSize: 14)),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Expanded(
                  child: MainTextFormField(
                    textEditingController: controller.emailCon,
                    hintText: "코드 8자리 입력",
                    textStyle: TextStyle(
                        fontSize: 14, fontWeight: FontWeight.w400),
                    verticalPadding: 15,
                  ),
                ),
                const SizedBox(width: 12),
                SmallButton(
                    text: '확인', onPressed: () => {}),
              ],
            ),
          ),
          if (controller.certSuccess)
            Text("성공적으로 인증되었어요!",
                style: TextStyle(
                    color: Color(0xff9f75d1),
                    fontWeight: FontWeight.w600,
                    fontSize: 14))
        ],
      ),
    );
  }
}