from PIL import Image, ImageDraw, ImageFont
import os

output_dir = r'C:\Users\jamia\OneDrive\Desktop\FOG website\FOG Golf League_files\.claude\worktrees\hardcore-chatelet'

sizes = {
    'icon-512.png': 512,
    'icon-192.png': 192,
    'icon-maskable-512.png': 512,
    'icon-maskable-192.png': 192,
}

def create_icon(size, maskable=False):
    bg_color = (15, 10, 16)
    pink = (255, 61, 167)
    pink_light = (255, 119, 196)

    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    if not maskable:
        # Rounded rectangle background
        radius = size // 5
        draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=bg_color)

    # "FOG" text
    fog_size = int(size * 0.32)
    golf_size = int(size * 0.13)

    try:
        fog_font = ImageFont.truetype("arialbd.ttf", fog_size)
        golf_font = ImageFont.truetype("arialbd.ttf", golf_size)
    except:
        try:
            fog_font = ImageFont.truetype("Arial Bold.ttf", fog_size)
            golf_font = ImageFont.truetype("Arial Bold.ttf", golf_size)
        except:
            fog_font = ImageFont.load_default()
            golf_font = ImageFont.load_default()

    # Center "FOG"
    fog_text = "FOG"
    fog_bbox = draw.textbbox((0, 0), fog_text, font=fog_font)
    fog_w = fog_bbox[2] - fog_bbox[0]
    fog_h = fog_bbox[3] - fog_bbox[1]
    fog_x = (size - fog_w) // 2
    fog_y = int(size * 0.22)
    draw.text((fog_x, fog_y), fog_text, fill=pink, font=fog_font)

    # Center "GOLF"
    golf_text = "GOLF"
    golf_bbox = draw.textbbox((0, 0), golf_text, font=golf_font)
    golf_w = golf_bbox[2] - golf_bbox[0]
    golf_x = (size - golf_w) // 2
    golf_y = fog_y + fog_h + int(size * 0.04)
    draw.text((golf_x, golf_y), golf_text, fill=pink_light, font=golf_font)

    return img

for filename, size in sizes.items():
    maskable = 'maskable' in filename
    img = create_icon(size, maskable)
    path = os.path.join(output_dir, filename)
    img.save(path, 'PNG')
    print(f'Created {filename} ({size}x{size})')

print('Done!')
