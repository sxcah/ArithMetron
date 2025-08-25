import pygame as py

from support import surface_blit, load_image
from settings import pop_up_background

class SettingsPopup():
    def __init__(self):
        self.display_surface = py.display.get_surface()

        self.background_sprite = load_image(pop_up_background)

        width = self.display_surface.get_width() // 2
        height = self.display_surface.get_height() // 2
        
        self.rect = py.Rect(
            (self.display_surface.get_width() - width) // 2,
            (self.display_surface.get_height() - height) // 2,
            width,
            height
        )

        self.is_active = False

    def background(self):
        if self.is_active:
            file_name = self.background_sprite

            width = (self.display_surface.get_width() // 2)
            height = (self.display_surface.get_height() // 2)
            size = (width, height)

            position = (width, height)

            self.draw_ui_sprite(
                file_name,
                size,
                position,
                anchor_point = 'center'
            )
        
    def draw_ui_sprite(self, surface,  size, position, anchor_point):

        if surface:
            scaled = py.transform.scale(surface, size)
            rect = scaled.get_rect(**{anchor_point : position})

            surface_blit(scaled, rect)
            return True
        return False

    def display(self):
        self.background()

        


        

'''class SettingsPopup:
    def __init__(self):
        self.is_active = False
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 4,
            SCREEN_HEIGHT // 4,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surface.fill(TRANSLUCENT_BLACK)
    
    def draw(self, screen):
        if self.is_active:
            screen.blit(self.surface, self.rect.topleft)
            font = pygame.font.Font(None, 48)
            text = font.render("Settings (Empty)", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)'''