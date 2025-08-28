import pygame as py, os, random

def load_image(path, colorkey=None):
    try:
        image = py.image.load(path)
        image = image.convert_alpha() if image.get_alpha() else image.convert()

        if colorkey is not None:
            image.set_colorkey(colorkey)

        return image
    except Exception as e:
        print(f"Failed to load image: {path}\n{e}")
        return None


def load_images_from_folder(folder, colorkey=None):
    images = {}

    for filename in os.listdir(folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            path = os.path.join(folder, filename)
            images[filename] = load_image(path, colorkey)

    return images

def surface_blit(surface, pos=(0, 0)):
    display_surface = py.display.get_surface()

    display_surface.blit(surface, pos)

def load_font(font, font_size):
    fonts = {}

    for size_key, size in font_size.items():
        fonts[size_key] = py.font.Font(font, size)

    return fonts

def overlay(size, color, alpha, pos=None):
    overlay = py.Surface(size, py.SRCALPHA)
    overlay.fill(color)
    overlay.set_alpha(alpha)

    if pos is None:
        pos = (0, 0)

    surface_blit(overlay, pos)

def display_text(display, font, text, color, center=None):
    fonts = font
    text_surf = fonts.render(text, True, color)

    if center is None:
        center = (display[0] // 2, display[1] // 2)
    text_rect = text_surf.get_rect(center=center)

    surface_blit(text_surf, text_rect)

    return text_rect

def draw_stars(display, stars, height):

    new_stars = [(x, (y + 3) % height) for (x, y) in stars]

    for (x, y) in new_stars:
        py.draw.rect(display, (200, 200, 220), (x, y, 2, 2))
    return new_stars
def get_master_sfx_volume() -> float:
    """
    Returns the current SFX volume (0.0 – 1.0) as set in SettingsPopup.
    """
    import __main__   # simple way to reach the running Game instance
    return __main__.game.settings_popup.sfx_volume