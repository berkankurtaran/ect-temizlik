from PIL import Image

img = Image.open(r"C:\Users\berka\.gemini\antigravity-ide\brain\a529fa63-4b00-4364-aa1e-6a28446e3df8\.user_uploaded\media_1789835439329.jpg").convert("RGB")
cx, cy = 512, 512

# Scan outwards from center to find the white border
for r in range(400, 512):
    p = img.getpixel((cx + r, cy))
    print(f"r={r} color={p}")
