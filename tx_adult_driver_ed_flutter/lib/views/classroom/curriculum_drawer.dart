import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../models/curriculum_model.dart';
import '../../providers/auth_provider.dart';
import '../../providers/course_provider.dart';
import '../dialogs/coupon_dialog.dart';

class CurriculumDrawer extends StatelessWidget {
  const CurriculumDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    final courseProvider = context.watch<CourseProvider>();
    final authProvider = context.watch<AuthProvider>();
    final isEnrolled = authProvider.isEnrolled || courseProvider.progress.isCourseUnlocked;

    return Drawer(
      backgroundColor: AppTheme.surface,
      child: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                border: Border(bottom: BorderSide(color: AppTheme.surfaceBorder)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(6),
                            decoration: BoxDecoration(
                              color: AppTheme.primary.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: const Icon(Icons.school, color: AppTheme.primary, size: 20),
                          ),
                          const SizedBox(width: 10),
                          const Text(
                            'Course Syllabus',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppTheme.textPrimary,
                            ),
                          ),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.close, color: AppTheme.textMuted, size: 20),
                        onPressed: () => Navigator.of(context).pop(),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  // Progress indicator
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '${courseProvider.progress.completedTopicIds.length} / ${courseProvider.allTopics.length} Topics Completed',
                        style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary),
                      ),
                      Text(
                        '${(courseProvider.progress.getProgressPercent(courseProvider.allTopics.length) * 100).toInt()}%',
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.primary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  LinearProgressIndicator(
                    value: courseProvider.progress.getProgressPercent(courseProvider.allTopics.length),
                    backgroundColor: AppTheme.surfaceElevated,
                    valueColor: const AlwaysStoppedAnimation(AppTheme.primary),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ],
              ),
            ),

            // Unlock Promo Banner for unpaid users
            if (!isEnrolled)
              Container(
                margin: const EdgeInsets.all(12),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      AppTheme.secondary.withOpacity(0.2),
                      AppTheme.primary.withOpacity(0.1),
                    ],
                  ),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppTheme.secondary.withOpacity(0.4)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.lock_open, color: AppTheme.primary, size: 22),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text(
                            'Module 1 Free Preview',
                            style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.textPrimary),
                          ),
                          Text(
                            'Use code TEXAS100 for 100% off',
                            style: TextStyle(fontSize: 11, color: AppTheme.textSecondary),
                          ),
                        ],
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                        CouponDialog.show(context);
                      },
                      style: TextButton.styleFrom(
                        backgroundColor: AppTheme.primary,
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        minimumSize: Size.zero,
                        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      ),
                      child: const Text('UNLOCK', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),

            // Modules & Topics List
            Expanded(
              child: ListView.builder(
                itemCount: courseProvider.modules.length,
                itemBuilder: (context, modIndex) {
                  final module = courseProvider.modules[modIndex];
                  final isModAccessible = isEnrolled || module.isFreePreview;

                  return ExpansionTile(
                    initiallyExpanded: module.topics.any((t) => t.id == courseProvider.progress.activeTopicId),
                    leading: CircleAvatar(
                      radius: 14,
                      backgroundColor: isModAccessible
                          ? AppTheme.secondary.withOpacity(0.2)
                          : AppTheme.surfaceElevated,
                      child: Text(
                        '${module.id}',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: isModAccessible ? AppTheme.secondary : AppTheme.textMuted,
                        ),
                      ),
                    ),
                    title: Text(
                      module.title,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: isModAccessible ? AppTheme.textPrimary : AppTheme.textMuted,
                      ),
                    ),
                    subtitle: Text(
                      '${module.topics.length} topics · ${module.quizInfo}',
                      style: const TextStyle(fontSize: 11, color: AppTheme.textSecondary),
                    ),
                    trailing: isModAccessible
                        ? null
                        : const Icon(Icons.lock, size: 16, color: AppTheme.danger),
                    children: module.topics.map((topic) {
                      final isActive = topic.id == courseProvider.progress.activeTopicId;
                      final isCompleted = courseProvider.progress.isTopicCompleted(topic.id);
                      final isTopicOpen = courseProvider.isTopicAccessible(topic, isEnrolled);

                      return ListTile(
                        dense: true,
                        contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 0),
                        leading: Icon(
                          isCompleted
                              ? Icons.check_circle
                              : isActive
                                  ? Icons.play_circle_fill
                                  : isTopicOpen
                                      ? Icons.circle_outlined
                                      : Icons.lock_outline,
                          color: isCompleted
                              ? AppTheme.primary
                              : isActive
                                  ? AppTheme.secondary
                                  : isTopicOpen
                                      ? AppTheme.textMuted
                                      : AppTheme.danger,
                          size: 18,
                        ),
                        title: Text(
                          topic.title,
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                            color: isActive
                                ? AppTheme.primaryLight
                                : isTopicOpen
                                    ? AppTheme.textPrimary
                                    : AppTheme.textMuted,
                          ),
                        ),
                        subtitle: Text(
                          '${topic.id} · ${topic.minutes} min',
                          style: const TextStyle(fontSize: 10, color: AppTheme.textSecondary),
                        ),
                        onTap: () {
                          if (isTopicOpen) {
                            courseProvider.selectTopic(topic.id, isEnrolled);
                            Navigator.of(context).pop();
                          } else {
                            CouponDialog.show(context);
                          }
                        },
                      );
                    }).toList(),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
