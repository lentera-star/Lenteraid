import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

/// Configuration for API endpoints
class ApiConfig {
  // VPS IP for production
  static const String vpsIp = '84.247.150.83';
  
  // Backend URL - Uses VPS by default for testing production
  // To use local backend, set BACKEND_URL env var: flutter run --dart-define=USE_LOCAL=true
  static const bool _useLocal = String.fromEnvironment('USE_LOCAL', defaultValue: 'false') == 'true';
  
  static const String backendUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: _useLocal
        ? 'http://localhost:8000'  // Local backend (when USE_LOCAL=true)
        : 'http://$vpsIp:8000',     // VPS backend (port 8000)
  );
  
  static const String wsUrl = String.fromEnvironment(
    'WS_URL',
    defaultValue: _useLocal
        ? 'ws://localhost:8000'     // Local WebSocket
        : 'ws://$vpsIp:8000',       // VPS WebSocket (port 8000)
  );
  
  // API endpoints
  static const String chatEndpoint = '/api/chat';
  static const String moodAnalysisEndpoint = '/api/mood/analyze';
  static const String voiceTranscribeEndpoint = '/api/voice/transcribe';
  static const String voiceSynthesizeEndpoint = '/api/voice/synthesize';
  static const String voiceCallWs = '/ws/voice-call';
  static const String healthEndpoint = '/health';
}

/// API Client for communicating with LENTERA backend
class ApiClient {
  final String baseUrl;
  final http.Client _client;
  
  ApiClient({
    String? baseUrl,
    http.Client? client,
  })  : baseUrl = baseUrl ?? ApiConfig.backendUrl,
        _client = client ?? http.Client();
  
  /// Send chat message to AI backend
  /// 
  /// Sends a chat message to the AI backend.
  /// Uses Supabase Edge Function proxy in production to avoid CORS issues.
  Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String? userId,
    String? conversationId,
  }) async {
    try {
      if (!ApiConfig._useLocal) {
        // Production: Use Supabase Edge Function Proxy
        final response = await Supabase.instance.client.functions.invoke(
          'proxy_ai',
          body: {
            'endpoint': ApiConfig.chatEndpoint,
            'message': message,
            'user_id': userId,
            'conversation_id': conversationId,
          },
        );

        if (response.status != null && response.status! >= 200 && response.status! < 300) {
          return response.data as Map<String, dynamic>;
        } else {
          throw ApiException(
            'Chat proxy request failed with status ${response.status}',
            statusCode: response.status ?? 500,
          );
        }
      } else {
        // Local: Call endpoint directly
        final url = Uri.parse('$baseUrl${ApiConfig.chatEndpoint}');
        final response = await _client.post(
          url,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'message': message,
            'user_id': userId,
            'conversation_id': conversationId,
          }),
        );
        
        if (response.statusCode == 200) {
          return jsonDecode(response.body) as Map<String, dynamic>;
        } else {
          throw ApiException(
            'Chat request failed with status ${response.statusCode}',
            statusCode: response.statusCode,
          );
        }
      }
    } catch (e) {
      debugPrint('Error sending chat message: $e');
      rethrow;
    }
  }
  
  /// Analyze mood entry with AI
  /// 
  /// Returns analysis or throws exception
  Future<Map<String, dynamic>> analyzeMood({
    required int moodRating,
    required List<String> emotions,
    String? journal,
  }) async {
    try {
      if (!ApiConfig._useLocal) {
        // Production: Use Supabase Edge Function Proxy
        final response = await Supabase.instance.client.functions.invoke(
          'proxy_ai',
          body: {
            'endpoint': ApiConfig.moodAnalysisEndpoint,
            'mood_rating': moodRating,
            'emotions': emotions,
            'journal': journal,
          },
        );

        if (response.status != null && response.status! >= 200 && response.status! < 300) {
          return response.data as Map<String, dynamic>;
        } else {
          throw ApiException(
            'Mood analysis proxy request failed with status ${response.status}',
            statusCode: response.status ?? 500,
          );
        }
      } else {
        // Local: Call endpoint directly
        final url = Uri.parse('$baseUrl${ApiConfig.moodAnalysisEndpoint}');
        
        final response = await _client.post(
          url,
          headers: {
            'Content-Type': 'application/json',
          },
          body: jsonEncode({
            'mood_rating': moodRating,
            'emotions': emotions,
            'journal': journal,
          }),
        );
        
        if (response.statusCode == 200) {
          return jsonDecode(response.body) as Map<String, dynamic>;
        } else {
          throw ApiException(
            'Mood analysis failed with status ${response.statusCode}',
            statusCode: response.statusCode,
          );
        }
      }
    } catch (e) {
      debugPrint('Error analyzing mood: $e');
      rethrow;
    }
  }
  
  /// Health check - verify backend is running
  /// 
  /// Returns true if healthy, false otherwise
  Future<bool> healthCheck() async {
    try {
      final url = Uri.parse('$baseUrl${ApiConfig.healthEndpoint}');
      
      final response = await _client.get(url).timeout(
        const Duration(seconds: 5),
      );
      
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
  
  /// Get backend service status
  /// 
  /// Returns service info or null if unavailable
  Future<Map<String, dynamic>?> getServiceStatus() async {
    try {
      final url = Uri.parse('$baseUrl${ApiConfig.healthEndpoint}');
      
      final response = await _client.get(url);
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }
      
      return null;
    } catch (e) {
      debugPrint('Error getting service status: $e');
      return null;
    }
  }
  
  /// Dispose resources
  void dispose() {
    _client.close();
  }
}

/// Custom exception for API errors
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  
  ApiException(this.message, {this.statusCode});
  
  @override
  String toString() => 'ApiException: $message (status: $statusCode)';
}
