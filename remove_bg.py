from PIL import Image, ImageDraw

def make_transparent():
    # Open the uploaded image
    img_path = r"C:\Users\berka\.gemini\antigravity-ide\brain\a529fa63-4b00-4364-aa1e-6a28446e3df8\.user_uploaded\media_1789835439329.jpg"
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print("Could not open image:", e)
        return

    datas = img.getdata()
    newData = []
    
    # Remove black background (threshold < 20)
    for item in datas:
        if item[0] < 25 and item[1] < 25 and item[2] < 25:
            newData.append((0, 0, 0, 0)) # Transparent
        else:
            newData.append(item)

    img.putdata(newData)
    
    # Save as PNG
    img.save("assets/images/logo.png", "PNG")
    print("Created transparent logo.png successfully.")

if __name__ == '__main__':
    make_transparent()
