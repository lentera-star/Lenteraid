import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:lentera/theme.dart';
import 'package:lentera/services/audio_recording_service.dart';
import 'package:lentera/services/websocket_service.dart';
import 'package:permission_handler/permission_handler.dart';

class VoiceCallScreen extends StatefulWidget {
  const VoiceCallScreen({super.key});

  @override
  State<VoiceCallScreen> createState() => _VoiceCallScreenState();
}

class _VoiceCallScreenState extends State<VoiceCallScreen> with SingleTickerProviderStateMixin {
  // Services
  final AudioRecordingService _audioService = AudioRecordingService();
  final VoiceCallWebSocketService _wsService = VoiceCallWebSocketService();
  final FlutterSoundPlayer _player = FlutterSoundPlayer();

  // State
  bool _isConnecting = true;
  bool _isCallActive = false;
  bool _isMuted = false;
  bool _isSpeakerOn = false;
  String _statusMessage = 'Menghubungkan...';
  
  // Animation
  late AnimationController _animationController;
  
  // Subscriptions
  StreamSubscription? _audioSubscription;
  StreamSubscription? _wsSubscription;

  @override
  void initState() {
    super.initState();
    _setupAnimation();
    _initializeCall();
  }

  void _setupAnimation() {
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
  }

  Future<void> _initializeCall() async {
    try {
      // 1. Initialize Player
      await _player.openPlayer();
      
      // 2. Connect WebSocket
      setState(() => _statusMessage = 'Menghubungkan ke server...');
      await _wsService.connectVoiceCall();
      
      // 3. Initialize Mic & Start Recording
      setState(() => _statusMessage = 'Menyiapkan microphone...');
      final hasPermission = await _audioService.initialize();
      
      if (!hasPermission) {
        _showErrorAndExit('Permission microphone ditolak');
        return;
      }

      // Start audio stream
      await _startAudioStream();
      
      // 4. Listen to Backend Responses
      _wsSubscription = _wsService.messages.listen(_handleBackendResponse);

      if (mounted) {
        setState(() {
          _isConnecting = false;
          _isCallActive = true;
          _statusMessage = 'Silahkan berbicara';
        });
      }
    } catch (e) {
      debugPrint('Error initializing call: $e');
      _showErrorAndExit('Gagal menghubungkan panggilan: $e');
    }
  }

  Future<void> _startAudioStream() async {
    final stream = await _audioService.startRecording();
    if (stream != null) {
      _audioSubscription = stream.listen((audioData) {
        if (!_isMuted && _isCallActive) {
          _wsService.sendAudio(audioData);
          
          // Animate UI based on volume (simulated for now)
          if (audioData.length > 100) { // Simple noise gate simulation
             // In real app, calculate RMS/Amplitude here
          }
        }
      });
    }
  }

  void _handleBackendResponse(Map<String, dynamic> message) {
    try {
      // Handle Voice Response (JSON with base64 audio)
      if (message['type'] == 'voice_response') {
        final response = VoiceResponse.fromJson(message);
        
        // Update UI with transcript if available
        if (response.transcript.isNotEmpty) {
           // Optional: Show transcript toast or subtitle
        }

        // Play Audio Response
        if (response.audioBase64.isNotEmpty) {
           _playAudio(response.audioBytes);
           setState(() => _statusMessage = 'Ai sedang berbicara...');
        }
      }
      
      // Handle Text Response (Fallback)
      if (message['type'] == 'text_response') {
        // AI replied with text only
      }
      
    } catch (e) {
      debugPrint('Error handling response: $e');
    }
  }

  Future<void> _playAudio(List<int> bytes) async {
    // Stop recording while AI speaks (to apply echo cancellation logic manually if needed)
    // For now we keep recording (full duplex)
    
    // Play using flutter_sound
    if (_player.isPlaying) {
      await _player.stopPlayer();
    }
    
    await _player.startPlayer(
      fromDataBuffer: Uint8List.fromList(bytes),
      whenFinished: () {
        if (mounted) {
           setState(() => _statusMessage = 'Silahkan berbicara');
        }
      },
    );
  }

  @override
  void dispose() {
    _cleanup();
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _cleanup() async {
    await _audioSubscription?.cancel();
    await _audioService.stopRecording();
    await _wsService.disconnect();
    
    // Dispose services
    _audioService.dispose();
    // _player.closePlayer(); // Careful passing context after dispose
    if (_player.isOpen()) {
       await _player.closePlayer();
    }
  }

  void _showErrorAndExit(String message) {
    if (!mounted) return;
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
    
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted && context.canPop()) {
        context.pop();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: theme.colorScheme.primary,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: AppSpacing.paddingLg,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: Icon(Icons.arrow_back, color: theme.colorScheme.onPrimary),
                    onPressed: () => _showEndCallDialog(context),
                  ),
                  Text(
                    _isConnecting ? 'Menghubungkan...' : 'Terhubung',
                    style: context.textStyles.titleMedium?.copyWith(
                      color: theme.colorScheme.onPrimary,
                    ),
                  ),
                  const SizedBox(width: 48),
                ],
              ),
            ),
            
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AnimatedBuilder(
                    animation: _animationController,
                    builder: (context, child) {
                      return Container(
                        width: 160,
                        height: 160,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: theme.colorScheme.onPrimary.withValues(alpha: 0.2),
                          boxShadow: _isCallActive
                              ? [
                                  BoxShadow(
                                    color: theme.colorScheme.onPrimary.withValues(
                                      alpha: 0.3 * _animationController.value,
                                    ),
                                    blurRadius: 30 + (20 * _animationController.value),
                                    spreadRadius: 10 * _animationController.value,
                                  ),
                                ]
                              : null,
                        ),
                        child: Center(
                          child: Icon(
                            Icons.psychology,
                            size: 80,
                            color: theme.colorScheme.onPrimary,
                          ),
                        ),
                      );
                    },
                  ),
                  
                  const SizedBox(height: AppSpacing.xl),
                  
                  Text(
                    'LENTERA AI',
                    style: context.textStyles.headlineMedium?.copyWith(
                      color: theme.colorScheme.onPrimary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  
                  const SizedBox(height: AppSpacing.sm),
                  
                  Text(
                    _statusMessage,
                    style: context.textStyles.bodyLarge?.copyWith(
                      color: theme.colorScheme.onPrimary.withValues(alpha: 0.8),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  if (_isCallActive) ...[
                    const SizedBox(height: AppSpacing.xl),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.lg,
                        vertical: AppSpacing.md,
                      ),
                      margin: AppSpacing.horizontalXl,
                      decoration: BoxDecoration(
                        color: theme.colorScheme.onPrimary.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(AppRadius.lg),
                      ),
                      child: Text(
                        '💡 Tips: Berbicara dengan jelas dan tenang untuk hasil terbaik',
                        style: context.textStyles.bodySmall?.copyWith(
                          color: theme.colorScheme.onPrimary,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ],
              ),
            ),
            
            Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildControlButton(
                    context,
                    icon: _isMuted ? Icons.mic_off : Icons.mic,
                    label: _isMuted ? 'Unmute' : 'Mute',
                    onTap: () => setState(() => _isMuted = !_isMuted),
                    backgroundColor: _isMuted
                        ? theme.colorScheme.error
                        : theme.colorScheme.onPrimary.withValues(alpha: 0.2),
                  ),
                  
                  _buildControlButton(
                    context,
                    icon: Icons.call_end,
                    label: 'End',
                    onTap: () => _showEndCallDialog(context),
                    backgroundColor: theme.colorScheme.error,
                    size: 72,
                  ),
                  
                  _buildControlButton(
                    context,
                    icon: _isSpeakerOn ? Icons.volume_up : Icons.volume_down,
                    label: 'Speaker',
                    onTap: () async {
                        // Toggle speaker logic (requires audio session config which is advanced)
                        // For now just toggle UI state
                        setState(() => _isSpeakerOn = !_isSpeakerOn);
                    },
                    backgroundColor: _isSpeakerOn
                        ? theme.colorScheme.tertiary
                        : theme.colorScheme.onPrimary.withValues(alpha: 0.2),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildControlButton(
    BuildContext context, {
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required Color backgroundColor,
    double size = 64,
  }) {
    return Column(
      children: [
        GestureDetector(
          onTap: onTap,
          child: Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
              color: backgroundColor,
              shape: BoxShape.circle,
            ),
            child: Icon(
              icon,
              color: Colors.white,
              size: size * 0.4,
            ),
          ),
        ),
        const SizedBox(height: AppSpacing.sm),
        Text(
          label,
          style: Theme.of(context).textTheme.labelSmall?.copyWith(
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  void _showEndCallDialog(BuildContext context) {
    final theme = Theme.of(context);
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: theme.colorScheme.surface,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.lg),
        ),
        title: Text(
          'Akhiri Panggilan?',
          style: context.textStyles.titleLarge?.semiBold,
        ),
        content: Text(
          'Apakah Anda yakin ingin mengakhiri panggilan dengan LENTERA AI?',
          style: context.textStyles.bodyMedium,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(
              'Batal',
              style: context.textStyles.labelLarge?.copyWith(
                color: theme.colorScheme.primary,
              ),
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _cleanup(); // Cleanup connection
              context.pop();
            },
            child: Text(
              'Akhiri',
              style: context.textStyles.labelLarge?.copyWith(
                color: theme.colorScheme.error,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
