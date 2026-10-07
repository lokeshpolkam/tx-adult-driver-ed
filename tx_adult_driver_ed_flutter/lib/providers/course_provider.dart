import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import '../models/curriculum_model.dart';
import '../models/progress_model.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../config/constants.dart';

class CourseProvider extends ChangeNotifier {
  List<CourseModule> _modules = [];
  List<CourseTopic> _allTopics = [];
  StudentProgress _progress = StudentProgress.initial();
  
  bool _isLoadingCurriculum = true;
  Timer? _studyTicker;
  Timer? _heartbeatTicker;
  int _activeTopicRemainingSeconds = 0;
  bool _isTimerActive = false;
  bool _isPVQActive = false;

  List<CourseModule> get modules => _modules;
  List<CourseTopic> get allTopics => _allTopics;
  StudentProgress get progress => _progress;
  bool get isLoadingCurriculum => _isLoadingCurriculum;
  int get activeTopicRemainingSeconds => _activeTopicRemainingSeconds;
  bool get isTimerActive => _isTimerActive;
  bool get isPVQActive => _isPVQActive;

  CourseTopic? get currentTopic {
    if (_allTopics.isEmpty) return null;
    return _allTopics.firstWhere(
      (t) => t.id == _progress.activeTopicId,
      orElse: () => _allTopics.first,
    );
  }

  CourseModule? get currentModule {
    final curTopic = currentTopic;
    if (curTopic == null) return null;
    return _modules.firstWhere(
      (m) => m.topics.any((t) => t.id == curTopic.id),
      orElse: () => _modules.first,
    );
  }

  Future<void> loadCurriculum() async {
    _isLoadingCurriculum = true;
    notifyListeners();

    try {
      final jsonString = await rootBundle.loadString('assets/curriculum/curriculum_data.json');
      final data = jsonDecode(jsonString);
      final List<dynamic> rawMods = data['modules'] ?? [];
      
      _modules = rawMods.map((m) => CourseModule.fromJson(m)).toList();
      _allTopics = _modules.flatMap((m) => m.topics).toList();

      // Load saved state
      final savedActive = StorageService.getActiveTopic();
      final savedCompleted = StorageService.getCompletedTopics();
      final savedSeconds = StorageService.getStudySeconds();
      final isUnlocked = StorageService.isUnlocked();

      _progress = StudentProgress(
        completedTopicIds: savedCompleted,
        activeTopicId: savedActive,
        totalStudySeconds: savedSeconds,
        isCourseUnlocked: isUnlocked,
      );

      _resetTopicTimer();
    } catch (e) {
      debugPrint('[CURRICULUM LOAD ERROR] $e');
    } finally {
      _isLoadingCurriculum = false;
      notifyListeners();
    }
  }

  /// Check whether topic is accessible by student
  bool isTopicAccessible(CourseTopic topic, bool isEnrolled) {
    if (isEnrolled || _progress.isCourseUnlocked) return true;
    // Module 1 is free preview
    return topic.isModule1;
  }

  /// Select and navigate to a topic
  void selectTopic(String topicId, bool isEnrolled) {
    final topic = _allTopics.firstWhere((t) => t.id == topicId, orElse: () => _allTopics.first);
    if (!isTopicAccessible(topic, isEnrolled)) {
      return;
    }

    _progress = _progress.copyWith(activeTopicId: topicId);
    StorageService.saveActiveTopic(topicId);
    _resetTopicTimer();
    notifyListeners();
  }

  /// Mark current topic as completed and advance
  void completeCurrentTopic() {
    final current = currentTopic;
    if (current == null) return;

    final newCompleted = Set<String>.from(_progress.completedTopicIds)..add(current.id);
    _progress = _progress.copyWith(completedTopicIds: newCompleted);
    StorageService.saveCompletedTopics(newCompleted);

    // Auto advance to next topic if available
    final currentIndex = _allTopics.indexWhere((t) => t.id == current.id);
    if (currentIndex != -1 && currentIndex < _allTopics.length - 1) {
      final nextTopic = _allTopics[currentIndex + 1];
      _progress = _progress.copyWith(activeTopicId: nextTopic.id);
      StorageService.saveActiveTopic(nextTopic.id);
      _resetTopicTimer();
    }

    notifyListeners();
  }

  /// Reset countdown timer for current topic
  void _resetTopicTimer() {
    final topic = currentTopic;
    if (topic != null) {
      _activeTopicRemainingSeconds = topic.minutes * 60;
    } else {
      _activeTopicRemainingSeconds = 600;
    }
  }

  /// Start statutory 16 TAC § 84.500 timer
  void startTimer() {
    if (_isTimerActive) return;
    _isTimerActive = true;

    _studyTicker?.cancel();
    _studyTicker = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_activeTopicRemainingSeconds > 0) {
        _activeTopicRemainingSeconds--;
      }
      final newSeconds = _progress.totalStudySeconds + 1;
      _progress = _progress.copyWith(totalStudySeconds: newSeconds);

      // Periodic local save every 10s
      if (newSeconds % 10 == 0) {
        StorageService.saveStudySeconds(newSeconds);
      }
      notifyListeners();
    });

    // Send server heartbeat every 30s
    _heartbeatTicker?.cancel();
    _heartbeatTicker = Timer.periodic(
      const Duration(seconds: AppConstants.heartbeatIntervalSeconds),
      (timer) {
        final current = currentTopic;
        if (current != null) {
          ApiService.sendHeartbeat(current.id, _progress.totalStudySeconds);
        }
      },
    );

    notifyListeners();
  }

  /// Pause timer when app is in background or dialog is open
  void pauseTimer() {
    _isTimerActive = false;
    _studyTicker?.cancel();
    _heartbeatTicker?.cancel();
    notifyListeners();
  }

  /// Trigger statutory 90-second PVQ challenge
  void triggerPVQChallenge() {
    pauseTimer();
    _isPVQActive = true;
    notifyListeners();
  }

  /// Submit PVQ answer
  void dismissPVQChallenge(bool wasCorrect) {
    _isPVQActive = false;
    if (wasCorrect) {
      _progress = _progress.copyWith(pvqAnsweredCount: _progress.pvqAnsweredCount + 1);
    }
    startTimer();
    notifyListeners();
  }

  /// Unlock full course via promo code
  void unlockFullCourse() {
    _progress = _progress.copyWith(isCourseUnlocked: true);
    StorageService.setUnlocked(true);
    notifyListeners();
  }

  @override
  void dispose() {
    _studyTicker?.cancel();
    _heartbeatTicker?.cancel();
    super.dispose();
  }
}

extension FlatMapExtension<T> on Iterable<T> {
  Iterable<R> flatMap<R>(Iterable<R> Function(T) f) => expand(f);
}
