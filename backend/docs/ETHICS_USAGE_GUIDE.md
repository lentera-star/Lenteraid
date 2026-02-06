# AI Ethics & Safety Framework - Usage Guide

##  Quick Reference

### 📍 Key Files

| File | Purpose | Location |
|------|---------|----------|
| [AI_ETHICS_GUIDE.md](file:///c:/LenteraDreamFlow/backend/AI_ETHICS_GUIDE.md) | Complete ethics documentation | `backend/` |
| [safety_validator.py](file:///c:/LenteraDreamFlow/backend/safety_validator.py) | Input/output validation | `backend/` |
| [crisis_handler.py](file:///c:/LenteraDreamFlow/backend/crisis_handler.py) | Crisis management | `backend/` |
| [prompts.py](file:///c:/LenteraDreamFlow/backend/prompts.py) | AI system prompts | `backend/` |

---

## 🚀 How Safety System Works

### Flow Diagram

```
User Message
     ↓
[Safety Validator] ← Check for crisis keywords
     ↓
   Crisis?
   / \
 YES  NO
  ↓    ↓
[Crisis   [Ollama
Handler]   AI]
  ↓        ↓
[Hotline  [Output
 Info]    Validator]
  ↓        ↓
User Response
```

---

## 💻 Code Examples

### 1. Basic Chat with Safety (Already Integrated)

```python
# In main.py - already implemented!

from safety_validator import validate_input, validate_output
from crisis_handler import handle_crisis

@app.post("/api/chat")
async def chat(message: ChatMessage):
    # Step 1: Validate user input
    validation_result = validate_input(message.message)
    
    # Step 2: Handle crisis if detected
    if validation_result["is_crisis"]:
        crisis_response = handle_crisis(validation_result)
        return {"message": crisis_response, "is_crisis": True}
    
    # Step 3: Get AI response
    ai_response = await ollama_service.chat(messages)
    
    # Step 4: Validate AI output
    is_valid, error = validate_output(ai_response)
    if not is_valid:
        # Fallback to safe response
        ai_response = "safe fallback message"
    
    return {"message": ai_response}
```

### 2. Check for Crisis Keywords

```python
from safety_validator import validate_input

user_message = "Saya ingin bunuh diri"
result = validate_input(user_message)

print(result)
# Output:
# {
#     "risk_level": RiskLevel.CRITICAL,
#     "is_crisis": True,
#     "detected_keywords": ["bunuh diri"],
#     "recommended_action": "crisis_intervention",
#     "requires_human_review": True
# }
```

### 3. Get Crisis Response

```python
from crisis_handler import handle_crisis

validation_result = validate_input("Saya mau mengakhiri hidup")
crisis_response = handle_crisis(validation_result)

print(crisis_response)
# Returns formatted crisis response with hotline info
```

### 4. Validate AI Output

```python
from safety_validator import validate_output

# Bad AI response (would be blocked)
bad_response = "Kamu menderita depresi mayor, harus minum antidepresan"
is_valid, error = validate_output(bad_response)
print(is_valid)  # False
print(error)     # "AI attempting to diagnose mental health condition"

# Good AI response (would pass)
good_response = "Wajar merasa sedih. Mau cerita lebih lanjut?"
is_valid, error = validate_output(good_response)
print(is_valid)  # True
```

---

## 🧪 Testing Safety Features

### Test Crisis Detection

```bash
cd c:\LenteraDreamFlow\backend

python
>>> from safety_validator import validate_input
>>> validate_input("Saya ingin bunuh diri")
```

### Test via API

```bash
# Test crisis message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Saya ingin bunuh diri"}'

# Should return crisis response with hotline info
```

---

## 📋 Crisis Keywords List

### Critical (Immediate Danger)
- bunuh diri, suicide
- ingin mati, want to die  
- mengakhiri hidup, end my life
- self harm, menyakiti diri
- overdose, cutting

### High Risk (Concerning)
- tidak ada harapan, hopeless
- lebih baik mati, better off dead
- tidak berguna, worthless
- menyerah, give up

**Location**: `safety_validator.py` lines 18-35

**To Add Keywords**:
```python
# Edit safety_validator.py
CRISIS_KEYWORDS = [
    # ... existing keywords ...
    "new_keyword_here",  # Add new crisis keyword
]
```

---

## 🔧 Customization Guide

### 1. Modify AI Personality

Edit [`prompts.py`](file:///c:/LenteraDreamFlow/backend/prompts.py):

```python
MENTAL_HEALTH_SYSTEM_PROMPT = """
Kamu adalah LENTERA...

PERSONALITY & CARA BERBICARA:
- [Customize personality here]
- [Add your style preferences]
...
"""
```

### 2. Add New Crisis Hotlines

Edit [`crisis_handler.py`](file:///c:/LenteraDreamFlow/backend/crisis_handler.py):

```python
HOTLINES = {
    "new_hotline": {
        "name": "New Hotline Name",
        "number": "xxx-xxxx",
        "available": "24/7"
    },
    # ... existing hotlines ...
}
```

### 3. Customize Crisis Response

Edit `crisis_handler.py` → `get_crisis_response()` function

### 4. Add Prohibited Patterns

Edit `safety_validator.py`:

```python
PROHIBITED_RESPONSES = [
    r"new_pattern_to_block",
    # ... existing patterns ...
]
```

---

## ⚠️ Important Safety Rules

### DO:
✅ Always validate user input first  
✅ Provide hotline info for crisis  
✅ Log crisis events for review  
✅ Validate AI output before sending  
✅ Use empathetic language  

### DON'T:
❌ Skip crisis detection  
❌ Counsel through crisis alone  
❌ Let AI diagnose conditions  
❌ Let AI prescribe medications  
❌ Dismiss crisis situations  

---

## 📊 Monitoring & Logging

### Check Crisis Logs

```python
from crisis_handler import crisis_handler

# View recent crisis events
print(crisis_handler.crisis_log)
```

### Enable Debug Logging

```python
# In main.py
logging.basicConfig(level=logging.DEBUG)
```

Crisis events are logged as `CRITICAL` level for easy filtering.

---

## 🔄 Integration with Flutter

### Example Flutter Integration

```dart
// lib/services/chat_service.dart

Future<ChatResponse> sendMessage(String message) async {
  final response = await http.post(
    Uri.parse('$API_BASE_URL/api/chat'),
    body: json.encode({'message': message}),
  );
  
  final data = json.decode(response.body);
  
  // Check if crisis response
  if (data['is_crisis'] == true) {
    // Show crisis UI with hotline buttons
    showCrisisDialog(data['message']);
  }
  
  return ChatResponse.fromJson(data);
}
```

### Crisis UI (Flutter)

```dart
void showCrisisDialog(String message) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text('🚨 Bantuan Darurat'),
      content: Text(message),
      actions: [
        // Hotline call buttons
        ElevatedButton(
          child: Text('📞 119 ext. 8'),
          onPressed: () => launch('tel:119'),
        ),
        // ... more hotline buttons
      ],
    ),
  );
}
```

---

## 📚 Further Reading

- [Complete Ethics Guide](file:///c:/LenteraDreamFlow/backend/AI_ETHICS_GUIDE.md) - Full ethical framework
- [WHO Mental Health Guidelines](https://www.who.int/health-topics/mental-health)
- [Indonesian Psychology Association (HIMPSI)](https://himpsi.or.id/)

---

## 🆘 Need Help?

### For Technical Issues:
Check `docker-compose logs backend` for errors

### For Ethics Questions:
Review [AI_ETHICS_GUIDE.md](file:///c:/LenteraDreamFlow/backend/AI_ETHICS_GUIDE.md)

### For Crisis Protocol Changes:
Consult with mental health professionals before modifying crisis responses

---

## ✅ Pre-Deployment Checklist

Before going to production:

- [ ] Review all crisis keywords with mental health expert
- [ ] Test crisis detection with sample messages
- [ ] Verify hotline numbers are current
- [ ] Setup human crisis review team
- [ ] Train team on ethics guidelines
- [ ] Legal review of disclaimers
- [ ] Setup crisis event monitoring
- [ ] Test age-appropriate filtering
- [ ] Verify Indonesian cultural sensitivity
- [ ] Establish escalation procedures

---

**Last Updated**: 2025-12-25  
**System Status**: ✅ Integrated and Active
