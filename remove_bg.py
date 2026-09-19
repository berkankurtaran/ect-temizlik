from PIL import Image

def make_transparent():
    # Open the image
    try:
        img = Image.open('assets/images/logo.jpg')
    except Exception as e:
        print("Could not open logo.jpg:", e)
        return
        
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    # If the background is light grey or white, we make it transparent.
    # Adjusting threshold. Greys can be around 200+.
    for item in datas:
        # Check if the pixel is light enough to be the background
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0)) # Fully transparent
        else:
            newData.append(item) # Keep the original pixel

    img.putdata(newData)
    img.save("assets/images/logo.png", "PNG")
    print("Created logo.png successfully.")

if __name__ == '__main__':
    make_transparent()
