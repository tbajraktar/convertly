import requests

url = "http://localhost:8000/remove-bg"
files = {'file': open('sample.jpg', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        with open('result.png', 'wb') as f:
            f.write(response.content)
        print("Success! Image saved as result.png")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
