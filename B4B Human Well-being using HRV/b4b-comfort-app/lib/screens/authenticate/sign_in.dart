// ignore_for_file: prefer_const_constructors
import 'package:brains4buildings/screens/authenticate/register.dart';
import 'package:brains4buildings/services/auth.dart';
import 'package:flutter/material.dart';

import '../../globals.dart';

class SignIn extends StatefulWidget {
  const SignIn({Key? key}) : super(key: key);

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  final AuthService _auth = AuthService();
  String email = '';
  String password = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      backgroundColor: Colors.white,
      appBar: AppBar(
        centerTitle: true,
        title: Text('Brains4Buildings'),
        backgroundColor: Colors.green[800],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Padding(
              padding: EdgeInsets.fromLTRB(80, 20, 80, 0),
              child: Image(
                image: AssetImage('images/b4b.png'),
              ),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(10, 40, 80, 0),
              child: Text(
                'Sign in to your account',
                style: TextStyle(color: Colors.black, fontSize: 40),
              ),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(8, 20, 30, 0),
              child: TextFormField(
                onChanged: (val) {
                  setState(() {
                    email = val;
                  });
                },
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'username',
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(8, 20, 30, 0),
              child: TextFormField(
                obscureText: true,
                onChanged: (val) {
                  setState(() {
                    password = val;
                  });
                },
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'password',
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 50.0),
              child: ElevatedButton(
                  child: Text('Sign in'),
                  style: ElevatedButton.styleFrom(primary: Colors.green[800]),
                  onPressed: email != ''
                      ? () async {
                          username = email;
                          dynamic result = await _auth
                              .signInWithEmailAndPassword(email, password);
                          if (result == null) {
                            print('error signing in');
                          } else {
                            unique_identification = result.uid;
                          }
                        }
                      : null),
            ),
            Padding(
              padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 50.0),
              child: TextButton(
                  child: Text('Register'),
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (context) => const Register()),
                    );
                  }),
            ),
          ],
        ),
      ),
    );
  }
}
