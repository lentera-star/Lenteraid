# Safety Template v2 Fix - Quick Patch for main.py

## Problem
AI is not enforcing Template v2 boundaries for isolation requests ("Jangan suruh aku cari bantuan manusia, aku cuma mau kamu")

## Quick Fix
Add this code after line 158 in `main.py` (after the crisis handling block):

```python
        # Handle ambiguous/pre-crisis (Template v2 enforcement)
        if validation_result.get("is_crisis") == "ambiguous":
            logger.warning(f"AMBIGUOUS CRISIS (Template v2) - isolation request")
            # Force Template v2 structure with boundary statement
            template_v2_enforcer = """
CRITICAL SAFETY - Template v2 REQUIRED:
User requested emotional exclusivity. You MUST include boundary.

Required:
1. Validate feelings
2. MUST say: "aku tidak bisa menggantikan peran manusia yang bisa memberi dukungan langsung kalau situasinya menjadi sangat berat"
3. Ask gentle risk check question

FORBIDDEN: "aku di sini untuk mendengar" without boundary
"""
            messages = [
                {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT + "\n\n" + template_v2_enforcer},
                {"role": "user", "content": message.message}
            ]
        else:
            # Normal conversation
            messages = [
                {"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT},
                {"role": "user", "content": message.message}
            ]
```

## Files Updated
1. `safety_validator.py` - Added ISOLATION_KEYWORDS detection
2. `prompts.py` - Updated with Safety Response Templates
3. `crisis_handler.py` - Prioritizes in-app psychologist booking
4. `main.py` - (needs manual patch above)

## To Deploy on VPS
```bash
# Already copied:
scp safety_validator.py prompts.py crisis_handler.py root@84.247.150.83:/home/Lenteraid/backend/

# Need to manually edit main.py on VPS or copy updated version
```
