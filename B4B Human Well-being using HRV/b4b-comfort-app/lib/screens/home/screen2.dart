import 'package:brains4buildings/screens/authenticate/sign_in.dart';
import 'package:brains4buildings/screens/home/screen1.dart';
import 'package:brains4buildings/screens/home/screen3.dart';
import 'package:flutter/material.dart';

// import '../../api/notifications_service.dart';
import '../../api/notifications_service.dart';
import '../../globals.dart';
import '../../services/auth.dart';
import '../../services/database.dart';

class ScreenTwo extends StatefulWidget {
  const ScreenTwo({Key? key}) : super(key: key);
  @override
  State<ScreenTwo> createState() => _ScreenTwoState();
}

class _ScreenTwoState extends State<ScreenTwo> {
  late final LocalNotificationService service;
  @override
  void initState() {
    service = LocalNotificationService();
    service.intialize();
    listenToNotification();
    super.initState();
  }

  final AuthService _auth = AuthService();
  // final rooms = [
  //   'Strip 1.15',
  //   'Strip 1.16',
  //   'Strip 1.17',
  //   'Strip 1.18',
  //   'Strip 1.19'
  // ];
  // final durations = ['less than an hour', '1-2 hours', 'more than 3 hours'];
  // String? value = 'Strip 1.16';
  // String? value2 = 'less than an hour';
  // int screen = 1;
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
      backgroundColor: Colors.grey[300],
      body: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Container(
            padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 20.0),
            child: Form(
                child: Column(children: <Widget>[
              SizedBox(height: 20.0),
              Text('5. How hot or cold do you feel?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(width: 50, height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: <Widget>[
                    thermalComfort == 1
                        ? Column(
                            children: [
                              Text(
                                'Hot',
                                style: TextStyle(color: Colors.grey[300]),
                              ),
                              SizedBox(
                                width: 45,
                                height: 45,
                                child: Material(
                                  elevation: 8,
                                  borderRadius: BorderRadius.circular(10),
                                  clipBehavior: Clip.antiAliasWithSaveLayer,
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        thermalComfort = 0;
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
                                            'images/Thermal_comfort1.png'),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(height: 3),
                              Text('Hot')
                            ],
                          )
                        : Column(
                            children: [
                              Text(
                                'Hot',
                                style: TextStyle(color: Colors.grey[300]),
                              ),
                              SizedBox(
                                width: 45,
                                height: 45,
                                child: Material(
                                  elevation: 8,
                                  borderRadius: BorderRadius.circular(10),
                                  clipBehavior: Clip.antiAliasWithSaveLayer,
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        thermalComfort = 1;
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
                                            'images/Thermal_comfort1.png'),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(height: 3),
                              Text('Hot')
                            ],
                          ),
                    SizedBox(width: 5.0, height: 50.0),
                    thermalComfort == 2
                        ? SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort2.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 2;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort2.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 5.0, height: 50.0),
                    thermalComfort == 3
                        ? SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort3.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 3;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort3.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 5),
                    thermalComfort == 4
                        ? SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort4.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 4;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort4.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 5.0, height: 50.0),
                    thermalComfort == 5
                        ? SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort5.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 5;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort5.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 5.0, height: 50.0),
                    thermalComfort == 6
                        ? SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 0;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.green, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort6.png'),
                                  ),
                                ),
                              ),
                            ),
                          )
                        : SizedBox(
                            width: 45,
                            height: 45,
                            child: Material(
                              elevation: 8,
                              borderRadius: BorderRadius.circular(10),
                              clipBehavior: Clip.antiAliasWithSaveLayer,
                              child: InkWell(
                                onTap: () {
                                  setState(() {
                                    thermalComfort = 6;
                                  });
                                },
                                child: Container(
                                  decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 3),
                                      borderRadius: BorderRadius.circular(10)),
                                  child: Ink.image(
                                    image: AssetImage(
                                        'images/Thermal_comfort6.png'),
                                  ),
                                ),
                              ),
                            ),
                          ),
                    SizedBox(width: 5.0, height: 50.0),
                    thermalComfort == 7
                        ? Column(
                            children: [
                              Text(
                                'Cold',
                                style: TextStyle(color: Colors.grey[300]),
                              ),
                              SizedBox(
                                width: 45,
                                height: 45,
                                child: Material(
                                  elevation: 8,
                                  borderRadius: BorderRadius.circular(10),
                                  clipBehavior: Clip.antiAliasWithSaveLayer,
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        thermalComfort = 0;
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
                                            'images/Thermal_comfort7.png'),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(height: 3),
                              Text('Cold'),
                            ],
                          )
                        : Column(
                            children: [
                              Text(
                                'Cold',
                                style: TextStyle(color: Colors.grey[300]),
                              ),
                              SizedBox(
                                width: 45,
                                height: 45,
                                child: Material(
                                  elevation: 8,
                                  borderRadius: BorderRadius.circular(10),
                                  clipBehavior: Clip.antiAliasWithSaveLayer,
                                  child: InkWell(
                                    onTap: () {
                                      setState(() {
                                        thermalComfort = 7;
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
                                            'images/Thermal_comfort7.png'),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(height: 3),
                              Text('Cold'),
                            ],
                          )
                  ],
                ),
              ),
              SizedBox(height: 30.0),
              Text('6. Do you want to be warmer or cooler?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: <Widget>[
                    thermalPreference == 1
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.white,
                                backgroundColor: Colors.orange,
                                side: BorderSide(color: Colors.orange)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 0;
                              });
                            },
                            child: Text('Warmer'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.orange,
                                side: BorderSide(color: Colors.orange)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 1;
                              });
                            },
                            child: Text('Warmer'),
                          ),
                    SizedBox(width: 45),
                    thermalPreference == 2
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.white,
                                backgroundColor: Colors.green,
                                side: BorderSide(color: Colors.green)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 0;
                              });
                            },
                            child: Text('I am good'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.green,
                                side: BorderSide(color: Colors.green)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 2;
                              });
                            },
                            child: Text('I am good'),
                          ),
                    SizedBox(width: 45),
                    thermalPreference == 3
                        ? OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.white,
                                backgroundColor: Colors.blue,
                                side: BorderSide(color: Colors.blue)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 0;
                              });
                            },
                            child: Text('Cooler'),
                          )
                        : OutlinedButton(
                            style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.blue,
                                side: BorderSide(color: Colors.blue)),
                            onPressed: () {
                              setState(() {
                                thermalPreference = 3;
                              });
                            },
                            child: Text('Cooler'),
                          ),
                  ],
                ),
              ),
              SizedBox(height: 20.0),
              Text('7. What do you think about the air quality?',
                  style: TextStyle(
                      fontSize: 15.0,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0)),
              SizedBox(width: 10, height: 10),
              Column(
                children: [
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: <Widget>[
                        suffocating
                            ? OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    backgroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    suffocating = false;
                                  });
                                },
                                child: Text('Suffocating'),
                              )
                            : OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    suffocating = true;
                                    allGood = false;
                                  });
                                },
                                child: Text('Suffocating'),
                              ),
                        SizedBox(
                          width: 9,
                        ),
                        humid
                            ? OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    backgroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    humid = !humid;
                                  });
                                },
                                child: Text('Humid'),
                              )
                            : OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    humid = !humid;
                                    allGood = false;
                                  });
                                },
                                child: Text('Humid'),
                              ),
                        SizedBox(width: 9),
                        stuffy
                            ? OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    backgroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    stuffy = !stuffy;
                                  });
                                },
                                child: Text('Stuffy'),
                              )
                            : OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    stuffy = !stuffy;
                                    allGood = false;
                                  });
                                },
                                child: Text('Stuffy'),
                              ),
                        SizedBox(width: 9),
                        smelly
                            ? OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    backgroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    smelly = !smelly;
                                  });
                                },
                                child: Text('Smelly'),
                              )
                            : OutlinedButton(
                                style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.black,
                                    side: BorderSide(color: Colors.black)),
                                onPressed: () {
                                  setState(() {
                                    smelly = !smelly;
                                    allGood = false;
                                  });
                                },
                                child: Text('Smelly'),
                              ),
                      ],
                    ),
                  ),
                  allGood
                      ? OutlinedButton(
                          style: OutlinedButton.styleFrom(
                              foregroundColor: Colors.white,
                              backgroundColor: Colors.green,
                              side: BorderSide(color: Colors.green)),
                          onPressed: () {
                            setState(() {
                              allGood = !allGood;
                            });
                          },
                          child: Text('All good!'),
                        )
                      : OutlinedButton(
                          style: OutlinedButton.styleFrom(
                              foregroundColor: Colors.green,
                              side: BorderSide(color: Colors.green)),
                          onPressed: () {
                            setState(() {
                              allGood = !allGood;
                              suffocating = false;
                              stuffy = false;
                              humid = false;
                              smelly = false;
                            });
                          },
                          child: Text('All good!'),
                        ),
                ],
              ),
              SizedBox(height: 50.0),
              ElevatedButton(
                  onPressed: (thermalComfort != 0) &&
                          (thermalPreference != 0) &&
                          (suffocating || humid || stuffy || smelly || allGood)
                      ? () async {
                          thermalComfort = thermalComfort;
                          thermalPreference = thermalPreference;
                          await service.showScheduledNotificationtwo(
                              id: 2,
                              title: 'Comfort App',
                              body:
                                  'Please don\'t forget to self-report if you are in the HHS',
                              scheduledDate: DateTime.now());
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const ScreenThree()));
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
