import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../config/constants.dart';
import '../../providers/auth_provider.dart';
import '../../providers/course_provider.dart';
import '../common/responsive_builder.dart';
import '../classroom/classroom_screen.dart';
import '../dialogs/coupon_dialog.dart';
import '../dialogs/signin_sheet.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    final authProvider = context.watch<AuthProvider>();
    final courseProvider = context.watch<CourseProvider>();
    final isEnrolled = authProvider.isEnrolled || courseProvider.progress.isCourseUnlocked;

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: AppTheme.secondary.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.drive_eta, color: AppTheme.secondary, size: 20),
            ),
            const SizedBox(width: 10),
            const Text(
              'TEXAS ADE',
              style: TextStyle(fontWeight: FontWeight.w900, letterSpacing: 1.2, fontSize: 16),
            ),
          ],
        ),
        actions: [
          if (authProvider.isAuthenticated)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Center(
                child: Chip(
                  avatar: const Icon(Icons.check_circle, color: AppTheme.primary, size: 16),
                  label: Text(
                    authProvider.currentUser?.fullName ?? 'Student',
                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                  ),
                  backgroundColor: AppTheme.surfaceElevated,
                  visualDensity: VisualDensity.compact,
                ),
              ),
            )
          else
            TextButton(
              onPressed: () => SignInSheet.show(context),
              child: const Text('SIGN IN', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
            ),
        ],
      ),
      body: ResponsiveBuilder(
        builder: (context, constraints, deviceType) {
          final isPhone = deviceType == DeviceType.mobile;

          return SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: isPhone ? 16.0 : 40.0,
              vertical: 20.0,
            ),
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1000),
                child: Column(
                  children: [
                    // TDLR Official State Banner
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                      decoration: BoxDecoration(
                        color: AppTheme.surfaceElevated,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.surfaceBorder),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: const [
                          Icon(Icons.verified, color: AppTheme.primary, size: 18),
                          SizedBox(width: 8),
                          Flexible(
                            child: Text(
                              'STATE OF TEXAS APPROVED · TDLR LICENSE #C3284 · COURSE ADE-1317',
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.primaryLight,
                                letterSpacing: 0.5,
                              ),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Hero Section
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(isPhone ? 24.0 : 40.0),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [
                            Color(0xFF131D33),
                            Color(0xFF0F172A),
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(color: AppTheme.surfaceBorder),
                        boxShadow: [
                          BoxShadow(
                            color: AppTheme.secondary.withOpacity(0.08),
                            blurRadius: 30,
                            offset: const Offset(0, 10),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: AppTheme.primary.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: const Text(
                              '✓ 100% ONLINE · NO IN-PERSON CLASSROOM NEEDED',
                              style: TextStyle(
                                color: AppTheme.primary,
                                fontSize: 11,
                                fontWeight: FontWeight.w800,
                                letterSpacing: 0.5,
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Texas Adult Driver Education',
                            style: isPhone
                                ? Theme.of(context).textTheme.headlineLarge
                                : const TextStyle(fontSize: 36, fontWeight: FontWeight.w900, color: Colors.white),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            'Complete the state-mandated 6-hour driver education course on your phone, tablet, or computer. Valid for Texas Driver License applicants aged 18–24 and recommended for all adults.',
                            style: TextStyle(
                              color: AppTheme.textSecondary,
                              fontSize: 15,
                              height: 1.5,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 28),

                          // CTA Buttons
                          Wrap(
                            spacing: 16,
                            runSpacing: 12,
                            alignment: WrapAlignment.center,
                            children: [
                              SizedBox(
                                width: isPhone ? double.infinity : 260,
                                child: ElevatedButton.icon(
                                  onPressed: () {
                                    Navigator.of(context).push(
                                      MaterialPageRoute(builder: (_) => const ClassroomScreen()),
                                    );
                                  },
                                  icon: const Icon(Icons.play_arrow_rounded, size: 22),
                                  label: Text(
                                    isEnrolled ? 'CONTINUE COURSE' : 'START MODULE 1 (FREE)',
                                    style: const TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                ),
                              ),
                              SizedBox(
                                width: isPhone ? double.infinity : 240,
                                child: OutlinedButton.icon(
                                  onPressed: () => CouponDialog.show(context),
                                  icon: const Icon(Icons.vpn_key_rounded, size: 18),
                                  label: const Text('ENTER PROMO CODE'),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Admin Promo Highlight Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: AppTheme.surface,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppTheme.secondary.withOpacity(0.4)),
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: AppTheme.secondary.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: const Icon(Icons.stars, color: AppTheme.secondary, size: 28),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  '100% OFF Promotional Code Active',
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.textPrimary),
                                ),
                                const SizedBox(height: 4),
                                RichText(
                                  text: const TextSpan(
                                    style: TextStyle(fontSize: 12, color: AppTheme.textSecondary),
                                    children: [
                                      TextSpan(text: 'Use admin code '),
                                      TextSpan(
                                        text: 'TEXAS100',
                                        style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryLight),
                                      ),
                                      TextSpan(text: ' at checkout or in the promo dialog to unlock all 9 modules for \$0!'),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 8),
                          TextButton(
                            onPressed: () => CouponDialog.show(context),
                            child: const Text('REDEEM', style: TextStyle(fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 28),

                    // Feature Grid (Phone Responsive)
                    GridView.count(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      crossAxisCount: isPhone ? 1 : 3,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                      childAspectRatio: isPhone ? 3.0 : 1.3,
                      children: [
                        _buildFeatureCard(
                          context,
                          icon: Icons.phone_android,
                          title: 'Mobile & Phone Ready',
                          description: 'Optimized touch UI, responsive syllabus drawer, and statutory timers on any device.',
                        ),
                        _buildFeatureCard(
                          context,
                          icon: Icons.assignment_turned_in_outlined,
                          title: 'DPS Exam Exemption',
                          description: 'Passing our final exam waives the written knowledge test at the Texas DPS office.',
                        ),
                        _buildFeatureCard(
                          context,
                          icon: Icons.cloud_done_outlined,
                          title: 'Cloud State Sync',
                          description: 'Progress backed up to Google Cloud Run in real-time. Pick up right where you left off.',
                        ),
                      ],
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

  Widget _buildFeatureCard(BuildContext context, {required IconData icon, required String title, required String description}) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppTheme.surface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.surfaceBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: AppTheme.primary, size: 24),
          const SizedBox(height: 10),
          Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppTheme.textPrimary)),
          const SizedBox(height: 6),
          Text(description, style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary, height: 1.4)),
        ],
      ),
    );
  }
}
