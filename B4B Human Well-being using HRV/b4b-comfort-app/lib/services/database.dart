import 'package:cloud_firestore/cloud_firestore.dart';

import '../globals.dart';

class DatabaseService {
  final String? uid;
  DatabaseService({this.uid});
  final CollectionReference userPreferences =
      FirebaseFirestore.instance.collection(username.toString());
  int timestamp = DateTime.now().millisecondsSinceEpoch;
  DateTime tsdate = DateTime.fromMillisecondsSinceEpoch(
      DateTime.now().millisecondsSinceEpoch);

  Future updateUserData(
      String user_name,
      int? mood,
      int? modeOfTransport,
      String? location,
      String? durationOfLocation,
      int? thermalComfort,
      int? thermalPreference,
      bool suffocating,
      bool humid,
      bool stuffy,
      bool smelly,
      bool allGood,
      String? eatenRecently,
      int? beverage,
      bool cloth1,
      bool cloth2,
      bool cloth3,
      bool cloth4,
      bool cloth5,
      bool cloth6,
      bool cloth7) async {
    return await userPreferences.doc(timestamp.toString()).set({
      'timestamp': tsdate.year.toString() +
          '/' +
          tsdate.month.toString() +
          '/' +
          tsdate.day.toString() +
          ' ' +
          DateTime.fromMillisecondsSinceEpoch(timestamp).toString(),
      'user_name': username,
      'mood': mood,
      'modeOfTransport': modeOfTransport,
      'location': location,
      'durationOfLocation': durationOfLocation,
      'thermalComfort': thermalComfort,
      'thermalPreference': thermalPreference,
      'suffocating': suffocating,
      'humid': humid,
      'stuffy': stuffy,
      'smelly': smelly,
      'AirQualityallGood': allGood,
      'eatRecent': eatenRecently,
      'beverage': beverage,
      'cloth1': cloth1,
      'cloth2': cloth2,
      'cloth3': cloth3,
      'cloth4': cloth4,
      'cloth5': cloth5,
      'cloth6': cloth6,
      'cloth7': cloth7,
    });
  }

  Future addUserData(
      String username,
      int mood,
      int? modeOfTransport,
      int location,
      String? durationOfLocation,
      int thermalComfort,
      int thermalPreference,
      int airQuality,
      int eatRecent,
      int hotColdRecent,
      int clothing,
      int whyRoom) async {
    return await userPreferences.doc(timestamp.toString()).set({
      'username': username,
      'mood': mood,
      'modeOfTransport': modeOfTransport,
      'location': location,
      'durationOfLocation': durationOfLocation,
      'thermalComfort': thermalComfort,
      'thermalPreference': thermalPreference,
      'airQuality': airQuality,
      'eatRecent': eatRecent,
      'hotColdRecent': hotColdRecent,
      'clothing': clothing,
      'whyRoom': whyRoom,
    });
  }
}
