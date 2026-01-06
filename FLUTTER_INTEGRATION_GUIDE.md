# Flutter-Backend Integration Guide

## ✅ Backend Server Running!

**Status**: Backend is running on `http://localhost:8000`

**Endpoints Available**:
- `GET /health` - Health check
- `POST /api/chat` - Send chat message

---

## 📱 Flutter Integration Steps

### Step 1: API Service Created ✅

File: `lib/services/api_service.dart`

**Features**:
- Uses Dio (already in pubspec.yaml)
- Base URL: `http://10.0.2.2:8000` (for Android emulator)
- Chat endpoint integration
- Error handling

---

### Step 2: Update Chat Screen

You need to integrate `ApiService` into your existing chat screen.

**Example Integration**:

```dart
import 'package:lentera/services/api_service.dart';

class ChatScreen extends StatefulWidget {
  // ... existing code
}

class _ChatScreenState extends State<ChatScreen> {
  final ApiService _apiService = ApiService();
  final List<Map<String, String>> _conversationHistory = [];
  bool _isLoading = false;

  Future<void> _sendMessage(String message) async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Send to backend
      final response = await _apiService.sendMessage(
        message,
        _conversationHistory,
      );

      // Add user message
      _conversationHistory.add({
        'role': 'user',
        'content': message,
      });

      // Add AI response
      _conversationHistory.add({
        'role': 'assistant',
        'content': response['response'],
      });

      setState(() {
        _isLoading = false;
      });

      // Check if crisis
      if (response['is_crisis'] == true) {
        // Show crisis alert with hotlines
        _showCrisisAlert(response['crisis_info']);
      }

    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      // Show error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  void _showCrisisAlert(Map<String, dynamic>? crisisInfo) {
    // Show dialog with crisis hotlines
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Bantuan Darurat'),
        content: Text(crisisInfo?['message'] ?? ''),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('OK'),
          ),
        ],
      ),
    );
  }
}
```

---

### Step 3: Test Backend Connection

**Before running Flutter app**, test backend:

1. **Open browser**: http://localhost:8000/docs
2. **Test /health endpoint**: Should return `{"status": "healthy"}`
3. **Test /api/chat endpoint**: 
   - Click "Try it out"
   - Input:
     ```json
     {
       "message": "Halo, aku sedih hari ini",
       "conversation_history": []
     }
     ```
   - Should get AI response!

---

### Step 4: Run Flutter App

```bash
cd c:\LenteraDreamFlow
flutter run
```

**Important**:
- For Android emulator: Use `http://10.0.2.2:8000`
- For iOS simulator: Use `http://localhost:8000`
- For physical device: Use your computer's IP (e.g., `http://192.168.1.100:8000`)

---

## 🔧 Troubleshooting

### Backend Not Responding

**Check if server is running**:
```powershell
# In PowerShell, check if port 8000 is listening
netstat -ano | findstr :8000
```

**Restart backend**:
```powershell
cd c:\LenteraDreamFlow\backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Connection Refused from Flutter

**Update base URL in `api_service.dart`**:

For physical device, use your computer's IP:
```dart
static const String baseUrl = 'http://YOUR_IP:8000';
```

Find your IP:
```powershell
ipconfig
# Look for IPv4 Address
```

### CORS Issues

Backend already has CORS enabled for all origins (development mode).

---

## 📊 API Response Format

### Chat Response

```json
{
  "response": "Halo! Aku mendengar kamu sedang sedih...",
  "is_crisis": false,
  "crisis_info": null,
  "conversation_id": "uuid-here"
}
```

### Crisis Response

```json
{
  "response": "Aku mendengar kamu...",
  "is_crisis": true,
  "crisis_info": {
    "severity": "high",
    "message": "Hubungi bantuan darurat",
    "hotlines": [
      {
        "name": "Sejiwa",
        "number": "119 ext 8",
        "available": "24/7"
      }
    ]
  }
}
```

---

## ✅ Next Steps

1. **Integrate ApiService** into your chat screen
2. **Test chat flow** with backend
3. **Handle loading states** (show spinner while waiting)
4. **Handle errors** (show error messages)
5. **Test crisis detection** (try "aku ingin bunuh diri")

---

## 🎯 Current Status

- ✅ Backend running on localhost:8000
- ✅ API service created
- ✅ Chat endpoint ready
- ⏳ **Need**: Integrate into chat screen UI
- ⏳ **Need**: Test end-to-end flow

**Estimated time to complete**: 30-45 minutes

---

## 💡 Tips

- Test backend in browser first (http://localhost:8000/docs)
- Use Postman/Thunder Client to test API before Flutter
- Check backend logs for errors
- Use `print()` statements in Flutter to debug

**Backend logs location**: Terminal where uvicorn is running

---

**Ready to integrate?** Update your chat screen with the example code above! 🚀
