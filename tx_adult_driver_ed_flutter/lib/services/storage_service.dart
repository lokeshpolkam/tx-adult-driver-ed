import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/constants.dart';
import '../models/user_model.dart';

class StorageService {
  static SharedPreferences? _prefs;

  static Future<void> init() async {
    _prefs ??= await SharedPreferences.getInstance();
  }

  // Session Token
  static Future<void> saveToken(String token) async {
    await _prefs?.setString(AppConstants.keyUserSession, token);
  }

  static String? getToken() {
    return _prefs?.getString(AppConstants.keyUserSession);
  }

  static Future<void> clearSession() async {
    await _prefs?.remove(AppConstants.keyUserSession);
    await _prefs?.remove(AppConstants.keyUserData);
  }

  // User Profile
  static Future<void> saveUser(UserModel user) async {
    final raw = jsonEncode(user.toJson());
    await _prefs?.setString(AppConstants.keyUserData, raw);
  }

  static UserModel? getUser() {
    final raw = _prefs?.getString(AppConstants.keyUserData);
    if (raw == null) return null;
    try {
      final map = jsonDecode(raw);
      return UserModel.fromJson(map);
    } catch (_) {
      return null;
    }
  }

  // Active Topic
  static Future<void> saveActiveTopic(String topicId) async {
    await _prefs?.setString(AppConstants.keyActiveTopic, topicId);
  }

  static String getActiveTopic() {
    return _prefs?.getString(AppConstants.keyActiveTopic) ?? 'L01-T01';
  }

  // Completed Topics
  static Future<void> saveCompletedTopics(Set<String> topics) async {
    await _prefs?.setStringList(AppConstants.keyCompletedTopics, topics.toList());
  }

  static Set<String> getCompletedTopics() {
    final list = _prefs?.getStringList(AppConstants.keyCompletedTopics) ?? [];
    return list.toSet();
  }

  // Total Study Seconds
  static Future<void> saveStudySeconds(int seconds) async {
    await _prefs?.setInt(AppConstants.keyTotalStudySeconds, seconds);
  }

  static int getStudySeconds() {
    return _prefs?.getInt(AppConstants.keyTotalStudySeconds) ?? 0;
  }

  // Course Unlock Status (100% Promo Code or Payment)
  static Future<void> setUnlocked(bool unlocked) async {
    await _prefs?.setBool(AppConstants.keyIsUnlocked, unlocked);
  }

  static bool isUnlocked() {
    return _prefs?.getBool(AppConstants.keyIsUnlocked) ?? false;
  }
}
