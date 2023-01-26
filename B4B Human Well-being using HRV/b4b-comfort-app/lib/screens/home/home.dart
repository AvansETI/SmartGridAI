// ignore_for_file: prefer_const_constructors
import 'package:brains4buildings/globals.dart';
import 'package:brains4buildings/screens/authenticate/sign_in.dart';
import 'package:brains4buildings/screens/home/screen1.dart';
import 'package:flutter/material.dart';

import '../../services/auth.dart';
import '../../services/database.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);
  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final AuthService _auth = AuthService();
  final rooms = [
    'Strip 1.15',
    'Strip 1.16',
    'Strip 1.17',
    'Strip 1.18',
    'Strip 1.19'
  ];
  final durations = ['less than an hour', '1-2 hours', 'more than 3 hours'];
  String? value = 'Strip 1.16';
  String? value2 = 'less than an hour';
  // ignore: non_constant_identifier_names
  int screen = 1;
  Map<String, int> roomsMap = {
    'Strip 1.15': 1,
    'Strip 1.16': 2,
    'Strip 1.17': 3,
    'Strip 1.18': 4,
    'Strip 1.19': 5
  };
  DropdownMenuItem<String> buildMenuItems(String item) =>
      DropdownMenuItem(value: item, child: Text(item));
  @override
  Widget build(BuildContext context) {
    if (screen == 1) {
      return ScreenOne();
    } else if (screen == 2) {
      return SignIn();
    } else if (screen == 3) {
      return ScreenOne();
    } else {
      return ScreenOne();
    }
  }
}
