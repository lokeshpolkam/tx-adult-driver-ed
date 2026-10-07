import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../config/constants.dart';
import '../../providers/auth_provider.dart';

class SignInSheet extends StatefulWidget {
  const SignInSheet({super.key});

  static Future<bool?> show(BuildContext context) {
    return showModalBottomSheet<bool>(
      context: context,
      isDismissible: false,
      enableDrag: false,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (_) => const SignInSheet(),
    );
  }

  @override
  State<SignInSheet> createState() => _SignInSheetState();
}

class _SignInSheetState extends State<SignInSheet> {
  final TextEditingController _emailController = TextEditingController(text: 'student@texasade.org');
  final TextEditingController _nameController = TextEditingController(text: 'Alex Miller');
  bool _isSigningIn = false;

  @override
  void dispose() {
    _emailController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _handleQuickSignIn() async {
    setState(() => _isSigningIn = true);
    final authProvider = context.read<AuthProvider>();

    await authProvider.loginWithMockUser(
      email: _emailController.text.trim(),
      name: _nameController.text.trim(),
    );

    setState(() => _isSigningIn = false);
    if (mounted) Navigator.of(context).pop(true);
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => false, // Mandatory identity verification
      child: Container(
        padding: EdgeInsets.only(
          left: 24,
          right: 24,
          top: 28,
          bottom: MediaQuery.of(context).viewInsets.bottom + 28,
        ),
        decoration: BoxDecoration(
          color: AppTheme.surface,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          border: Border.all(color: AppTheme.surfaceBorder),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: AppTheme.primary.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: const Icon(Icons.verified_user_outlined, color: AppTheme.primary),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Student Identity Registration',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      Text(
                        'TDLR Rule 16 TAC § 84.500 Compliance',
                        style: TextStyle(
                          color: AppTheme.primaryLight.withOpacity(0.9),
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              'Texas state regulations require student identity authentication prior to instruction and clock-hour tracking for official DPS certificate issuance.',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 20),
            // Mock Google SSO Button
            OutlinedButton.icon(
              onPressed: _isSigningIn ? null : _handleQuickSignIn,
              icon: Image.network(
                'https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg',
                height: 20,
                width: 20,
                errorBuilder: (_, __, ___) => const Icon(Icons.account_circle, color: Colors.white),
              ),
              label: const Text('Sign in with Google'),
              style: OutlinedButton.styleFrom(
                backgroundColor: AppTheme.surfaceElevated,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: const [
                Expanded(child: Divider(color: AppTheme.surfaceBorder)),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 12),
                  child: Text('OR TEST SIGN-IN', style: TextStyle(color: AppTheme.textMuted, fontSize: 11)),
                ),
                Expanded(child: Divider(color: AppTheme.surfaceBorder)),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Student Full Name',
                prefixIcon: Icon(Icons.person_outline, color: AppTheme.textMuted),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Student Email',
                prefixIcon: Icon(Icons.email_outlined, color: AppTheme.textMuted),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _isSigningIn ? null : _handleQuickSignIn,
              child: _isSigningIn
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2),
                    )
                  : const Text('ENTER CLASSROOM'),
            ),
          ],
        ),
      ),
    );
  }
}
