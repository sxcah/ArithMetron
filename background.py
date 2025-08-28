# In your background.py file, replace the existing content with this:
import pygame, os
from settings import *

def load_image(filename):
    """A helper function to load and scale images."""
    try:
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, SCREEN_SIZE)
        return img
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return pygame.Surface(SCREEN_SIZE) # Return a fallback surface


class AnimatedBackground:
    def __init__(self, path_base, num_frames, animation_speed=100):
        self.frames = []
        for i in range(1, num_frames + 1):
            filename = f"{i}.png"
            full_path = os.path.join(path_base, filename)
            self.frames.append(load_image(full_path))
        
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.animation_timer = 0
        self.current_frame = self.frames[self.frame_index]

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.current_frame = self.frames[self.frame_index]
    
    def get_current_frame(self):
        return self.current_frame