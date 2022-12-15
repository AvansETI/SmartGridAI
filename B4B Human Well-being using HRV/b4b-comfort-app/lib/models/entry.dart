import 'package:realm/realm.dart';

@RealmModel()
class _Entry {
  @PrimaryKey()
  late final String make;
  late String? model;
  late int? miles;
}
