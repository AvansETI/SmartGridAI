import 'package:brains4buildings/screens/authenticate/sign_in.dart';
import 'package:brains4buildings/screens/home/screen1.dart';
import 'package:brains4buildings/screens/home/screen4.dart';
import 'package:flutter/material.dart';

// import '../../api/notifications_service.dart';
import '../../api/notifications_service.dart';
import '../../globals.dart';
import '../../services/auth.dart';
import '../../services/database.dart';

class ScreenThree extends StatefulWidget {
  const ScreenThree({Key? key}) : super(key: key);
  @override
  State<ScreenThree> createState() => _ScreenThreeState();
}

class _ScreenThreeState extends State<ScreenThree> {
  late final LocalNotificationService service;
  @override
  void initState() {
    service = LocalNotificationService();
    service.intialize();
    listenToNotification();
    super.initState();
  }

  final AuthService _auth = AuthService();
  final eatenRecently = [
    'No',
    '30 mins ago',
    'One hour ago',
    'Two hours ago',
  ];
  // final durations = ['less than an hour', '1-2 hours', 'more than 3 hours'];
  String? value = '30 mins ago';
  // String? value2 = 'less than an hour';
  // int beverage = 0;
  // // ignore: non_constant_identifier_names
  // // int mode_of_transport = 0;
  // bool cloth1 = false;
  // bool cloth2 = false;
  // bool cloth3 = false;
  // bool cloth4 = false;
  // bool cloth5 = false;
  // bool cloth6 = false;
  // bool cloth7 = false;
  // int screen = 1;
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
      body: SingleChildScrollView(
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Container(
            padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 20.0),
            child: Form(
                child: Column(children: <Widget>[
              SizedBox(height: 20.0),
              Text('8. Have you eaten recently?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              DropdownButton<String>(
                  value: value,
                  items: eatenRecently.map(buildMenuItems).toList(),
                  onChanged: (value) => setState(() => this.value = value)),
              SizedBox(height: 20.0),
              Text('9. Have you had a hot/cold beverage recently?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: <Widget>[
                    SizedBox(
                      width: 25,
                    ),
                    beverage == 1
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.white,
                                backgroundColor: Colors.orange,
                                side: BorderSide(color: Colors.orange)),
                            onPressed: () {
                              setState(() {
                                beverage = 0;
                              });
                            },
                            child: Text('Hot'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.orange,
                                side: BorderSide(color: Colors.orange)),
                            onPressed: () {
                              setState(() {
                                beverage = 1;
                              });
                            },
                            child: Text('Hot'),
                          ),
                    SizedBox(
                      width: 55,
                      height: 50,
                    ),
                    beverage == 2
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.white,
                                backgroundColor: Colors.green,
                                side: BorderSide(color: Colors.green)),
                            onPressed: () {
                              setState(() {
                                beverage = 0;
                              });
                            },
                            child: Text('No'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.green,
                                side: BorderSide(color: Colors.green)),
                            onPressed: () {
                              setState(() {
                                beverage = 2;
                              });
                            },
                            child: Text('No'),
                          ),
                    SizedBox(
                      width: 55,
                      height: 50,
                    ),
                    beverage == 3
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.white,
                                backgroundColor: Colors.blue,
                                side: BorderSide(color: Colors.blue)),
                            onPressed: () {
                              setState(() {
                                beverage = 0;
                              });
                            },
                            child: Text('Cold'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                primary: Colors.blue,
                                side: BorderSide(color: Colors.blue)),
                            onPressed: () {
                              setState(() {
                                beverage = 3;
                              });
                            },
                            child: Text('Cold'),
                          ),
                  ],
                ),
              ),
              SizedBox(height: 20.0),
              Text('10. What are you wearing today?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Column(
                  children: [
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: <Widget>[
                          cloth1
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
                                          cloth1 = !cloth1;
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
                                          image:
                                              AssetImage('images/Icons2.png'),
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
                                          cloth1 = !cloth1;
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
                                          image:
                                              AssetImage('images/Icons2.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 25.0, height: 50.0),
                          cloth2
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
                                          cloth2 = !cloth2;
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
                                          image:
                                              AssetImage('images/Icons3.png'),
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
                                          cloth2 = !cloth2;
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
                                          image:
                                              AssetImage('images/Icons3.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 25.0, height: 50.0),
                          cloth3
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
                                          cloth3 = !cloth3;
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
                                          image:
                                              AssetImage('images/Icons4.png'),
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
                                          cloth3 = !cloth3;
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
                                          image:
                                              AssetImage('images/Icons4.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 25.0, height: 50.0),
                          cloth4
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
                                          cloth4 = !cloth4;
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
                                          image:
                                              AssetImage('images/Icons5.png'),
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
                                          cloth4 = !cloth4;
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
                                          image:
                                              AssetImage('images/Icons5.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 25.0, height: 50.0),
                          cloth5
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
                                          cloth5 = !cloth5;
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
                                          image:
                                              AssetImage('images/Icons6.png'),
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
                                          cloth5 = !cloth5;
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
                                          image:
                                              AssetImage('images/Icons6.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                        ],
                      ),
                    ),
                    SizedBox(
                      height: 10,
                    ),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          cloth6
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
                                          cloth6 = !cloth6;
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
                                          image:
                                              AssetImage('images/Icons7.png'),
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
                                          cloth6 = !cloth6;
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
                                          image:
                                              AssetImage('images/Icons7.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                          SizedBox(width: 25.0, height: 50.0),
                          cloth7
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
                                          cloth7 = !cloth7;
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
                                          image:
                                              AssetImage('images/Icons8.png'),
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
                                          cloth7 = !cloth7;
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
                                          image:
                                              AssetImage('images/Icons8.png'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                        ],
                      ),
                    )
                  ],
                ),
              ),
              SizedBox(height: 50.0),
              ElevatedButton(
                  onPressed: (beverage != 0) &&
                          (cloth1 ||
                              cloth2 ||
                              cloth3 ||
                              cloth4 ||
                              cloth5 ||
                              cloth6 ||
                              cloth7)
                      ? () async {
                          // setState(() => screen = 2);
                          await DatabaseService(uid: unique_identification)
                              .updateUserData(
                                  'username',
                                  mood,
                                  modeOfTransport,
                                  location,
                                  durationInBuilding,
                                  thermalComfort,
                                  thermalPreference,
                                  suffocating,
                                  humid,
                                  stuffy,
                                  smelly,
                                  allGood,
                                  value,
                                  beverage,
                                  cloth1,
                                  cloth2,
                                  cloth3,
                                  cloth4,
                                  cloth5,
                                  cloth6,
                                  cloth7);
                          await service.showScheduledNotification(
                              id: 0,
                              title: 'Comfort App',
                              body:
                                  'Please don\'t forget to self-report if you are in the HHS',
                              scheduledDate: DateTime.now());

                          await service.showScheduledNotificationthree(
                              id: 3,
                              title: 'Comfort App',
                              body:
                                  'Please don\'t forget to self-report if you are in the HHS',
                              scheduledDate: DateTime.now());
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const ScreenFour()));
                        }
                      : null,
                  child: Text('Next'))
            ])),
          ),
        ),
      ),
    );
  }

  void listenToNotification() =>
      service.onNotificationClick.stream.listen(onNoticationListener);

  void onNoticationListener(String? payload) {
    if (payload != null && payload.isNotEmpty) {
      print('payload $payload');

      Navigator.push(
          context, MaterialPageRoute(builder: ((context) => ScreenOne())));
    }
  }
}
