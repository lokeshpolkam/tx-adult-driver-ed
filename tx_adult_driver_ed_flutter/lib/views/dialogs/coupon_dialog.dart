import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../config/constants.dart';
import '../../providers/auth_provider.dart';
import '../../providers/course_provider.dart';

class CouponDialog extends StatefulWidget {
  const CouponDialog({super.key});

  static Future<bool?> show(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 600;
    if (isMobile) {
      return showModalBottomSheet<bool>(
        context: context,
        isScrollControlled: true,
        backgroundColor: Colors.transparent,
        builder: (_) => const CouponDialog(),
      );
    } else {
      return showDialog<bool>(
        context: context,
        builder: (_) => const Dialog(
          backgroundColor: Colors.transparent,
          child: SizedBox(
            width: 480,
            child: CouponDialog(),
          ),
        ),
      );
    }
  }

  @override
  State<CouponDialog> createState() => _CouponDialogState();
}

class _CouponDialogState extends State<CouponDialog> {
  final TextEditingController _codeController = TextEditingController();
  bool _isChecking = false;
  String? _statusMessage;
  bool _isSuccess = false;

  @override
  void dispose() {
    _codeController.dispose();
    super.dispose();
  }

  Future<void> _redeemCode() async {
    final code = _codeController.text.trim();
    if (code.isEmpty) return;

    setState(() {
      _isChecking = true;
      _statusMessage = null;
    });

    final authProvider = context.read<AuthProvider>();
    final courseProvider = context.read<CourseProvider>();

    final res = await authProvider.applyPromoCode(code);
    setState(() {
      _isChecking = false;
      _statusMessage = res['message'];
      _isSuccess = res['success'] == true;
    });

    if (_isSuccess) {
      courseProvider.unlockFullCourse();
      await Future.delayed(const Duration(milliseconds: 1200));
      if (mounted) Navigator.of(context).pop(true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(
        left: 24,
        right: 24,
        top: 24,
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
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
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppTheme.primary.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.confirmation_number_outlined, color: AppTheme.primary),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Redeem Promo Code',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ],
              ),
              IconButton(
                icon: const Icon(Icons.close, color: AppTheme.textMuted),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'Enter an authorized promotional coupon or administrative code to unlock all 9 course modules instantly.',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 16),
          // Quick hint badge for admin promo
          InkWell(
            onTap: () {
              _codeController.text = AppConstants.adminPromoCode;
            },
            borderRadius: BorderRadius.circular(8),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: AppTheme.secondary.withOpacity(0.12),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: AppTheme.secondary.withOpacity(0.3)),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.vpn_key_rounded, size: 16, color: AppTheme.secondary),
                  const SizedBox(width: 8),
                  Text(
                    'Tap to use Admin 100% OFF: ${AppConstants.adminPromoCode}',
                    style: const TextStyle(
                      color: AppTheme.secondary,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _codeController,
            textCapitalization: TextCapitalization.characters,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              letterSpacing: 2,
            ),
            decoration: InputDecoration(
              hintText: 'e.g. TEXAS100',
              prefixIcon: const Icon(Icons.discount_outlined, color: AppTheme.textMuted),
              suffixIcon: _codeController.text.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.clear, size: 18),
                      onPressed: () => setState(() => _codeController.clear()),
                    )
                  : null,
            ),
            onChanged: (_) => setState(() {}),
          ),
          if (_statusMessage != null) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: _isSuccess
                    ? AppTheme.primary.withOpacity(0.15)
                    : AppTheme.danger.withOpacity(0.15),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: _isSuccess ? AppTheme.primary : AppTheme.danger,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    _isSuccess ? Icons.check_circle : Icons.error_outline,
                    color: _isSuccess ? AppTheme.primary : AppTheme.danger,
                    size: 18,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      _statusMessage!,
                      style: TextStyle(
                        color: _isSuccess ? AppTheme.primaryLight : AppTheme.danger,
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _isChecking ? null : _redeemCode,
            child: _isChecking
                ? const SizedBox(
                    height: 20,
                    width: 20,
                    child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2),
                  )
                : const Text('UNLOCK FULL COURSE'),
          ),
        ],
      ),
    );
  }
}
