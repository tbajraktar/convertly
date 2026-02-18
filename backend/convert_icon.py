from PIL import Image
import os

input_path = "frontend/assets/logo.png"
output_path = "frontend/assets/logo.ico"

try:
    img = Image.open(input_path)
    # Icon sizes for Windows
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(output_path, sizes=icon_sizes)
    print(f"Converted {input_path} to {output_path}")
except Exception as e:
    print(f"Error converting icon: {e}")
