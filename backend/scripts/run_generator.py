# Quick test script to generate training data without emoji issues
import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

# Quick test
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API Key loaded: {api_key[:20]}...")
    print("Starting data generation...")
    
    # Import and run
    os.system('chcp 65001 >nul & python generate_training_data.py --num 10')
else:
    print("ERROR: OPENAI_API_KEY not found in .env!")
