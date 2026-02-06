import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:lentera/models/mood_entry.dart';
import 'package:lentera/models/conversation.dart';
import 'package:lentera/config/api_config.dart';
import 'api_client.dart';
export 'api_client.dart' show AiModelMode;

/// AI Service - handles all AI-related operations
/// Communicates with LENTERA backend for chat, mood analysis and voice
class AIService {
  final ApiClient _apiClient;
  
  AIService({ApiClient? apiClient}) 
      : _apiClient = apiClient ?? ApiClient();
  
  /// Send message to AI chatbot
  Future<AIResponse> sendMessage({
    required String message,
    List<Map<String, String>>? history,
    String? userId,
    String? conversationId,
    AiModelMode mode = AiModelMode.smart,
  }) async {
    try {
      final response = await _apiClient.sendChatMessage(
        message: message,
        history: history,
        userId: userId,
        conversationId: conversationId,
        mode: mode,
      );

      return AIResponse.fromJson(response);
    } catch (e) {
      debugPrint('Error in sendMessage: $e');
      rethrow;
    }
  }
  
  /// Analyze mood entry with AI
  Future<MoodAnalysisResponse> analyzeMood(MoodEntry moodEntry) async {
    try {
      final response = await _apiClient.analyzeMood(
        moodRating: moodEntry.moodRating,
        emotions: moodEntry.moodTags,
        journal: moodEntry.journalText,
      );
      
      return MoodAnalysisResponse.fromJson(response);
    } catch (e) {
      debugPrint('Error in analyzeMood: $e');
      rethrow;
    }
  }
  
  /// Check if backend is available
  Future<bool> isBackendAvailable() async {
    return await _apiClient.healthCheck();
  }
  
  /// Get backend service status
  Future<BackendStatus?> getBackendStatus() async {
    try {
      final status = await _apiClient.getServiceStatus();
      if (status != null) {
        return BackendStatus.fromJson(status);
      }
      return null;
    } catch (e) {
      debugPrint('Error getting backend status: $e');
      return null;
    }
  }

  /// Process audio input for real-time voice call
  /// Note: Real-time use is better via WebSocket, but this handles simple audio upload
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
  
  void dispose() {
    _apiClient.dispose();
  }
}

/// AI Response from chat endpoint
class AIResponse {
  final String message;
  final String conversationId;
  final String timestamp;
  final bool isCrisis;
  
  AIResponse({
    required this.message,
    required this.conversationId,
    required this.timestamp,
    this.isCrisis = false,
  });
  
  factory AIResponse.fromJson(Map<String, dynamic> json) {
    // Robust parsing
    String message = json['message'] as String? ?? json['response'] as String? ?? '';
    
    if (message.isEmpty && json['choices'] != null && json['choices'] is List) {
      final choices = json['choices'] as List;
      if (choices.isNotEmpty) {
        final firstChoice = choices[0];
        if (firstChoice['message'] != null && firstChoice['message']['content'] != null) {
          message = firstChoice['message']['content'] as String? ?? '';
        } else if (firstChoice['text'] != null) {
          message = firstChoice['text'] as String? ?? '';
        }
      }
    }

    return AIResponse(
      message: message,
      conversationId: json['conversation_id'] as String? ?? json['id'] as String? ?? '',
      timestamp: json['timestamp'] as String? ?? DateTime.now().toIso8601String(),
      isCrisis: json['is_crisis'] == true || json['is_crisis'] == 'true',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'message': message,
      'conversation_id': conversationId,
      'timestamp': timestamp,
      'is_crisis': isCrisis,
    };
  }
}

/// Mood Analysis Response
class MoodAnalysisResponse {
  final String analysis;
  final int moodScore;
  final String timestamp;
  
  MoodAnalysisResponse({
    required this.analysis,
    required this.moodScore,
    required this.timestamp,
  });
  
  factory MoodAnalysisResponse.fromJson(Map<String, dynamic> json) {
    String analysis = json['analysis'] as String? ?? '';
    
    if (analysis.isEmpty && json['choices'] != null && json['choices'] is List) {
      final choices = json['choices'] as List;
      if (choices.isNotEmpty) {
        final firstChoice = choices[0];
        if (firstChoice['message'] != null && firstChoice['message']['content'] != null) {
          analysis = firstChoice['message']['content'] as String? ?? '';
        } else if (firstChoice['text'] != null) {
          analysis = firstChoice['text'] as String? ?? '';
        }
      }
    }

    return MoodAnalysisResponse(
      analysis: analysis,
      moodScore: json['mood_score'] as int? ?? 3,
      timestamp: json['timestamp'] as String? ?? DateTime.now().toIso8601String(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'analysis': analysis,
      'mood_score': moodScore,
      'timestamp': timestamp,
    };
  }
}

/// Backend Service Status
class BackendStatus {
  final String status;
  final Map<String, String> services;
  final Map<String, dynamic> info;
  
  BackendStatus({
    required this.status,
    required this.services,
    required this.info,
  });
  
  factory BackendStatus.fromJson(Map<String, dynamic> json) {
    return BackendStatus(
      status: json['status'] as String? ?? 'unknown',
      services: Map<String, String>.from(json['services'] ?? {}),
      info: Map<String, dynamic>.from(json['info'] ?? {}),
    );
  }
  
  bool get isHealthy => status == 'ok';
  bool get isDegraded => status == 'degraded';
  
  bool isServiceReady(String serviceName) {
    return services[serviceName] == 'ready';
  }
  
  String get aiMode => info['ai_mode'] as String? ?? 'unknown';
}

}
