import pygame, os

from settings import LIVES
from support import *

pygame.init()

class UI():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.original_number_sprites = load_images_from_folder('assets/ui_ux/level/numbers/')
        self.original_stage_text = load_image('assets/ui_ux/level/stage.png')
        self.original_dash_sprite = load_image('assets/ui_ux/level/dash.png')
        self.original_lives_sprite = load_images_from_folder('assets/ui_ux/health_bar/')

        self.lives = LIVES

        self.stage_size = (150, 50)
        self.number_size = (25, 25)
        self.lives_sprite_size = (120, 48)
        self.dash_size = (25, 25)
        
        self.scale_images()
    
    def scale_images(self):
        self.number_sprites = {}
        if self.original_number_sprites:
            for key, sprite in self.original_number_sprites.items():
                if sprite:
                    self.number_sprites[key.replace('.png', '')] = pygame.transform.scale(sprite, self.number_size)
        
        self.lives_sprites = {}
        if self.original_lives_sprite:
            for key, sprite in self.original_lives_sprite.items():
                if sprite:
                    self.lives_sprites[key.replace('.png', '')] = pygame.transform.scale(sprite, self.lives_sprite_size)
        
        if self.original_stage_text:
            self.stage_text = pygame.transform.scale(self.original_stage_text, self.stage_size)
        else:
            self.stage_text = None

        if self.original_dash_sprite:
            self.dash_sprite = pygame.transform.scale(self.original_dash_sprite, self.dash_size)
        else:
            self.dash_sprite = None
    
    def draw_stage_info(self, stage_number):
        stage_str = str(stage_number)
        
        total_width = 0
        if self.stage_text:
            total_width += self.stage_size[0] + 10
        total_width += len(stage_str) * (self.number_size[0] + 5) - 5
        
        pos_x = 0
        pos_y = self.display_surface.get_height() - max(self.stage_size[1], self.number_size[1])
        
        if self.stage_text:
            self.display_surface.blit(self.stage_text, (pos_x, pos_y))
            pos_x += self.stage_size[0] + 10
        
        if self.dash_size:
            self.display_surface.blit(self.dash_sprite, (pos_x - 35, pos_y + 10))

        for digit in stage_str:
            if digit in self.number_sprites and self.number_sprites[digit]:
                self.display_surface.blit(self.number_sprites[digit], (pos_x, pos_y + 10))
                pos_x += self.number_size[0] + 5
    
    def draw_lives(self,):
        x = self.display_surface.get_width()
        y = self.display_surface.get_height()

        x = x - self.lives_sprite_size[0] - 10
        y = y - self.lives_sprite_size[1] - 70
        lives_key = str(self.lives)
        if lives_key in self.lives_sprites and self.lives_sprites[lives_key]:
            self.display_surface.blit(self.lives_sprites[lives_key], (x, y))
    
    def draw_score(self, score):
        score_str = str(score).zfill(3)
        pos_x = self.display_surface.get_width() - 10
        pos_y = 10
        
        for digit in score_str:
            if digit in self.number_sprites and self.number_sprites[digit]:
                sprite = self.number_sprites[digit]
                sprite_rect = sprite.get_rect()
                sprite_rect.topright = (pos_x, pos_y)
                self.display_surface.blit(sprite, sprite_rect)
                pos_x -= self.number_size[0] + 2
    
    def draw_dash(self, x, y):
        if self.dash_sprite:
            self.display_surface.blit(self.dash_sprite, (x, y))
    
    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
        return self.lives
    
    def add_life(self):
        self.lives += 1
    
    def reset_lives(self):
        self.lives = LIVES
    
    def display(self, stage_number=0, score=0):
        self.draw_stage_info(stage_number)
        self.draw_lives()
        self.draw_score(score)