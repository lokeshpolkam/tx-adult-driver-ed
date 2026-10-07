import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../config/constants.dart';
import '../../providers/auth_provider.dart';
import '../../providers/course_provider.dart';
import '../common/responsive_builder.dart';
import '../dialogs/signin_sheet.dart';
import '../dialogs/coupon_dialog.dart';
import '../dialogs/pvq_dialog.dart';
import '../quiz/quiz_view.dart';
import 'curriculum_drawer.dart';

class ClassroomScreen extends StatefulWidget {
  const ClassroomScreen({super.key});

  @override
  State<ClassroomScreen> createState() => _ClassroomScreenState();
}

class _ClassroomScreenState extends State<ClassroomScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkAuthAndStart();
    });
  }

  Future<void> _checkAuthAndStart() async {
    final authProvider = context.read<AuthProvider>();
    final courseProvider = context.read<CourseProvider>();

    if (!authProvider.isAuthenticated) {
      final signedIn = await SignInSheet.show(context);
      if (signedIn != true) return;
    }

    courseProvider.startTimer();
  }

  String _formatTime(int totalSeconds) {
    final minutes = totalSeconds ~/ 60;
    final seconds = totalSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final courseProvider = context.watch<CourseProvider>();
    final authProvider = context.watch<AuthProvider>();
    final currentTopic = courseProvider.currentTopic;
    final currentModule = courseProvider.currentModule;
    final isEnrolled = authProvider.isEnrolled || courseProvider.progress.isCourseUnlocked;

    if (courseProvider.isLoadingCurriculum) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(color: AppTheme.primary),
        ),
      );
    }

    return Scaffold(
      key: _scaffoldKey,
      drawer: const CurriculumDrawer(),
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () => _scaffoldKey.currentState?.openDrawer(),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(
                  currentModule?.code ?? 'MOD 01',
                  style: const TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.secondary,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: AppTheme.primary.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    currentTopic?.id ?? 'L01-T01',
                    style: const TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryLight,
                    ),
                  ),
                ),
              ],
            ),
            Text(
              currentTopic?.title ?? 'Classroom Player',
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
        actions: [
          // Statutory 16 TAC § 84.500 Countdown Timer Badge
          Container(
            margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: AppTheme.surfaceElevated,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppTheme.surfaceBorder),
            ),
            child: Row(
              children: [
                const Icon(Icons.timer_outlined, size: 14, color: AppTheme.primary),
                const SizedBox(width: 6),
                Text(
                  _formatTime(courseProvider.activeTopicRemainingSeconds),
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'monospace',
                    color: AppTheme.textPrimary,
                  ),
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.shield_outlined, size: 20),
            tooltip: 'Trigger PVQ Challenge',
            onPressed: () {
              PVQDialog.show(
                context,
                onCompleted: (isOk) => courseProvider.dismissPVQChallenge(isOk),
              );
            },
          ),
        ],
      ),
      body: ResponsiveBuilder(
        builder: (context, constraints, deviceType) {
          final isPhone = deviceType == DeviceType.mobile;

          return SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: isPhone ? 16.0 : 32.0,
              vertical: 16.0,
            ),
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 900),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Official TDLR Accreditation Strip
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                      decoration: BoxDecoration(
                        color: AppTheme.surface,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.surfaceBorder),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.verified, color: AppTheme.primary, size: 18),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              'TDLR ADE-1317 · School #C3284 · 16 TAC § 84.500 Statutory Session Active',
                              style: const TextStyle(fontSize: 11, color: AppTheme.textSecondary),
                            ),
                          ),
                          Text(
                            authProvider.currentUser?.fullName ?? 'Student Active',
                            style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppTheme.primaryLight),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Lesson Header Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            AppTheme.surfaceElevated,
                            AppTheme.surface,
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppTheme.surfaceBorder),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Chip(
                                label: Text(currentModule?.title ?? 'Module 01'),
                                backgroundColor: AppTheme.secondary.withOpacity(0.15),
                                labelStyle: const TextStyle(color: AppTheme.secondary, fontSize: 11, fontWeight: FontWeight.bold),
                                visualDensity: VisualDensity.compact,
                              ),
                              const Spacer(),
                              Text(
                                '${currentTopic?.minutes ?? 10} Minutes Required',
                                style: const TextStyle(color: AppTheme.textMuted, fontSize: 12),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Text(
                            currentTopic?.title ?? 'Topic Introduction',
                            style: Theme.of(context).textTheme.headlineMedium,
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            'Texas Transportation Code statutory requirements mandate comprehension of safe roadway operating procedures, defensive driving maneuvers, and legal compliance.',
                            style: TextStyle(color: AppTheme.textSecondary, height: 1.5, fontSize: 14),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Topic Educational Content Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: AppTheme.surface,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppTheme.surfaceBorder),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: const [
                              Icon(Icons.menu_book_outlined, color: AppTheme.primary, size: 20),
                              SizedBox(width: 10),
                              Text(
                                'Core Learning Objectives',
                                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.textPrimary),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          _buildBulletPoint(
                            context,
                            title: 'Statutory Authority & Right-of-Way',
                            description: 'Understand the legal hierarchy at uncontrolled and four-way stop intersections under TX Trans Code § 545.',
                          ),
                          _buildBulletPoint(
                            context,
                            title: 'Defensive Observation & Scan Patterns',
                            description: 'Maintain a 12-to-15 second visual lead time to identify hazards before they enter vehicle braking zones.',
                          ),
                          _buildBulletPoint(
                            context,
                            title: 'Zero Tolerance & Statutory Compliance',
                            description: 'Comply with Texas Administrative Code guidelines to maintain legal driving status and vehicle insurance verification.',
                          ),
                          const SizedBox(height: 20),

                          // Visual Scenario Card
                          Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: AppTheme.surfaceElevated,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: AppTheme.surfaceBorder),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: const [
                                    Icon(Icons.directions_car, color: AppTheme.secondary, size: 18),
                                    SizedBox(width: 8),
                                    Text(
                                      'Roadway Scenario Focus',
                                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppTheme.textPrimary),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                const Text(
                                  'When approaching a yellow flashing arrow or an emergency vehicle on the shoulder, Texas "Move Over / Slow Down" statutes require moving out of the adjacent lane or dropping vehicle speed to 20 MPH below the posted limit.',
                                  style: TextStyle(fontSize: 13, color: AppTheme.textSecondary, height: 1.4),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Mobile-Optimized Action Bar
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.surfaceElevated,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppTheme.surfaceBorder),
                      ),
                      child: Column(
                        children: [
                          Row(
                            children: [
                              Icon(
                                courseProvider.progress.isTopicCompleted(currentTopic?.id ?? '')
                                    ? Icons.check_circle
                                    : Icons.radio_button_unchecked,
                                color: courseProvider.progress.isTopicCompleted(currentTopic?.id ?? '')
                                    ? AppTheme.primary
                                    : AppTheme.textMuted,
                              ),
                              const SizedBox(width: 10),
                              Expanded(
                                child: Text(
                                  courseProvider.progress.isTopicCompleted(currentTopic?.id ?? '')
                                      ? 'Topic Mastered & Verified'
                                      : 'Complete Quiz to Validate Topic',
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 16),
                          Row(
                            children: [
                              Expanded(
                                child: OutlinedButton.icon(
                                  onPressed: () => _scaffoldKey.currentState?.openDrawer(),
                                  icon: const Icon(Icons.list_alt, size: 18),
                                  label: const Text('SYLLABUS'),
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                flex: 2,
                                child: ElevatedButton.icon(
                                  onPressed: () {
                                    if (currentTopic != null) {
                                      QuizSheet.show(
                                        context,
                                        topic: currentTopic,
                                        onPassed: () => courseProvider.completeCurrentTopic(),
                                      );
                                    }
                                  },
                                  icon: const Icon(Icons.assignment_turned_in, size: 18),
                                  label: const Text('TAKE TOPIC QUIZ'),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 40),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildBulletPoint(BuildContext context, {required String title, required String description}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 4),
            width: 8,
            height: 8,
            decoration: const BoxDecoration(
              color: AppTheme.primary,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: RichText(
              text: TextSpan(
                style: const TextStyle(fontSize: 13, color: AppTheme.textSecondary, height: 1.4),
                children: [
                  TextSpan(
                    text: '$title: ',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.textPrimary),
                  ),
                  TextSpan(text: description),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
