/// Texas Adult Driver Education (TDLR Approved ADE-1317, School #C3284)
/// Global Constants and Configuration
class AppConstants {
  // Cloud Run Production API Base URL
  static const String apiBaseUrl = 'https://tx-ade-api-1004296326114.us-central1.run.app';

  // Google OAuth 2.0 Client ID
  static const String googleClientId = '1004296326114-dq4t23m4evubp6jv6jovjd955ju808jc.apps.googleusercontent.com';

  // Statutory Certification Information
  static const String courseTitle = 'Texas Adult Driver Education';
  static const String courseCode = 'ADE-1317';
  static const String schoolLicense = 'C3284';
  static const String statuteCitation = '16 TAC § 84.500';

  // Statutory Timer and Assessment Rules
  static const int requiredTotalHours = 6;
  static const int requiredTotalMinutes = 360;
  static const double passingGradePercent = 70.0;
  static const int pvqTimeoutSeconds = 90;
  static const int heartbeatIntervalSeconds = 30;

  // Pricing & Promotional Codes
  static const double regularPrice = 39.00;
  static const String adminPromoCode = 'TEXAS100';
  static const List<String> valid100PercentPromoCodes = [
    'TEXAS100',
    'FREE100',
    'TEXASVIP',
    'TDLRADMIN',
  ];

  // Storage Keys
  static const String keyUserSession = 'tx_ade_session_token';
  static const String keyUserData = 'tx_ade_user_data';
  static const String keyActiveTopic = 'tx_ade_active_topic';
  static const String keyCompletedTopics = 'tx_ade_completed_topics';
  static const String keyTotalStudySeconds = 'tx_ade_study_seconds';
  static const String keyIsUnlocked = 'tx_ade_is_unlocked';
}
