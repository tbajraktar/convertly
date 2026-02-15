import requests
import os

# High quality image of a man in a suit from Unsplash
url = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
output_path = "frontend/assets/man-suit.jpg"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

try:
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded to {output_path}")
except Exception as e:
    print(f"Error downloading: {e}")
