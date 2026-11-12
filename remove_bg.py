import numpy as np
from PIL import Image, ImageFilter

def generate_3d_logo():
    # 1. Load original logo.jpg and extract clean foreground alpha
    orig = Image.open('assets/images/logo.jpg').convert('RGB')
    arr = np.array(orig, dtype=np.float32)
    H, W, _ = arr.shape
    Y, X = np.meshgrid(np.arange(H, dtype=np.float32), np.arange(W, dtype=np.float32), indexing='ij')

    # Mask out the outer ring from original image
    dist_orig = np.sqrt((X - 505.5)**2 + (Y - 487.0)**2)
    # True white pixels have high R and B, and G is not much larger than R (excludes bright green glare)
    rb_min = np.minimum(arr[:, :, 0], arr[:, :, 2])
    green_excess = np.maximum(0.0, arr[:, :, 1] - rb_min)
    white_score = rb_min - green_excess * 1.2
    fg_raw = np.clip((white_score - 45.0) / (215.0 - 45.0), 0.0, 1.0)
    fg_raw[dist_orig >= 375] = 0.0

    # Convert fg_raw to PIL Image for subpixel shifting, scaling, and Gaussian blur
    fg_img = Image.fromarray((fg_raw * 255.0).astype(np.uint8), mode='L')

    # Visual center of the house + ECT Temizlik inside the circular boundary
    crop_r = 450.0
    cx_art, cy_art = 508.5, 492.0
    fg_centered = fg_img.transform(
        (W, H),
        Image.Transform.EXTENT,
        (cx_art - crop_r, cy_art - crop_r, cx_art + crop_r, cy_art + crop_r),
        resample=Image.Resampling.BICUBIC
    )
    # Smooth tiny JPEG artifacts and re-sharpen
    fg_smooth = fg_centered.filter(ImageFilter.GaussianBlur(radius=0.6))
    fg_mask = np.array(fg_smooth, dtype=np.float32) / 255.0
    fg_mask = np.clip((fg_mask - 0.14) / 0.74, 0.0, 1.0)
    fg_pil = Image.fromarray((fg_mask * 255.0).astype(np.uint8), mode='L')

    # 2. Build 3D Emerald Dome & Beveled Rim centered at (512, 512)
    cx, cy = 512.0, 512.0
    dx = (X - cx)
    dy = (Y - cy)
    r = np.sqrt(dx**2 + dy**2)
    R_outer = 496.0
    R_rim_inner = 460.0
    R_groove = 452.0

    # Dome normal vector (spherical cap)
    nz_dome = np.sqrt(np.clip(1.0 - (r / R_groove)**2 * 0.58, 0.05, 1.0))
    nx_dome = -(dx / R_groove) * 0.76
    ny_dome = -(dy / R_groove) * 0.76
    norm_len = np.sqrt(nx_dome**2 + ny_dome**2 + nz_dome**2)
    nx_dome = nx_dome / norm_len
    ny_dome = ny_dome / norm_len
    nz_dome = nz_dome / norm_len

    # Light source from top-left (-0.45, -0.55, 0.703)
    lx, ly, lz = -0.45, -0.55, 0.703
    ndotl = np.clip(nx_dome * lx + ny_dome * ly + nz_dome * lz, 0.0, 1.0)

    # Specular highlight (Blinn-Phong) on dome
    hx, hy, hz = -0.25, -0.32, 0.914
    ndoth = np.clip(nx_dome * hx + ny_dome * hy + nz_dome * hz, 0.0, 1.0)
    spec_dome = (ndoth ** 16) * 0.30

    # Base emerald palette (rich green, no black, no white)
    dome_r = 14.0 + ndotl * 24.0 + spec_dome * 45.0
    dome_g = 86.0 + ndotl * 82.0 + spec_dome * 95.0
    dome_b = 50.0 + ndotl * 46.0 + spec_dome * 65.0

    # 3D Torus Rim (from R_groove to R_outer)
    rim_mid = (R_outer + R_rim_inner) / 2.0
    rim_half = (R_outer - R_rim_inner) / 2.0
    rim_pos = np.clip((r - rim_mid) / rim_half, -1.0, 1.0)
    r_len = np.maximum(r, 1e-5)
    rx_dir = dx / r_len
    ry_dir = dy / r_len
    nx_rim = rx_dir * rim_pos * 0.82
    ny_rim = ry_dir * rim_pos * 0.82
    nz_rim = np.sqrt(np.clip(1.0 - nx_rim**2 - ny_rim**2, 0.05, 1.0))
    rim_ndotl = np.clip(nx_rim * lx + ny_rim * ly + nz_rim * lz, 0.0, 1.0)
    rim_spec = (np.clip(nx_rim * hx + ny_rim * hy + nz_rim * hz, 0.0, 1.0) ** 14) * 0.38

    rim_r = 16.0 + rim_ndotl * 30.0 + rim_spec * 52.0
    rim_g = 94.0 + rim_ndotl * 96.0 + rim_spec * 95.0
    rim_b = 54.0 + rim_ndotl * 56.0 + rim_spec * 65.0

    # Groove transition between R_groove and R_rim_inner
    groove_mask = np.clip((r - R_groove) / 3.0, 0.0, 1.0) * np.clip((R_rim_inner - r) / 3.0, 0.0, 1.0)
    rim_blend = np.clip((r - R_rim_inner + 2.0) / 4.0, 0.0, 1.0)

    bg_r = dome_r * (1.0 - rim_blend) + rim_r * rim_blend
    bg_g = dome_g * (1.0 - rim_blend) + rim_g * rim_blend
    bg_b = dome_b * (1.0 - rim_blend) + rim_b * rim_blend

    # Darken groove slightly for 3D separation (still rich green, never black!)
    bg_r = bg_r * (1.0 - 0.22 * groove_mask)
    bg_g = bg_g * (1.0 - 0.22 * groove_mask)
    bg_b = bg_b * (1.0 - 0.22 * groove_mask)

    # 3. 3D Extrusion & Drop Shadow of Foreground Artwork
    shadow_pil = fg_pil.transform((W, H), Image.Transform.AFFINE, (1, 0, -13, 0, 1, -15), resample=Image.Resampling.BILINEAR)
    shadow_pil = shadow_pil.filter(ImageFilter.GaussianBlur(radius=7.0))
    shadow_mask = (np.array(shadow_pil, dtype=np.float32) / 255.0) * 0.45

    bg_r = bg_r * (1.0 - shadow_mask) + 9.0 * shadow_mask
    bg_g = bg_g * (1.0 - shadow_mask) + 55.0 * shadow_mask
    bg_b = bg_b * (1.0 - shadow_mask) + 32.0 * shadow_mask

    # 3D Extruded side walls (steps from 10 down to 1)
    for step in range(10, 0, -1):
        s_pil = fg_pil.transform((W, H), Image.Transform.AFFINE, (1, 0, -step * 1.0, 0, 1, -step * 1.15), resample=Image.Resampling.BILINEAR)
        s_mask = np.array(s_pil, dtype=np.float32) / 255.0
        t = 1.0 - (step / 10.0)
        wall_r = 120.0 + t * 55.0
        wall_g = 190.0 + t * 35.0
        wall_b = 156.0 + t * 40.0
        bg_r = bg_r * (1.0 - s_mask) + wall_r * s_mask
        bg_g = bg_g * (1.0 - s_mask) + wall_g * s_mask
        bg_b = bg_b * (1.0 - s_mask) + wall_b * s_mask

    # 4. 3D Beveled Front Face of White Artwork
    fg_blur = np.array(fg_pil.filter(ImageFilter.GaussianBlur(radius=1.8)), dtype=np.float32) / 255.0
    gy, gx = np.gradient(fg_blur)
    bevel_light = np.clip((-gx * 0.7 - gy * 0.7) * 2.0, -0.15, 0.15)
    face_r = np.clip(246.0 + bevel_light * 80.0, 224.0, 255.0)
    face_g = np.clip(252.0 + bevel_light * 50.0, 240.0, 255.0)
    face_b = np.clip(249.0 + bevel_light * 65.0, 232.0, 255.0)

    final_r = bg_r * (1.0 - fg_mask) + face_r * fg_mask
    final_g = bg_g * (1.0 - fg_mask) + face_g * fg_mask
    final_b = bg_b * (1.0 - fg_mask) + face_b * fg_mask

    # 5. Crisp Anti-Aliased Circular Alpha Mask (NO black, NO white outside!)
    alpha = np.clip((R_outer - r) / 1.5, 0.0, 1.0)

    out = np.zeros((H, W, 4), dtype=np.uint8)
    out[:, :, 0] = np.clip(final_r, 0, 255).astype(np.uint8)
    out[:, :, 1] = np.clip(final_g, 0, 255).astype(np.uint8)
    out[:, :, 2] = np.clip(final_b, 0, 255).astype(np.uint8)
    out[:, :, 3] = np.clip(alpha * 255.0, 0, 255).astype(np.uint8)
    out[out[:, :, 3] == 0] = [0, 0, 0, 0]

    Image.fromarray(out, 'RGBA').save('assets/images/logo.png', 'PNG')
    print('3D logo generated successfully!')

if __name__ == '__main__':
    generate_3d_logo()
