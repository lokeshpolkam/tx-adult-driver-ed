import 'dart:async';
import 'package:flutter/material.dart';
import '../../config/theme.dart';
import '../../config/constants.dart';

class PVQDialog extends StatefulWidget {
  final Function(bool isCorrect) onCompleted;

  const PVQDialog({super.key, required this.onCompleted});

  static Future<bool?> show(BuildContext context, {required Function(bool) onCompleted}) {
    return showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (_) => PVQDialog(onCompleted: onCompleted),
    );
  }

  @override
  State<PVQDialog> createState() => _PVQDialogState();
}

class _PVQDialogState extends State<PVQDialog> {
  int _secondsLeft = AppConstants.pvqTimeoutSeconds;
  Timer? _countdownTimer;
  int? _selectedOption;

  final String _prompt = 'To verify your identity per TDLR regulations, please answer the question registered upon enrollment: What was the primary vehicle fuel type discussed in your profile?';
  final List<String> _options = [
    'Electric Vehicle (EV)',
    'Unleaded Gasoline',
    'Diesel Commercial',
    'Biofuel Blend',
  ];
  final int _correctIndex = 1;

  @override
  void initState() {
    super.initState();
    _startCountdown();
  }

  void _startCountdown() {
    _countdownTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_secondsLeft > 0) {
        setState(() => _secondsLeft--);
      } else {
        _countdownTimer?.cancel();
        _handleTimeout();
      }
    });
  }

  void _handleTimeout() {
    widget.onCompleted(false);
    Navigator.of(context).pop(false);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        backgroundColor: AppTheme.danger,
        content: Text('PVQ timed out. Identity challenge failed per 16 TAC § 84.500.'),
      ),
    );
  }

  void _submitAnswer() {
    if (_selectedOption == null) return;
    _countdownTimer?.cancel();
    final isCorrect = _selectedOption == _correctIndex;
    widget.onCompleted(isCorrect);
    Navigator.of(context).pop(isCorrect);

    if (isCorrect) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppTheme.primary,
          content: Text('✓ Identity verified! Classroom unlocked.'),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: AppTheme.danger,
          content: Text('Incorrect identity answer. Verification logged.'),
        ),
      );
    }
  }

  @override
  void dispose() {
    _countdownTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isUrgent = _secondsLeft <= 20;

    return WillPopScope(
      onWillPop: () async => false, // Cannot dismiss without answering
      child: Dialog(
        backgroundColor: Colors.transparent,
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: AppTheme.surface,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: isUrgent ? AppTheme.danger : AppTheme.surfaceBorder,
              width: isUrgent ? 2 : 1,
            ),
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
                          color: AppTheme.danger.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Icon(Icons.shield_outlined, color: AppTheme.danger),
                      ),
                      const SizedBox(width: 12),
                      const Text(
                        'Identity Check',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: AppTheme.textPrimary,
                        ),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      color: isUrgent
                          ? AppTheme.danger.withOpacity(0.2)
                          : AppTheme.surfaceElevated,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: isUrgent ? AppTheme.danger : AppTheme.surfaceBorder,
                      ),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          Icons.timer,
                          size: 14,
                          color: isUrgent ? AppTheme.danger : AppTheme.textSecondary,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          '${_secondsLeft}s',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: isUrgent ? AppTheme.danger : AppTheme.textPrimary,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                _prompt,
                style: const TextStyle(fontSize: 14, color: AppTheme.textPrimary, height: 1.4),
              ),
              const SizedBox(height: 16),
              ...List.generate(_options.length, (index) {
                final isSelected = _selectedOption == index;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    onTap: () => setState(() => _selectedOption = index),
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? AppTheme.primary.withOpacity(0.15)
                            : AppTheme.surfaceElevated,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: isSelected ? AppTheme.primary : AppTheme.surfaceBorder,
                          width: isSelected ? 1.5 : 1,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            isSelected ? Icons.radio_button_checked : Icons.radio_button_off,
                            color: isSelected ? AppTheme.primary : AppTheme.textMuted,
                            size: 18,
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: Text(
                              _options[index],
                              style: TextStyle(
                                fontSize: 13,
                                color: isSelected ? AppTheme.textPrimary : AppTheme.textSecondary,
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              }),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _selectedOption == null ? null : _submitAnswer,
                child: const Text('SUBMIT VERIFICATION'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
