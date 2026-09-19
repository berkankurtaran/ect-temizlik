from PIL import Image
import math

def circular_crop():
    img_path = r"C:\Users\berka\.gemini\antigravity-ide\brain\a529fa63-4b00-4364-aa1e-6a28446e3df8\.user_uploaded\media_1789835439329.jpg"
    img = Image.open(img_path).convert("RGBA")
    
    datas = img.getdata()
    newData = []
    
    cx, cy = 512, 512
    # Core radius where image is fully opaque
    inner_radius = 425
    # Outer radius where image becomes fully transparent
    outer_radius = 445
    
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            r, g, b, a = pixel
            
            # Calculate distance from center
            distance = math.sqrt((x - cx)**2 + (y - cy)**2)
            
            if distance <= inner_radius:
                newData.append((r, g, b, 255))
            elif distance >= outer_radius:
                newData.append((r, g, b, 0))
            else:
                # Smooth transition (anti-aliasing)
                ratio = 1 - ((distance - inner_radius) / (outer_radius - inner_radius))
                new_a = int(255 * ratio)
                newData.append((r, g, b, new_a))
                
    img.putdata(newData)
    img.save("assets/images/logo.png", "PNG")
    print("Perfect circular crop complete.")

if __name__ == '__main__':
    circular_crop()
