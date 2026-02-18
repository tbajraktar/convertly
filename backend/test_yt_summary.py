import requests
import json

# Test with a Shorts video
# https://www.youtube.com/shorts/XT-1_D4q6xA
url = "http://localhost:8000/api/yt-summary"
payload = {"url": "https://www.youtube.com/shorts/XT-1_D4q6xA"}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print("-" * 20)
        print(data.get("summary"))
        print("-" * 20)
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
