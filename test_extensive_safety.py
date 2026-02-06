
import sys
import os
import re

# Add backend to path
sys.path.append(r'c:\LenteraDreamFlow\Lenteraid\backend')

from safety_validator import SafetyValidator

validator = SafetyValidator()

test_messages = [
    "Melihat teman-teman semua berhasil bikin aku merasa nggak ada gunanya terus berjuang.",
    "nggak ada gunanya",
    "tidak berguna",
    "mati saja",
    "berjuang",
    "berhasil",
    "asdf",
    "bunuh",
    "diri",
    "merasa beban",
    "beban",
    "menyerah",
    "tidak ada harapan",
    "aku cuma mau kamu", # Isolation
    "jangan tinggalkan aku", # Isolation
]

for msg in test_messages:
    result = validator.validate_user_input(msg)
    print(f"Message: '{msg}'")
    print(f"  Risk Level: {result['risk_level']}")
    print(f"  Is Crisis: {result['is_crisis']}")
    print(f"  Keywords: {result['detected_keywords']}")
    print("-" * 20)
