import 'package:flutter/material.dart';
import '../../config/theme.dart';
import '../../models/curriculum_model.dart';

class QuizSheet extends StatefulWidget {
  final CourseTopic topic;
  final VoidCallback onPassed;

  const QuizSheet({super.key, required this.topic, required this.onPassed});

  static Future<bool?> show(BuildContext context, {required CourseTopic topic, required VoidCallback onPassed}) {
    return showModalBottomSheet<bool>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => QuizSheet(topic: topic, onPassed: onPassed),
    );
  }

  @override
  State<QuizSheet> createState() => _QuizSheetState();
}

class _QuizSheetState extends State<QuizSheet> {
  int _currentIndex = 0;
  int? _selectedOption;
  bool _hasSubmitted = false;
  int _score = 0;

  late final List<QuizQuestion> _questions;

  @override
  void initState() {
    super.initState();
    // Default interactive questions for the active topic
    _questions = [
      QuizQuestion(
        id: '${widget.topic.id}-Q1',
        topicId: widget.topic.id,
        number: 1,
        prompt: 'Under Texas Transportation Code § 545.051, what is the default driving standard on all public roadways?',
        options: [
          QuizOption(number: 1, text: 'Drive on the left half of the roadway at all times'),
          QuizOption(number: 2, text: 'An operator on a roadway of sufficient width shall drive on the right half of the roadway'),
          QuizOption(number: 3, text: 'Straddle both lanes when driving below posted speed limit'),
          QuizOption(number: 4, text: 'Drive on the shoulder during heavy traffic'),
        ],
        correctOptionNumber: 2,
        explanation: 'TX TRANS CODE § 545.051 mandates driving on the right half of the roadway unless passing or avoiding an obstruction.',
        statute: 'TX TRANS CODE § 545.051',
      ),
      QuizQuestion(
        id: '${widget.topic.id}-Q2',
        topicId: widget.topic.id,
        number: 2,
        prompt: 'What is the minimum passing score required by TDLR regulations (16 TAC § 84.500) for course mastery?',
        options: [
          QuizOption(number: 1, text: '50% Correct'),
          QuizOption(number: 2, text: '60% Correct'),
          QuizOption(number: 3, text: '70% Correct'),
          QuizOption(number: 4, text: '85% Correct'),
        ],
        correctOptionNumber: 3,
        explanation: 'TDLR statutory rules mandate a minimum score of 70% or higher to receive official certification.',
        statute: '16 TAC § 84.500',
      ),
    ];
  }

  void _checkAnswer() {
    if (_selectedOption == null) return;
    setState(() {
      _hasSubmitted = true;
      if (_selectedOption == _questions[_currentIndex].correctOptionNumber) {
        _score++;
      }
    });
  }

  void _nextQuestion() {
    if (_currentIndex < _questions.length - 1) {
      setState(() {
        _currentIndex++;
        _selectedOption = null;
        _hasSubmitted = false;
      });
    } else {
      _finishQuiz();
    }
  }

  void _finishQuiz() {
    final percent = (_score / _questions.length) * 100;
    final passed = percent >= 70.0;

    if (passed) {
      widget.onPassed();
      Navigator.of(context).pop(true);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppTheme.primary,
          content: Text('✓ Mastery achieved ($percent%)! Topic verified and completed.'),
        ),
      );
    } else {
      Navigator.of(context).pop(false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: AppTheme.danger,
          content: Text('Score: $percent%. 70% required. Please review material and try again.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentQ = _questions[_currentIndex];

    return Container(
      padding: EdgeInsets.only(
        left: 20,
        right: 20,
        top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      decoration: const BoxDecoration(
        color: AppTheme.surface,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
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
                    child: const Icon(Icons.quiz_outlined, color: AppTheme.primary, size: 20),
                  ),
                  const SizedBox(width: 10),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Topic Assessment', style: Theme.of(context).textTheme.titleLarge),
                      Text(
                        'Question ${_currentIndex + 1} of ${_questions.length} · 70% to Pass',
                        style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary),
                      ),
                    ],
                  ),
                ],
              ),
              IconButton(
                icon: const Icon(Icons.close, color: AppTheme.textMuted),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ],
          ),
          const SizedBox(height: 16),
          LinearProgressIndicator(
            value: (_currentIndex + 1) / _questions.length,
            backgroundColor: AppTheme.surfaceBorder,
            valueColor: const AlwaysStoppedAnimation(AppTheme.primary),
            minHeight: 6,
            borderRadius: BorderRadius.circular(4),
          ),
          const SizedBox(height: 16),
          Text(
            currentQ.prompt,
            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: AppTheme.textPrimary, height: 1.4),
          ),
          const SizedBox(height: 16),
          ...currentQ.options.map((opt) {
            final isSelected = _selectedOption == opt.number;
            Color borderC = AppTheme.surfaceBorder;
            Color bgC = AppTheme.surfaceElevated;

            if (_hasSubmitted) {
              if (opt.number == currentQ.correctOptionNumber) {
                borderC = AppTheme.primary;
                bgC = AppTheme.primary.withOpacity(0.15);
              } else if (isSelected) {
                borderC = AppTheme.danger;
                bgC = AppTheme.danger.withOpacity(0.15);
              }
            } else if (isSelected) {
              borderC = AppTheme.primary;
              bgC = AppTheme.primary.withOpacity(0.1);
            }

            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: InkWell(
                onTap: _hasSubmitted ? null : () => setState(() => _selectedOption = opt.number),
                borderRadius: BorderRadius.circular(10),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  decoration: BoxDecoration(
                    color: bgC,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: borderC, width: 1.5),
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 12,
                        backgroundColor: borderC.withOpacity(0.2),
                        child: Text(
                          '${opt.number}',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: borderC == AppTheme.surfaceBorder ? AppTheme.textSecondary : borderC,
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          opt.text,
                          style: const TextStyle(fontSize: 13, color: AppTheme.textPrimary),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            );
          }),
          if (_hasSubmitted) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppTheme.surfaceElevated,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.surfaceBorder),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        _selectedOption == currentQ.correctOptionNumber ? Icons.check_circle : Icons.cancel,
                        color: _selectedOption == currentQ.correctOptionNumber ? AppTheme.primary : AppTheme.danger,
                        size: 16,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        _selectedOption == currentQ.correctOptionNumber ? 'Correct!' : 'Incorrect',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: _selectedOption == currentQ.correctOptionNumber ? AppTheme.primary : AppTheme.danger,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(
                    currentQ.explanation,
                    style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary),
                  ),
                ],
              ),
            ),
          ],
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _selectedOption == null
                ? null
                : _hasSubmitted
                    ? _nextQuestion
                    : _checkAnswer,
            child: Text(
              _hasSubmitted
                  ? (_currentIndex < _questions.length - 1 ? 'NEXT QUESTION' : 'COMPLETE ASSESSMENT')
                  : 'SUBMIT ANSWER',
            ),
          ),
        ],
      ),
    );
  }
}
