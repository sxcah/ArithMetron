import pygame as py

from support import surface_blit, load_font, overlay, display_text
from settings import FONT, FONT_SIZE

class StageCleared():
    def __init__(self,  background, stars, all_sprites, score):
        self.display_surface = py.display.get_surface()

        self.stars = stars
        self.background = background
        self.all_sprites = all_sprites
        self.score = score

        self.font = load_font(FONT, FONT_SIZE)

    def update(self, dt):
        self.star = [((x - 1) % self.display_surface.get_width(),(y + 1) % self.display_surface.get_height()) for (x, y) in self.stars]
        self.all_sprites.update(dt)

    def display(self):
        surface_blit(self.background, (0, 0))

        for (x, y) in self.stars:
            self.display_surface.fill((200, 200, 220), (x, y, 2, 2))

        self.all_sprites.draw(self.display_surface)

        overlay((self.display_surface.get_width(),
                 self.display_surface.get_height()),
                 (0, 50, 0),
                 180
                 )

        display_text(self.display_surface,
                     self.font['big'],
                     "VICTORY",
                     (255, 255, 0),
                     (self.display_surface.get_width() // 2,
                      self.display_surface.get_height() // 2 - 60)                    
                     )
        
        display_text(self.display_surface,
                     self.font['med'],
                     f"Current Score: {self.score}",
                     (255, 255, 255),
                     (self.display_surface.get_width() // 2,
                      self.display_surface.get_height() // 2)                    
                     )

        display_text(self.display_surface,
                     self.font['med'],
                     "Press \"Enter\" to Next Stage!",
                     (255, 255, 255),
                     (self.display_surface.get_width() // 2,
                      self.display_surface.get_height() // 2 + 80)                    
                     )

        display_text(self.display_surface,
                     self.font['med'],
                     "Press \"R\" to return to Menu!",
                     (255, 255, 255),
                     (self.display_surface.get_width() // 2,
                      self.display_surface.get_height() // 2 + 120)                    
                     )
        