class CourseTopic {
  final String id;
  final String title;
  final int minutes;
  final int? moduleId;

  CourseTopic({
    required this.id,
    required this.title,
    required this.minutes,
    this.moduleId,
  });

  bool get isModule1 => id.startsWith('L01-');

  factory CourseTopic.fromJson(Map<String, dynamic> json, {int? moduleId}) {
    return CourseTopic(
      id: json['id'] ?? '',
      title: json['title'] ?? '',
      minutes: json['minutes'] ?? 10,
      moduleId: moduleId ?? json['moduleId'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'minutes': minutes,
      'moduleId': moduleId,
    };
  }
}

class CourseModule {
  final int id;
  final String code;
  final String title;
  final String quizInfo;
  final bool isFreePreview;
  final List<CourseTopic> topics;

  CourseModule({
    required this.id,
    required this.code,
    required this.title,
    required this.quizInfo,
    this.isFreePreview = false,
    required this.topics,
  });

  int get totalMinutes => topics.fold(0, (sum, t) => sum + t.minutes);

  factory CourseModule.fromJson(Map<String, dynamic> json) {
    final int modId = json['id'] ?? 1;
    final List<dynamic> rawTopics = json['topics'] ?? [];
    return CourseModule(
      id: modId,
      code: json['code'] ?? 'MOD $modId',
      title: json['title'] ?? '',
      quizInfo: json['quizInfo'] ?? '10 Q · 70% Pass',
      isFreePreview: json['isFreePreview'] ?? (modId == 1),
      topics: rawTopics.map((t) => CourseTopic.fromJson(t, moduleId: modId)).toList(),
    );
  }
}

class QuizOption {
  final int number;
  final String text;

  QuizOption({required this.number, required this.text});

  factory QuizOption.fromJson(Map<String, dynamic> json) {
    return QuizOption(
      number: json['number'] ?? 0,
      text: json['text'] ?? '',
    );
  }
}

class QuizQuestion {
  final String id;
  final String topicId;
  final int number;
  final String prompt;
  final List<QuizOption> options;
  final int correctOptionNumber;
  final String explanation;
  final String? statute;

  QuizQuestion({
    required this.id,
    required this.topicId,
    required this.number,
    required this.prompt,
    required this.options,
    required this.correctOptionNumber,
    this.explanation = '',
    this.statute,
  });

  factory QuizQuestion.fromJson(Map<String, dynamic> json) {
    final List<dynamic> rawOpts = json['options'] ?? [];
    return QuizQuestion(
      id: json['id'] ?? '',
      topicId: json['topic_id'] ?? json['topicId'] ?? '',
      number: json['number'] ?? 1,
      prompt: json['prompt'] ?? '',
      options: rawOpts.map((o) => QuizOption.fromJson(o)).toList(),
      correctOptionNumber: json['correct_option'] ?? 2,
      explanation: json['explanation'] ?? 'According to Texas Transportation Code regulations.',
      statute: json['statute'],
    );
  }
}
