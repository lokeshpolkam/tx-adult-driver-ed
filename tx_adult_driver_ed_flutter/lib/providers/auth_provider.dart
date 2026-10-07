import 'package:flutter/foundation.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../config/constants.dart';

class AuthProvider extends ChangeNotifier {
  UserModel? _currentUser;
  bool _isLoading = false;
  String? _errorMessage;

  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _currentUser != null;
  String? get errorMessage => _errorMessage;

  bool get isEnrolled =>
      _currentUser?.isEnrolled == true || StorageService.isUnlocked();

  Future<void> initAuth() async {
    _isLoading = true;
    notifyListeners();

    try {
      _currentUser = await ApiService.fetchCurrentUser();
    } catch (_) {
      _currentUser = StorageService.getUser();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Sign in using Google ID Token
  Future<bool> signInWithGoogle(String idToken) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await ApiService.loginWithGoogle(idToken);
    _isLoading = false;

    if (result['success'] == true) {
      if (result['data']?['user'] != null) {
        _currentUser = UserModel.fromJson(result['data']['user']);
      }
      notifyListeners();
      return true;
    } else {
      _errorMessage = result['message'] ?? 'Sign in failed';
      notifyListeners();
      return false;
    }
  }

  /// Demo / Direct login for testing and instant access
  Future<void> loginWithMockUser({String? email, String? name}) async {
    _isLoading = true;
    notifyListeners();

    final mockUser = UserModel(
      id: 'usr_mock_${DateTime.now().millisecondsSinceEpoch}',
      email: email ?? 'student@texasade.org',
      fullName: name ?? 'Texas Driver Student',
      enrollmentStatus: StorageService.isUnlocked() ? 'ACTIVE' : 'UNPAID',
    );

    await StorageService.saveUser(mockUser);
    _currentUser = mockUser;
    _isLoading = false;
    notifyListeners();
  }

  /// Apply 100% discount promo code (TEXAS100)
  Future<Map<String, dynamic>> applyPromoCode(String code) async {
    final cleanCode = code.trim().toUpperCase();
    final res = await ApiService.validateCoupon(cleanCode);

    if (res['valid'] == true && res['isFree'] == true) {
      await StorageService.setUnlocked(true);
      if (_currentUser != null) {
        _currentUser = _currentUser!.copyWith(enrollmentStatus: 'ACTIVE');
        await StorageService.saveUser(_currentUser!);
      }
      notifyListeners();
      return {'success': true, 'message': '100% OFF Code Applied! Course unlocked.'};
    }

    return {'success': false, 'message': res['message'] ?? 'Invalid promo code'};
  }

  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    await ApiService.logout();
    _currentUser = null;
    _isLoading = false;
    notifyListeners();
  }
}
