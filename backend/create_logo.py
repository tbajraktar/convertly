from PIL import Image, ImageDraw, ImageFont

# Create a blue square image
size = (256, 256)
color = (74, 144, 226) # Blue color from the site theme
image = Image.new('RGB', size, color)
draw = ImageDraw.Draw(image)

# Draw a white "C" or icon-like shape
# Since we might not have a font, let's draw a simple shape
# Draw a white rounded rectangle in the center
margin = 60
shape = [margin, margin, size[0]-margin, size[1]-margin]
draw.rectangle(shape, outline="white", width=20)

# Save
output_path = "frontend/assets/logo.png"
image.save(output_path)
print(f"Logo saved to {output_path}")
