import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import 'dart:convert';
import 'dart:async';
import 'api_client.dart';

/// WebSocket service for real-time communications
class WebSocketService with ChangeNotifier {
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  bool _isConnected = false;
  
  // Connection state
  bool get isConnected => _isConnected;
  
  // Stream controller for messages
  final _messageController = StreamController<Map<String, dynamic>>.broadcast();
  Stream<Map<String, dynamic>> get messages => _messageController.stream;
  
  /// Connect to WebSocket endpoint
  Future<void> connect(String endpoint) async {
    try {
      final wsUrl = '${ApiConfig.wsUrl}$endpoint';
      debugPrint('Connecting to WebSocket: $wsUrl');
      
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      
      // Listen to messages
      _subscription = _channel!.stream.listen(
        (data) {
          _handleMessage(data);
        },
        onError: (error) {
          debugPrint('WebSocket error: $error');
          _isConnected = false;
          notifyListeners();
        },
        onDone: () {
          debugPrint('WebSocket closed');
          _isConnected = false;
          notifyListeners();
        },
      );
      
      _isConnected = true;
      notifyListeners();
      debugPrint('WebSocket connected successfully');
    } catch (e) {
      debugPrint('WebSocket connection failed: $e');
      _isConnected = false;
      notifyListeners();
      rethrow;
    }
  }
  
  /// Handle incoming WebSocket message
  void _handleMessage(dynamic data) {
    try {
      if (data is String) {
        final message = jsonDecode(data) as Map<String, dynamic>;
        _messageController.add(message);
      } else if (data is List<int>) {
        // Binary data (audio, etc)
        _messageController.add({
          'type': 'binary',
          'data': data,
        });
      }
    } catch (e) {
      debugPrint('Error handling WebSocket message: $e');
    }
  }
  
  /// Send message through WebSocket
  void sendMessage(Map<String, dynamic> message) {
    if (_isConnected && _channel != null) {
      _channel!.sink.add(jsonEncode(message));
    } else {
      debugPrint('Cannot send message: WebSocket not connected');
    }
  }
  
  /// Send binary data (e.g., audio)
  void sendBinary(List<int> data) {
    if (_isConnected && _channel != null) {
      _channel!.sink.add(data);
    } else {
      debugPrint('Cannot send binary: WebSocket not connected');
    }
  }
  
  /// Disconnect from WebSocket
  Future<void> disconnect() async {
    try {
      await _subscription?.cancel();
      await _channel?.sink.close(status.goingAway);
      _isConnected = false;
      notifyListeners();
      debugPrint('WebSocket disconnected');
    } catch (e) {
      debugPrint('Error disconnecting WebSocket: $e');
    }
  }
  
  @override
  void dispose() {
    disconnect();
    _messageController.close();
    super.dispose();
  }
}

/// Voice Call WebSocket Service
/// Handles real-time voice communication with backend
class VoiceCallWebSocketService extends WebSocketService {
  /// Connect to voice call endpoint
  Future<void> connectVoiceCall() async {
    await connect(ApiConfig.voiceCallWs);
  }
  
  /// Send audio data for processing
  /// Backend will return: transcript + AI response + TTS audio
  void sendAudio(List<int> audioData) {
    debugPrint('Sending audio: ${audioData.length} bytes');
    sendBinary(audioData);
  }
  
  /// Stream of voice responses from backend
  Stream<VoiceResponse> get voiceResponses {
    return messages.where((msg) => msg['type'] == 'voice_response').map(
      (msg) => VoiceResponse.fromJson(msg),
    );
  }
  
  /// Stream of errors
  Stream<String> get errors {
    return messages.where((msg) => msg['type'] == 'error').map(
      (msg) => msg['message'] as String? ?? 'Unknown error',
    );
  }
}

/// Voice response from backend
class VoiceResponse {
  final String transcript;
  final String aiResponse;
  final String audioBase64;
  final double confidence;
  
  VoiceResponse({
    required this.transcript,
    required this.aiResponse,
    required this.audioBase64,
    required this.confidence,
  });
  
  factory VoiceResponse.fromJson(Map<String, dynamic> json) {
    return VoiceResponse(
      transcript: json['transcript'] as String? ?? '',
      aiResponse: json['ai_response'] as String? ?? '',
      audioBase64: json['audio_base64'] as String? ?? '',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
    );
  }
  
  /// Decode audio from base64
  List<int> get audioBytes {
    return base64Decode(audioBase64);
  }
}
