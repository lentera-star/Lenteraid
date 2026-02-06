import 'package:flutter/foundation.dart';
import 'package:lentera/services/api_client.dart';
import 'package:lentera/services/mood_service.dart';

class QuizService {
  final _apiClient = ApiClient();
  final _moodService = MoodService();

  /// Generate personalized quiz based on user's mood (daily or recent history)
  Future<List<Map<String, dynamic>>> generateQuiz({
    required String userId,
    int dayRange = 1,  // Changed to 1 day for daily generation
    int questionCount = 3,
  }) async {
    try {
      // Fetch mood history - try today first, fallback to recent if empty
      final now = DateTime.now();
      final start = now.subtract(Duration(days: dayRange));
      final moodHistory = await _moodService.getMoodEntriesBetween(
        userId,
        start: start,
        end: now,
      );

      debugPrint('[QuizService] Fetched ${moodHistory.length} mood entries for today');

      // ALWAYS call AI generation - it will handle empty history gracefully
      final result = await _apiClient.generatePersonalizedQuiz(
        userId: userId,
        moodHistory: moodHistory.map((e) => e.toJson()).toList(),
        count: questionCount,
      );

      final questions = result['questions'] as List<dynamic>;
      final isPersonalized = result['personalized'] ?? false;

      debugPrint('[QuizService] Generated ${questions.length} questions (personalized: $isPersonalized)');

      return questions.map((q) => q as Map<String, dynamic>).toList();
    } catch (e) {
      debugPrint('[QuizService] Error generating quiz: $e');
      // Fallback to static questions only on error
      return _getStaticQuestions();
    }
  }

  List<Map<String, dynamic>> _getStaticQuestions() {
    return [
      {
        'question': 'Berapa lama waktu tidur yang ideal untuk orang dewasa?',
        'options': ['5-6 jam', '7-9 jam', '10-12 jam', '4-5 jam'],
        'correctAnswer': '7-9 jam',
        'explanation': 'Orang dewasa membutuhkan 7-9 jam tidur per malam untuk kesehatan optimal.',
      },
      {
        'question': 'Apa yang dimaksud dengan mindfulness?',
        'options': [
          'Berpikir tentang masa lalu',
          'Fokus pada saat ini',
          'Merencanakan masa depan',
          'Multitasking'
        ],
        'correctAnswer': 'Fokus pada saat ini',
        'explanation': 'Mindfulness adalah praktik untuk fokus pada momen saat ini tanpa judgment.',
      },
      {
        'question': 'Aktivitas fisik yang disarankan per minggu adalah?',
        'options': ['30 menit', '75 menit', '150 menit', '300 menit'],
        'correctAnswer': '150 menit',
        'explanation': 'WHO merekomendasikan 150 menit aktivitas fisik intensitas sedang per minggu.',
      },
    ];
  }
}
