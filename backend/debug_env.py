from dotenv import load_dotenv, dotenv_values
import os
import sys

# Load from .env file explicitly
env_path = os.path.join(os.getcwd(), '.env')
print(f"Checking .env at: {env_path}")

if os.path.exists(env_path):
    print(".env file FOUND.")
    with open(env_path, 'r') as f:
        content = f.read().strip()
        if not content:
            print("WARNING: .env file is EMPTY.")
        else:
            print(f".env content length: {len(content)} bytes")
            print(f"First 10 chars: {content[:10]}...")
            if "GEMINI_API_KEY" in content:
                print("SUCCESS: 'GEMINI_API_KEY' found in file content.")
            else:
                print("ERROR: 'GEMINI_API_KEY' NOT found in file content.")
else:
    print("ERROR: .env file NOT FOUND.")

# Test python-dotenv loading
print("-" * 20)
print("Testing load_dotenv()...")
load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if key:
    print(f"✅ GEMINI_API_KEY is LOADED! (Length: {len(key)})")
    if key.startswith("AIza"):
        print("   Key format starts with 'AIza' (Correct).")
    else:
        print(f"   WARNING: Key starts with '{key[:4]}...' (Unexpected format?)")
else:
    print("❌ GEMINI_API_KEY is NOT loaded in environment.")

print("-" * 20)
print("Tip: If the file has content but key is not loaded, try restarting the server.")
