import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/constants.dart';
import '../models/user_model.dart';
import 'storage_service.dart';

class ApiService {
  static final String _baseUrl = AppConstants.apiBaseUrl;

  static Map<String, String> _getHeaders() {
    final token = StorageService.getToken();
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (token != null && token.isNotEmpty) {
      headers['Authorization'] = 'Bearer $token';
    }
    return headers;
  }

  /// Verify Google ID Token with Cloud Run backend
  static Future<Map<String, dynamic>> loginWithGoogle(String idToken) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/v1/auth/google'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'id_token': idToken}),
      );

      final data = jsonDecode(response.body);
      if (response.statusCode == 200 && data['success'] == true) {
        if (data['token'] != null) {
          await StorageService.saveToken(data['token']);
        }
        if (data['user'] != null) {
          final user = UserModel.fromJson(data['user']);
          await StorageService.saveUser(user);
        }
        return {'success': true, 'data': data};
      }
      return {'success': false, 'message': data['message'] ?? 'Authentication failed'};
    } catch (e) {
      return {'success': false, 'message': 'Network error: $e'};
    }
  }

  /// Check current user session
  static Future<UserModel?> fetchCurrentUser() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/v1/auth/me'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success'] == true && data['user'] != null) {
          final user = UserModel.fromJson(data['user']);
          await StorageService.saveUser(user);
          return user;
        }
      }
      return null;
    } catch (_) {
      return StorageService.getUser();
    }
  }

  /// Validate promotional code (e.g., TEXAS100)
  static Future<Map<String, dynamic>> validateCoupon(String code) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/v1/billing/validate-coupon'),
        headers: _getHeaders(),
        body: jsonEncode({'code': code}),
      );

      final data = jsonDecode(response.body);
      if (response.statusCode == 200 && data['success'] == true) {
        return {
          'valid': true,
          'discountPercent': data['discountPercent'] ?? 100,
          'isFree': data['isFree'] ?? true,
          'message': data['message'] ?? 'Promo code applied!',
        };
      }
      return {
        'valid': false,
        'message': data['message'] ?? 'Invalid promo code',
      };
    } catch (e) {
      // Local fallback for offline mode or demo
      if (AppConstants.valid100PercentPromoCodes.contains(code.toUpperCase().trim())) {
        return {
          'valid': true,
          'discountPercent': 100,
          'isFree': true,
          'message': '100% OFF Admin Code Verified!',
        };
      }
      return {'valid': false, 'message': 'Network connection error'};
    }
  }

  /// Send 30-second statutory heartbeat to Cloud Run
  static Future<void> sendHeartbeat(String topicId, int elapsedSeconds) async {
    try {
      await http.post(
        Uri.parse('$_baseUrl/api/v1/student/heartbeat'),
        headers: _getHeaders(),
        body: jsonEncode({
          'topicId': topicId,
          'studySeconds': elapsedSeconds,
          'timestamp': DateTime.now().toIso8601String(),
        }),
      );
    } catch (_) {
      // Fail silently for background telemetry
    }
  }

  /// Log out from session
  static Future<void> logout() async {
    try {
      await http.post(
        Uri.parse('$_baseUrl/api/v1/auth/logout'),
        headers: _getHeaders(),
      );
    } catch (_) {}
    await StorageService.clearSession();
  }
}
