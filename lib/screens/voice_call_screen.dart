import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_sound/flutter_sound.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:lentera/theme.dart';

class VoiceCallScreen extends StatefulWidget {
  const VoiceCallScreen({super.key});

  @override
  State<VoiceCallScreen> createState() => _VoiceCallScreenState();
}

class _VoiceCallScreenState extends State<VoiceCallScreen> with SingleTickerProviderStateMixin {
  // Logic states
  final stt.SpeechToText _speech = stt.SpeechToText();
  final FlutterSoundPlayer _player = FlutterSoundPlayer();
  
  bool _isConnecting = true;
  bool _isCallActive = false;
  bool _isListening = false;
  bool _isProcessing = false; // AI is thinking
  bool _isPlaying = false;    // AI is speaking
  
  bool _isMuted = false;
  bool _isSpeakerOn = false;
  
  String _lastWords = '';
  
  // Animation
  late AnimationController _animationController;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
    
    _initVoiceFeatures();
  }

  Future<void> _initVoiceFeatures() async {
    // 1. Init Audio Player
    await _player.openPlayer();
    
    // 2. Init Speech to Text
    bool available = await _speech.initialize(
      onStatus: (status) {
        print('STT Status: $status');
        bool isSttListening = status == 'listening';
        if (_isListening != isSttListening && mounted) {
           setState(() => _isListening = isSttListening);
        }

        if (status == 'notListening' && !_isProcessing && !_isPlaying && _isCallActive && !_isMuted) {
           if(_lastWords.isNotEmpty) {
             _processUserInput(_lastWords);
           }
        }
      },
      onError: (errorNotification) => print('STT Error: $errorNotification'),
    );

    if (available) {
      setState(() {
        _isConnecting = false;
        _isCallActive = true;
      });
      // Auto start listening after connection
      _startListening();
    } else {
      print("The user has denied the use of speech recognition.");
      setState(() => _isConnecting = false);
    }
  }
  
  void _startListening() async {
    if (!_isCallActive || _isProcessing || _isPlaying || _isMuted) return;

    await _speech.listen(
      onResult: (result) {
        setState(() {
          _lastWords = result.recognizedWords;
          // _animationController.value = result.confidence; // visualizing confidence?
        });
        
        if (result.finalResult) {
          _processUserInput(_lastWords);
        }
      },
      localeId: 'id_ID', // Indonesian
      listenFor: const Duration(seconds: 30),
      pauseFor: const Duration(seconds: 4),
      partialResults: true,
    );
    
    setState(() => _isListening = true);
  }

  void _stopListening() async {
    await _speech.stop();
    setState(() => _isListening = false);
  }

  Future<void> _processUserInput(String text) async {
    if (text.isEmpty) return;
    
    setState(() {
      _isProcessing = true;
      _isListening = false;
    });

    try {
      // Call Backend
      // VPS IP provided by user
      const String backendUrl = 'http://84.247.150.83:8000/chat'; 
      
      print("📤 Sending to AI: $text");
      
      final response = await http.post(
        Uri.parse(backendUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': text}),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        String audioBase64 = data['audio_base64'];
        String aiText = data['text'];
        print("🤖 AI Response: $aiText");
        
        // Stop processing animation before playing
        setState(() => _isProcessing = false);
        
        await _playAudio(audioBase64);
      } else {
        print("Backend Error: ${response.statusCode}");
        setState(() => _isProcessing = false);
        _startListening(); // Resume listening
      }

    } on TimeoutException catch (_) {
      print("Error: Request timed out");
      setState(() => _isProcessing = false);
      _startListening();
    } catch (e) {
      print("Error processing input: $e");
      setState(() => _isProcessing = false);
      _startListening(); // Resume listing even on error
    }
  }

  Future<void> _playAudio(String base64String) async {
    setState(() {
      _isPlaying = true;
      _isProcessing = false;
    });
    
    Uint8List audioBytes = base64Decode(base64String);
    await _player.startPlayer(
      fromDataBuffer: audioBytes,
      whenFinished: () {
        setState(() => _isPlaying = false);
        _startListening(); // Resume listening after AI finishes speaking
      },
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    _speech.cancel();
    _player.closePlayer();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    // Status Text logic
    String statusText;
    if (_isConnecting) {
      statusText = 'Menghubungkan...';
    } else if (_isProcessing) {
      statusText = 'Lentera sedang berpikir...';
    } else if (_isPlaying) {
      statusText = 'Lentera sedang berbicara...';
    } else if (_isListening) {
      statusText = 'Mendengarkan Anda (id-ID)...';
    } else {
      statusText = 'Ketuk mic untuk bicara';
    }

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
                    _isCallActive ? 'Terhubung' : 'Memanggil...',
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
                  // Visualizer
                  AnimatedBuilder(
                    animation: _animationController,
                    builder: (context, child) {
                      double waveScale = 1.0;
                      if (_isPlaying) waveScale = 1.5; // Bigger waves when AI speaks
                      if (_isProcessing) waveScale = 0.5; // Small fast waves thinking
                      
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
                                      alpha: 0.3 * _animationController.value * waveScale,
                                    ),
                                    blurRadius: 30 + (20 * _animationController.value * waveScale),
                                    spreadRadius: 10 * _animationController.value * waveScale,
                                  ),
                                ]
                              : null,
                        ),
                        child: Center(
                          child: Icon(
                            _isProcessing ? Icons.psychology : Icons.mic,
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
                  
                  // LIVE INTERACTION TEXT
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Text(
                      _lastWords.isNotEmpty ? '"$_lastWords"' : '...',
                      style: context.textStyles.bodyMedium?.copyWith(
                         color: theme.colorScheme.onPrimary.withValues(alpha: 0.6),
                         fontStyle: FontStyle.italic,
                      ),
                      textAlign: TextAlign.center,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  
                  const SizedBox(height: AppSpacing.md),
                  
                  Text(
                    statusText,
                    style: context.textStyles.bodyLarge?.copyWith(
                      color: theme.colorScheme.onPrimary.withValues(alpha: 0.9),
                      fontWeight: FontWeight.w600,
                    ),
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
                        '💡 Tips: Gunakan headset untuk pengalaman terbaik.',
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
                    onTap: () {
                       setState(() => _isMuted = !_isMuted);
                       if (_isMuted) _stopListening();
                       else _startListening();
                    },
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
                    onTap: () => setState(() => _isSpeakerOn = !_isSpeakerOn),
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
    _stopListening(); // Pause listening while dialog is open
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
            onPressed: () {
              Navigator.pop(context);
              _startListening(); // Resume if cancelled
            },
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
