import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:lentera/config/api_config.dart';
import 'package:lentera/models/conversation.dart';

/// AI Service for communicating with VPS backend (Ollama + Llama 3.1)
class AIService {
  /// Send a chat message and get AI response
  Future<String> sendMessage({
    required String userId,
    required String message,
    List<Message>? conversationHistory,
  }) async {
    try {
      // Prepare conversation history
      final history = conversationHistory?.map((msg) => {
            'role': msg.role,
            'content': msg.content,
          }).toList() ?? [];

      // Prepare request body
      final body = jsonEncode({
        'user_id': userId,
        'message': message,
        'conversation_history': history,
      });

      debugPrint('Sending message to: ${ApiConfig.chatEndpoint}');

      // Send request to backend
      final response = await http
          .post(
            Uri.parse(ApiConfig.chatEndpoint),
            headers: ApiConfig.defaultHeaders,
            body: body,
          )
          .timeout(ApiConfig.receiveTimeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] as String;
      } else if (response.statusCode == 500) {
        throw Exception('Server error: ${response.body}');
      } else {
        throw Exception('HTTP ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      debugPrint('AI Service Error: $e');
      rethrow;
    }
  }

  /// Check if backend is healthy
  Future<bool> checkHealth() async {
    try {
      final response = await http
          .get(Uri.parse(ApiConfig.healthEndpoint))
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['status'] == 'ok' || data['status'] == 'degraded';
      }
      return false;
    } catch (e) {
      debugPrint('Health check failed: $e');
      return false;
    }
  }

  /// Process audio input (if backend supports it)
  Future<Map<String, dynamic>> processAudio({
    required String userId,
    required String audioPath,
  }) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse(ApiConfig.audioEndpoint),
      );

      request.fields['user_id'] = userId;
      request.files.add(await http.MultipartFile.fromPath('audio', audioPath));

      final streamedResponse =
          await request.send().timeout(const Duration(seconds: 60));
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('Audio processing failed: ${response.body}');
      }
    } catch (e) {
      debugPrint('Audio processing error: $e');
      rethrow;
    }
  }
}
