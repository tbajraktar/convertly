import requests
import os

url = "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
output_path = "frontend/assets/sneaker.jpg"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

try:
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded to {output_path}")
except Exception as e:
    print(f"Error downloading: {e}")
