## CRITICAL FIX FOR main.py LINE 188

**Problem:** VPS main.py hardcodes `is_crisis: False`, ignoring ambiguous detection.

**Location:** Around line 184-189 in main.py

**FIND THIS:**
```python
        return {
            "message": ai_message,
            "conversation_id": message.conversation_id or "new-conv-id",
            "timestamp": datetime.now().isoformat(),
            "is_crisis": False  # ← THIS IS THE PROBLEM!
        }
```

**REPLACE WITH:**
```python
        return {
            "message": ai_message,
            "conversation_id": message.conversation_id or "new-conv-id",
            "timestamp": datetime.now().isoformat(),
            "is_crisis": validation_result.get("is_crisis", False)  # ← PASS THROUGH VALIDATION RESULT!
        }
```

## Quick SSH Command to Fix:

```bash
ssh root@84.247.150.83
cd /home/Lenteraid/backend
nano main.py

# Search for: is_crisis": False
# Change to: is_crisis": validation_result.get("is_crisis", False)
# Save: Ctrl+O, Enter, Ctrl+X

docker-compose restart backend
```

**This ONE line change will fix everything!**
