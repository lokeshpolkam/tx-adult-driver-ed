class StudentProgress {
  final Set<String> completedTopicIds;
  final String activeTopicId;
  final int totalStudySeconds;
  final bool isCourseUnlocked;
  final int pvqAnsweredCount;

  StudentProgress({
    required this.completedTopicIds,
    required this.activeTopicId,
    required this.totalStudySeconds,
    required this.isCourseUnlocked,
    this.pvqAnsweredCount = 0,
  });

  factory StudentProgress.initial() {
    return StudentProgress(
      completedTopicIds: {},
      activeTopicId: 'L01-T01',
      totalStudySeconds: 0,
      isCourseUnlocked: false,
      pvqAnsweredCount: 0,
    );
  }

  double getProgressPercent(int totalTopics) {
    if (totalTopics <= 0) return 0.0;
    return (completedTopicIds.length / totalTopics).clamp(0.0, 1.0);
  }

  bool isTopicCompleted(String topicId) => completedTopicIds.contains(topicId);

  StudentProgress copyWith({
    Set<String>? completedTopicIds,
    String? activeTopicId,
    int? totalStudySeconds,
    bool? isCourseUnlocked,
    int? pvqAnsweredCount,
  }) {
    return StudentProgress(
      completedTopicIds: completedTopicIds ?? this.completedTopicIds,
      activeTopicId: activeTopicId ?? this.activeTopicId,
      totalStudySeconds: totalStudySeconds ?? this.totalStudySeconds,
      isCourseUnlocked: isCourseUnlocked ?? this.isCourseUnlocked,
      pvqAnsweredCount: pvqAnsweredCount ?? this.pvqAnsweredCount,
    );
  }
}
