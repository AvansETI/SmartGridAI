import 'package:brains4buildings/screens/authenticate/sign_in.dart';
import 'package:brains4buildings/screens/home/screen1.dart';
import 'package:brains4buildings/screens/wrapper.dart';
import 'package:flutter/material.dart';

import '../../globals.dart';
import '../../services/auth.dart';
import '../../services/database.dart';

class ScreenFour extends StatefulWidget {
  const ScreenFour({Key? key}) : super(key: key);
  @override
  State<ScreenFour> createState() => _ScreenFourState();
}

class _ScreenFourState extends State<ScreenFour> {
  final AuthService _auth = AuthService();
  final rooms = [
    'No',
    '30 mins ago',
    'One hour ago',
    'Two hours ago',
  ];
  final durations = ['less than an hour', '1-2 hours', 'more than 3 hours'];
  String? value = '30 mins ago';
  String? value2 = 'less than an hour';
  int mood = 0;
  // ignore: non_constant_identifier_names
  int mode_of_transport = 0;
  int screen = 1;
  Map<String, int> roomsMap = {
    'No': 1,
    '30 mins ago': 2,
    'One hour ago': 3,
    'Two hours ago': 4,
  };
  DropdownMenuItem<String> buildMenuItems(String item) =>
      DropdownMenuItem(value: item, child: Text(item));
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Brains for Buildings'),
          backgroundColor: Colors.green[800],
          elevation: 0.0,
        ),
        backgroundColor: Colors.green[90],
        body: Container(
            child: Center(
          child: Column(children: [
            SizedBox(height: 140),
            Text(
              'Thank you so much! \n\nPlease submit 3 responses in a day :)',
              style: TextStyle(fontSize: 15),
            ),
            SizedBox(height: 15),
            ElevatedButton(
                onPressed: () {
                  setState(() {
                    mood = 0;
                  });
                  thermalComfort = 0;
                  thermalPreference = 0;
                  allGood = false;
                  suffocating = false;
                  humid = false;
                  smelly = false;
                  stuffy = false;
                  beverage = 0;
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => Wrapper()));
                },
                child: Text('Finish'))
          ]),
        )));
  }
}
