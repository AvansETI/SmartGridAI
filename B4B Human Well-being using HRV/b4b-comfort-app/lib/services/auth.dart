import 'package:brains4buildings/globals.dart';
import 'package:brains4buildings/models/user.dart';
import 'package:brains4buildings/services/database.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  AuthService(){
    _auth
        .authStateChanges()
        .listen((User? user) {
      if (user == null) {
        print('User is currently signed out!');
      }
    });
  }

  // create our user based on firebase user
  OurUser? _userFromFirebaseUser(User user) {
    return user != null ? OurUser(uid: user.uid) : null;
  }

  //auth change user stream
  Stream<OurUser?> get user {
    return _auth
        .authStateChanges()
        .map((User? user) => _userFromFirebaseUser(user!));
  }

  Future registerWithEmailAndPassword(String email, String password) async {
    var credential;
    try {
      credential = await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
    } on FirebaseAuthException catch (e) {
      if (e.code == 'weak-password') {
        print('The password provided is too weak.');
      } else if (e.code == 'email-already-in-use') {
        print('The account already exists for that email.');
      }
    } catch (e) {
      print(e);
    }
    User? user = credential.user;
    return _userFromFirebaseUser(user!);
  }

  Future signInWithEmailAndPassword(String email, String password) async {
    var credential;
    try {
       credential = await FirebaseAuth.instance.signInWithEmailAndPassword(
          email: email,
          password: password
      );
    } on FirebaseAuthException catch (e) {
      if (e.code == 'user-not-found') {
        print('No user found for that email.');
      } else if (e.code == 'wrong-password') {
        print('Wrong password provided for that user.');
      }
    }
    User? user = credential.user;
    return _userFromFirebaseUser(user!);
  }

  //signout
  Future signOut() async {
    try {
      return await _auth.signOut();
    } catch (e) {
      print(e.toString());
      return null;
    }
  }
}
