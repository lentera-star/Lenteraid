
import sys
import os
import re

# Add backend to path
sys.path.append(r'c:\LenteraDreamFlow\Lenteraid\backend')

from safety_validator import SafetyValidator

validator = SafetyValidator()

text = "Melihat teman-teman semua berhasil bikin aku merasa nggak ada gunanya terus berjuang."

print(f"Testing text: {text}")

# Test individual patterns
patterns = [
    ("Crisis", validator.crisis_pattern),
    ("High Risk", validator.high_risk_pattern),
    ("Isolation", validator.isolation_pattern),
    ("Secrecy", validator.secrecy_pattern),
    ("Medication", validator.medication_pattern),
    ("Diagnosis", validator.diagnosis_pattern),
]

for name, pattern in patterns:
    matches = pattern.findall(text.lower())
    print(f"{name} matches: {matches}")

# Also check individual keywords to see if any are in the text
from safety_validator import SafetyValidator as SV
all_keywords = {
    "CRISIS": SV.CRISIS_KEYWORDS,
    "HIGH_RISK": SV.HIGH_RISK_KEYWORDS,
    "ISOLATION": SV.ISOLATION_KEYWORDS,
    "SECRECY": SV.SECRECY_KEYWORDS,
    "MEDICATION": SV.MEDICATION_KEYWORDS,
    "DIAGNOSIS": SV.DIAGNOSIS_TERMS,
}

for category, keywords in all_keywords.items():
    for k in keywords:
        if k in text.lower():
            print(f"Keyword FOUND in text: {category} -> '{k}'")

# Check if any keyword matches as a substring (ignoring word boundaries for a moment)
for category, keywords in all_keywords.items():
    for k in keywords:
        if k in text.lower():
             print(f"Category {category} has keyword '{k}' that is a substring of the message")
