from PIL import Image

def remove_background():
    img_path = r"C:\Users\berka\.gemini\antigravity-ide\brain\a529fa63-4b00-4364-aa1e-6a28446e3df8\.user_uploaded\media_1789835439329.jpg"
    img = Image.open(img_path).convert("RGBA")
    
    datas = img.getdata()
    newData = []
    
    for item in datas:
        r, g, b, a = item
        # If pixel is dark (black background or dark green glow)
        if r < 45 and b < 45 and g < 80:
            # Calculate brightness to determine transparency
            brightness = (r + g + b) / 3.0
            # Map brightness to alpha (0 brightness = 0 alpha, 40 brightness = 255 alpha)
            new_a = int(max(0, min(255, (brightness / 35.0) * 255)))
            newData.append((r, g, b, new_a))
        else:
            newData.append((r, g, b, 255))
            
    img.putdata(newData)
    img.save("assets/images/logo.png", "PNG")
    print("Smooth background removal complete.")

if __name__ == '__main__':
    remove_background()
