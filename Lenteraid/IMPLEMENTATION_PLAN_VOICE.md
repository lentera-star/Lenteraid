# 🎙️ Implementation Plan: Voice Call Audio Streaming

**Status**: 🚧 Proposed
**Goal**: Enable real-time audio recording in Flutter app and stream it to the VPS Backend (Whisper STT).

## 🧩 The Missing Piece
Currently, `VoiceCallScreen` is **UI-only**. It mimics a call but does not:
1.  Request microphone permission.
2.  Capture audio data.
3.  Send audio to `WebSocketService`.

The backend is READY (Whisper/TTS pipeline), but the frontend is silent. We need to give it a voice!

## 🛠️ Proposed Solution

### 1. New Service: `AudioRecordingService`
Create `lib/services/audio_recording_service.dart`:
- Uses usage of `record` or `flutter_sound` package (already in pubspec).
- Captures audio stream (16kHz, Mono, PCM/WAV) to match Whisper requirements.
- Handles permissions (Microphone).
- Provides a `Stream<List<int>>` of audio bytes.

### 2. Update `WebSocketService`
Ensure `VoiceCallWebSocketService` can:
- Accept the audio stream.
- Packetize audio if needed (though raw streaming might work for WebSocket).
- Handle "EndOfSpeech" or silence detection (optional, but good for UX).

### 3. Integrate into `VoiceCallScreen`
Update `lib/screens/voice_call_screen.dart`:
- **Init**: Connect WebSocket + Start Recording.
- **Loop**: Stream Mic -> WebSocket -> VPS.
- **Receive**: Listen WebSocket -> Play audio response (TTS).
- **UI**: Visualize audio levels (using stream amplitude).

## 📦 Dependencies Check
Checked `pubspec.yaml`:
- `record`: ✅ (Good for streaming raw bytes)
- `permission_handler`: ✅
- `web_socket_channel`: ✅

## 📝 Step-by-Step Implementation

1.  **Create Service**: `AudioRecordingService` class.
2.  **Integrate Logic**: Modify `VoiceCallScreen` state management.
3.  **Test**: Dry run (log bytes size) -> Connect to VPS.

## ⚠️ Challenges (Without Backend)
Since backend VPS is unstable and Local Docker is off:
- We will mock the `WebSocket` connection for testing.
- We will verify using logs that "Audio bytes are generated" (proving mic works).

---

**Ready to start coding?** 🚀
