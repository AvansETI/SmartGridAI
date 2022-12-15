import 'package:brains4buildings/screens/home/screen2.dart';
import 'package:flutter/material.dart';

import '../../globals.dart';
import '../../services/auth.dart';

class ScreenOne extends StatefulWidget {
  const ScreenOne({Key? key}) : super(key: key);
  @override
  State<ScreenOne> createState() => _ScreenOneState();
}

class _ScreenOneState extends State<ScreenOne> {
  final AuthService _auth = AuthService();
  final rooms = [
    'LA001',
    'LA008',
    'LA020',
    'LA020a',
    'LA021',
    'LA023',
    'LA025a',
    'LA025b',
    'LA025c',
    'LA026',
    'LA029',
    'LA036',
    'LA043',
    'LA121',
    'LA123',
    'LA124',
    'LA125',
    'LA126',
    'LA127',
    'LA128',
    'LA134',
    'LA136',
    'LA221',
    'LA222',
    'LA223',
    'LA225',
    'LA227',
    'LA229',
    'LA234',
    'LA235',
    'LA236',
    'LA301',
    'LA303',
    'LA305',
    'LA402',
    'LA420',
    'LA423',
    'LA425',
    'LA501',
    'LA502',
    'LA503',
    'LA520',
    'LA523',
    'LD021',
    'LD022',
    'LD023',
    'LD024',
    'LD025',
    'LD027',
    'LD102',
    'LD103',
    'LD104',
    'LD105',
    'LD106',
    'LD107',
    'LD108',
    'LD109',
    'LD110',
    'LD111',
    'LD112',
    'LD122',
    'LD124',
    'LD125',
    'LD126',
    'LD240',
    'LD302',
    'LD303',
    'LD305',
    'LD306',
    'LD307',
    'LD308',
    'LD309',
    'LD310',
    'LD311',
    'LD312',
    'LD313',
    'LD314',
    'LD315',
    'LD316',
    'LD323',
    'LD328',
    'LA Explora floor 1',
    'LA Explora floor 2',
    'LA Explora floor 3',
    'LA Explora floor 4',
    'LA Explora floor 5'
  ];
  final durations = ['less than an hour', '1-2 hours', 'more than 3 hours'];
  String? value = 'LA001';
  String? value2 = 'less than an hour';
  // ignore: non_constant_identifier_names
  bool nextButtonActive = false;
  // int screen = 1;
  Map<String, int> roomsMap = {
    'LA001': 1,
    'LA008': 2,
    'LA020': 3,
    'LA020a': 4,
    'LA021': 5,
    'LA023': 6,
    'LA025a': 7,
    'LA025b': 8,
    'LA025c': 9,
    'LA026': 10,
    'LA029': 11,
    'LA036': 12,
    'LA043': 13,
    'LA121': 14,
    'LA123': 15,
    'LA124': 16,
    'LA125': 17,
    'LA126': 18,
    'LA127': 19,
    'LA128': 20,
    'LA134': 21,
    'LA136': 22,
    'LA221': 23,
    'LA222': 24,
    'LA223': 25,
    'LA225': 26,
    'LA227': 27,
    'LA229': 28,
    'LA234': 29,
    'LA235': 30,
    'LA236': 31,
    'LA301': 32,
    'LA303': 33,
    'LA305': 34,
    'LA402': 35,
    'LA420': 36,
    'LA423': 37,
    'LA425': 38,
    'LA501': 39,
    'LA502': 40,
    'LA503': 41,
    'LA520': 42,
    'LA523': 43,
    'LD021': 44,
    'LD022': 45,
    'LD023': 46,
    'LD024': 47,
    'LD025': 48,
    'LD027': 49,
    'LD102': 50,
    'LD103': 51,
    'LD104': 52,
    'LD105': 53,
    'LD106': 54,
    'LD107': 55,
    'LD108': 56,
    'LD109': 57,
    'LD110': 58,
    'LD111': 59,
    'LD112': 60,
    'LD122': 61,
    'LD124': 62,
    'LD125': 63,
    'LD126': 64,
    'LD240': 65,
    'LD302': 66,
    'LD303': 67,
    'LD305': 68,
    'LD306': 69,
    'LD307': 70,
    'LD308': 71,
    'LD309': 72,
    'LD310': 73,
    'LD311': 74,
    'LD312': 75,
    'LD313': 76,
    'LD314': 77,
    'LD315': 78,
    'LD316': 79,
    'LD323': 80,
    'LD328': 81,
    'LA Explora floor 1': 82,
    'LA Explora floor 2': 83,
    'LA Explora floor 3': 84,
    'LA Explora floor 4': 85,
    'LA Explora floor 5': 86
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
        actions: <Widget>[
          TextButton.icon(
            icon: Icon(Icons.person),
            label: Text('logout'),
            onPressed: () async {
              await _auth.signOut();
              setState(() {
                mood = 0;
                modeOfTransport = 0;
                cloth1 = false;
                cloth2 = false;
                cloth3 = false;
                cloth4 = false;
                cloth5 = false;
                cloth6 = false;
                cloth7 = false;
              });
            },
          )
        ],
      ),
      backgroundColor: Colors.green[90],
      body: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: SingleChildScrollView(
          child: Container(
            padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 20.0),
            child: Form(
                child: Column(children: <Widget>[
              SizedBox(height: 20.0),
              Text(
                '1. How do you feel right now?',
                style: TextStyle(
                    fontSize: 15.0,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 2.0),
              ),
              SizedBox(width: 10, height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: <Widget>[
                    mood == 1
                        ? SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood1.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 1;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood1.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 25.0, height: 50.0),
                    mood == 2
                        ? SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood2.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 2;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood2.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    const SizedBox(width: 25.0, height: 50.0),
                    mood == 3
                        ? SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood3.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 3;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood3.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    const SizedBox(width: 25.0, height: 50.0),
                    mood == 4
                        ? SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood4.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 4;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood4.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    const SizedBox(width: 25.0, height: 50.0),
                    mood == 5
                        ? SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood5.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 50,
                            height: 50,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    mood = 5;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage('images/Mood5.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                  ],
                ),
              ),
              SizedBox(height: 30.0),
              Text('2. How did you come to Avans today?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(width: 10, height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Column(
                  children: [
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: <Widget>[
                          SizedBox(
                            width: 25,
                            height: 50,
                          ),
                          modeOfTransport == 1
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov1.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 1;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov1.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 50.0, height: 50.0),
                          modeOfTransport == 2
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov2.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 2;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov2.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 50.0, height: 50.0),
                          modeOfTransport == 3
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov3.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 3;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov3.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                        ],
                      ),
                    ),
                    SizedBox(width: 15, height: 15),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          SizedBox(width: 50.0, height: 50.0),
                          modeOfTransport == 6
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov4.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 6;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov4.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 50.0, height: 50.0),
                          modeOfTransport == 4
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov5.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 4;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov5.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 50.0, height: 50.0),
                          modeOfTransport == 5
                              ? SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 0;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.green, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov6.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                )
                              : SizedBox(
                                  width: 50,
                                  height: 50,
                                  child: Material(
                                    elevation: 8,
                                    borderRadius: BorderRadius.circular(10),
                                    clipBehavior: Clip.antiAliasWithSaveLayer,
                                    child: InkWell(
                                      onTap: () {
                                        setState(() {
                                          modeOfTransport = 5;
                                        });
                                      },
                                      child: Container(
                                        decoration: BoxDecoration(
                                            color: Colors.transparent,
                                            border: Border.all(
                                                color: Colors.white, width: 3),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Ink.image(
                                          image: AssetImage(
                                              'images/Icons_Mov6.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 30.0),
              Text('3. Where are you located in the building?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              DropdownButton<String>(
                  value: value,
                  items: rooms.map(buildMenuItems).toList(),
                  onChanged: (value) => setState(() => this.value = value)),
              SizedBox(height: 10.0),
              Text('4. How long have you been here',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              DropdownButton<String>(
                  value: value2,
                  items: durations.map(buildMenuItems).toList(),
                  onChanged: (value2) => setState(() => this.value2 = value2)),
              SizedBox(height: 35.0),
              ElevatedButton(
                  onPressed: (mood != 0) && (modeOfTransport != 0)
                      ? () async {
                          // setState(() => screen = 2);
                          location = value;
                          durationInBuilding = value2;
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const ScreenTwo()));
                        }
                      : null,
                  child: Text('Next'))
            ])),
          ),
        ),
      ),
    );
  }
}
