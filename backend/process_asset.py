from rembg import remove
from PIL import Image
import io

input_path = 'frontend/assets/sneaker.jpg'
output_path = 'frontend/assets/sneaker-transparent.png'

print(f"Processing {input_path}...")
try:
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input_image = i.read()
            output_image = remove(input_image)
            o.write(output_image)
    print(f"Saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")
