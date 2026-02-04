import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

/// Configuration for API endpoints
class ApiConfig {
  // Supabase Edge Function URL for AI Chat
  static const String supabaseUrl = 'https://ghtjooqihifvbmdaojpp.supabase.co';
  static const String supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdodGpvb3FpaGlmdmJtZGFvanBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzNzM4NzQsImV4cCI6MjA4MDk0OTg3NH0.4lxPJ8kFkkJySRTapNXf5JDkVMkjt0uuT-u0xWZPQos';
  
  // VPS IP for other services (legacy)
  static const String vpsIp = '84.247.150.83';
  
  // AI Chat uses Supabase Edge Function → Modal GPU
  static const String aiChatUrl = '$supabaseUrl/functions/v1/proxy_ai';
  
  // Other backend services (health, mood) still use VPS for now
  static const bool _useLocal = String.fromEnvironment('USE_LOCAL', defaultValue: 'false') == 'true';
  
  static const String backendUrl = String.fromEnvironment(
    'BACKEND_URL',
    defaultValue: _useLocal
        ? 'http://localhost:8000'  // Local backend (when USE_LOCAL=true)
        : 'http://$vpsIp:8000',     // VPS backend (default)
  );
  
  static const String wsUrl = String.fromEnvironment(
    'WS_URL',
    defaultValue: _useLocal
        ? 'ws://localhost:8000'     // Local WebSocket
        : 'ws://$vpsIp:8000',       // VPS WebSocket (default)
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
  
  /// Send chat message to AI backend via Supabase → Modal GPU
  /// 
  /// Returns AI response or throws exception
  Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String? userId,
    String? conversationId,
  }) async {
    try {
      // Use Supabase Edge Function → Modal GPU endpoint
      final url = Uri.parse(ApiConfig.aiChatUrl);
      
      debugPrint('📤 Sending message to: $url');
      
      final response = await _client.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${ApiConfig.supabaseAnonKey}',
          'apikey': ApiConfig.supabaseAnonKey,
        },
        body: jsonEncode({
          // OpenAI-compatible format for Modal
          'messages': [
            {'role': 'user', 'content': message}
          ],
          'max_tokens': 512,
          'temperature': 0.7,
        }),
      ).timeout(
        const Duration(seconds: 300), // Longer timeout for longer CPU inference
      );
      
      debugPrint('📥 Response status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        
        // Extract message from Modal response format
        String aiMessage = '';
        if (data['choices'] != null && (data['choices'] as List).isNotEmpty) {
          aiMessage = data['choices'][0]['message']['content'] ?? '';
        } else if (data['message'] != null) {
          aiMessage = data['message'] as String;
        }
        
        return {
          'message': aiMessage,
          'conversation_id': conversationId ?? DateTime.now().millisecondsSinceEpoch.toString(),
          'timestamp': DateTime.now().toIso8601String(),
          'is_crisis': false,
        };
      } else {
        throw ApiException(
          'Chat request failed with status ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      debugPrint('Error sending chat message: $e');
      rethrow;
    }
  }
  
  /// Analyze mood entry with AI via Supabase → Modal GPU
  /// 
  /// Returns analysis or throws exception
  Future<Map<String, dynamic>> analyzeMood({
    required int moodRating,
    required List<String> emotions,
    String? journal,
  }) async {
    try {
      final url = Uri.parse(ApiConfig.aiChatUrl);
      
      debugPrint('📊 Sending mood analysis request to: $url');
      
      final response = await _client.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${ApiConfig.supabaseAnonKey}',
          'apikey': ApiConfig.supabaseAnonKey,
        },
        body: jsonEncode({
          'mode': 'mood_analysis',
          'mood_rating': moodRating,
          'emotions': emotions,
          'journal': journal ?? '',
          'max_tokens': 512,
        }),
      ).timeout(
        const Duration(seconds: 300),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        // Modal returns OpenAI format, but our proxy extracts content
        String aiMessage = '';
        if (data['choices'] != null && (data['choices'] as List).isNotEmpty) {
          aiMessage = data['choices'][0]['message']['content'] ?? '';
        } else if (data['message'] != null) {
          aiMessage = data['message'] as String;
        } else if (data['analysis'] != null) {
          aiMessage = data['analysis'] as String;
        }
        
        return {
          'analysis': aiMessage,
          'mood_score': moodRating,
          'timestamp': DateTime.now().toIso8601String(),
        };
      } else {
        throw ApiException(
          'Mood analysis failed with status ${response.statusCode}',
          statusCode: response.statusCode,
        );
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
