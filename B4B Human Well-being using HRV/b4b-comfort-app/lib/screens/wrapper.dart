// ignore_for_file: prefer_const_constructors
import 'package:brains4buildings/screens/authenticate/authenticate.dart';
import 'package:brains4buildings/screens/home/home.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/user.dart';

class Wrapper extends StatefulWidget {
  const Wrapper({Key? key}) : super(key: key);

  @override
  State<Wrapper> createState() => _WrapperState();
}

class _WrapperState extends State<Wrapper> {
  @override
  Widget build(BuildContext context) {
    final user = Provider.of<OurUser?>(context);
    if (user == null) {
      return Authenticate();
    } else {
      return Home();
    }
  }
}
