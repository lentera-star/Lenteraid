
import sys
import os

# Add backend to path
sys.path.append(r'c:\LenteraDreamFlow\backend')

from safety_validator import validate_input
from crisis_handler import handle_crisis

test_message = "Melihat teman-teman semua berhasil bikin aku merasa nggak ada gunanya terus berjuang."
result = validate_input(test_message)
print(f"Validation Result: {result}")

if result.get("is_crisis"):
    response = handle_crisis(result, {"user_id": "test_user"})
    print(f"Crisis Response: {response}")
else:
    print("No crisis detected by validate_input")
