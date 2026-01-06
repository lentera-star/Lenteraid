import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:record/record.dart';

/// Service to handle audio recording and streaming
/// captures raw PCM data for real-time processing
class AudioRecordingService {
  final AudioRecorder _audioRecorder = AudioRecorder();
  StreamSubscription<List<int>>? _audioSubscription;
  bool _isRecording = false;

  bool get isRecording => _isRecording;

  /// Initialize and check permissions
  Future<bool> initialize() async {
    final status = await Permission.microphone.request();
    return status == PermissionStatus.granted;
  }

  /// Start recording and get the audio stream
  /// Returns a stream of audio bytes (PCM 16-bit, 16kHz, Mono)
  Future<Stream<Uint8List>?> startRecording() async {
    try {
      // Check permission again
      if (!await _audioRecorder.hasPermission()) {
        debugPrint('Microphone permission denied');
        return null;
      }

      // Configure recording parameters for Whisper
      // Whisper works best with 16kHz, 16-bit, Mono audio
      const config = RecordConfig(
        encoder: AudioEncoder.pcm16bit,
        sampleRate: 16000,
        numChannels: 1,
      );

      // Start the stream
      final stream = await _audioRecorder.startStream(config);
      _isRecording = true;
      debugPrint('Audio recording started: 16kHz PCM 16bit Mono');
      
      return stream;
    } catch (e) {
      debugPrint('Error starting recording: $e');
      _isRecording = false;
      return null;
    }
  }

  /// Stop recording
  Future<void> stopRecording() async {
    try {
      if (!_isRecording) return;
      
      await _audioRecorder.stop();
      _isRecording = false;
      debugPrint('Audio recording stopped');
    } catch (e) {
      debugPrint('Error stopping recording: $e');
    }
  }

  /// Check authentication/permission status
  Future<bool> hasPermission() async {
    return await _audioRecorder.hasPermission();
  }

  /// Dispose resources
  void dispose() {
    stopRecording();
    _audioRecorder.dispose();
  }
}
