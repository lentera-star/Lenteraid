import 'package:flutter/material.dart';
import 'package:lentera/services/ai_service.dart';

/// Quick test screen to verify AI backend integration
class AITestScreen extends StatefulWidget {
  const AITestScreen({super.key});

  @override
  State<AITestScreen> createState() => _AITestScreenState();
}

class _AITestScreenState extends State<AITestScreen> {
  final AIService _aiService = AIService();
  final TextEditingController _controller = TextEditingController();
  String _response = '';
  bool _loading = false;

  Future<void> _sendTest() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _loading = true;
      _response = 'Mengirim ke backend...';
    });

    try {
      final result = await _aiService.sendMessage(
        message: text,
        conversationId: 'test-${DateTime.now().millisecondsSinceEpoch}',
      );
      
      setState(() {
        _response = 'AI Response:\n\n${result.message}';
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _response = 'ERROR: $e';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Backend Test')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: 'Test Message',
                hintText: 'Halo, aku merasa sedih',
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loading ? null : _sendTest,
              child: Text(_loading ? 'Loading...' : 'Send to AI'),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: SingleChildScrollView(
                child: Text(_response),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
