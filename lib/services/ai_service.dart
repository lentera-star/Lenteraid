import 'package:flutter/foundation.dart';
import 'package:lentera/models/mood_entry.dart';
import 'api_client.dart';

/// AI Service - handles all AI-related operations
/// Communicates with LENTERA backend for chat and mood analysis
class AIService {
  final ApiClient _apiClient;
  
  AIService({ApiClient? apiClient}) 
      : _apiClient = apiClient ?? ApiClient();
  
  /// Send message to AI chatbot
  /// 
  /// Returns AI response text and metadata
  Future<AIResponse> sendMessage({
    required String message,
    String? userId,
    String? conversationId,
  }) async {
    try {
      final response = await _apiClient.sendChatMessage(
        message: message,
        userId: userId,
        conversationId: conversationId,
      );
      
      return AIResponse.fromJson(response);
    } catch (e) {
      debugPrint('Error in sendMessage: $e');
      rethrow;
    }
  }
  
  /// Analyze mood entry with AI
  /// 
  /// Returns AI analysis and insights
  Future<MoodAnalysisResponse> analyzeMood(MoodEntry moodEntry) async {
    try {
      final response = await _apiClient.analyzeMood(
        moodRating: moodEntry.rating,
        emotions: moodEntry.emotions,
        journal: moodEntry.description,
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
    return AIResponse(
      message: json['message'] as String? ?? '',
      conversationId: json['conversation_id'] as String? ?? '',
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
    return MoodAnalysisResponse(
      analysis: json['analysis'] as String? ?? '',
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
