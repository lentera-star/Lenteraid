import 'package:dio/dio.dart';

class ApiService {
  // Base URL - localhost untuk development
  // Untuk Android emulator gunakan 10.0.2.2
  // Untuk iOS simulator gunakan localhost
  static const String baseUrl = 'http://10.0.2.2:8000';
  
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  // Chat endpoint
  Future<Map<String, dynamic>> sendMessage(
    String message,
    List<Map<String, String>> conversationHistory,
  ) async {
    try {
      final response = await _dio.post(
        '/api/chat',
        data: {
          'message': message,
          'conversation_history': conversationHistory,
        },
      );

      return response.data;
    } on DioException catch (e) {
      if (e.response != null) {
        throw Exception('Server error: ${e.response?.statusCode}');
      } else {
        throw Exception('Connection error: ${e.message}');
      }
    }
  }

  // Health check
  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
