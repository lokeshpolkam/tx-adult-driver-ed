class UserModel {
  final String id;
  final String email;
  final String fullName;
  final String? legalFirstName;
  final String? legalLastName;
  final String role;
  final String enrollmentStatus; // 'ACTIVE', 'UNPAID', 'COMPLETED'
  final String? profileImage;
  final DateTime? createdAt;

  UserModel({
    required this.id,
    required this.email,
    required this.fullName,
    this.legalFirstName,
    this.legalLastName,
    this.role = 'STUDENT',
    this.enrollmentStatus = 'UNPAID',
    this.profileImage,
    this.createdAt,
  });

  bool get isEnrolled => enrollmentStatus == 'ACTIVE' || enrollmentStatus == 'COMPLETED';

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? '',
      email: json['email'] ?? '',
      fullName: json['fullName'] ?? json['full_name'] ?? 'Texas Student',
      legalFirstName: json['legalFirstName'] ?? json['legal_first_name'],
      legalLastName: json['legalLastName'] ?? json['legal_last_name'],
      role: json['role'] ?? 'STUDENT',
      enrollmentStatus: json['enrollmentStatus'] ?? json['enrollment_status'] ?? 'UNPAID',
      profileImage: json['profileImage'] ?? json['profile_image'],
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at'].toString()) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'fullName': fullName,
      'legalFirstName': legalFirstName,
      'legalLastName': legalLastName,
      'role': role,
      'enrollmentStatus': enrollmentStatus,
      'profileImage': profileImage,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  UserModel copyWith({
    String? id,
    String? email,
    String? fullName,
    String? enrollmentStatus,
    String? profileImage,
  }) {
    return UserModel(
      id: id ?? this.id,
      email: email ?? this.email,
      fullName: fullName ?? this.fullName,
      enrollmentStatus: enrollmentStatus ?? this.enrollmentStatus,
      profileImage: profileImage ?? this.profileImage,
      role: role,
      legalFirstName: legalFirstName,
      legalLastName: legalLastName,
      createdAt: createdAt,
    );
  }
}
