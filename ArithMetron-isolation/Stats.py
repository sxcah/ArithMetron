import pygame as py
import os
from support import surface_blit, load_image, load_font, draw_ui_sprite
from settings import *

class MyStatsPopup:
    def _init_assets(self):
        """Initialize all asset sprites"""
        try:
            # Load digit sprites (0-9)
            base_path = "assets/ui_ux/settings/number"
            self.digits = {}
            for n in range(10):
                self.digits[n] = load_image(os.path.join(base_path, f"{n}.png"))
            
            # Load text sprites
            text_path = "assets/ui_ux/settings/text"
            self.text_sprites = {
                'highest': load_image(os.path.join(text_path, "highest.png")),
                'level': load_image(os.path.join(text_path, "level.png")),
                'annihilated': load_image(os.path.join(text_path, "annihilated.png"))
            }
            
            print("MyStatsPopup assets loaded successfully")
            
        except Exception as e:
            print(f"Warning: Could not load MyStatsPopup assets: {e}. Using fallbacks.")
            
            # Create fallback digits
            font = py.font.Font(None, 48)
            self.digits = {}
            for n in range(10):
                surf = font.render(str(n), True, WHITE)
                self.digits[n] = surf
            
            # Create fallback text
            text_font = py.font.Font(None, 36)
            self.text_sprites = {
                'highest': text_font.render("HIGHEST", True, WHITE),
                'level': text_font.render("LEVEL", True, WHITE),
                'annihilated': text_font.render("ANNIHILATED", True, WHITE)
            }

    def __init__(self):
        self.display_surface = py.display.get_surface()
        
        # Load background sprite
        try:
            self.background_sprite = load_image("assets/ui_ux/settings/tab.png")
        except:
            # Fallback background
            self.background_sprite = None
            print("Warning: Could not load tab.png background")

        # Calculate popup dimensions and position
        width = self.display_surface.get_width() // 2
        height = self.display_surface.get_height() // 2
        
        self.rect = py.Rect(
            (self.display_surface.get_width() - width) // 2,
            (self.display_surface.get_height() - height) // 2,
            width,
            height
        )

        self.is_active = False
        
        # Load font
        self.font = load_font(FONT, FONT_SIZE)
        
        # Stats data
        self.highest_level = 1  # Start at 1 instead of 0
        self.annihilated = 0
        
        # Initialize assets
        self.digits = {}
        self.text_sprites = {}
        self._init_assets()

    def update(self, data):
        """Update stats with new data"""
        new_level = data.get("highest_level", self.highest_level)
        new_annihilated = data.get("annihilated", 0)
        
        # Keep track of highest level achieved
        if new_level > self.highest_level:
            self.highest_level = new_level
            
        # Keep track of total enemies annihilated across all stages
        self.annihilated += new_annihilated
        
        print(f"Stats updated: Level {self.highest_level}, Annihilated {self.annihilated}")

    def toggle(self):
        """Toggle popup visibility"""
        self.is_active = not self.is_active
        print(f"MyStatsPopup toggled: is_active = {self.is_active}")

    def handle_event(self, event):
        """Handle events (currently no interactive elements, but keeping structure consistent)"""
        if not self.is_active:
            return
        
        # Add any event handling logic here if needed in the future
        pass

    def background(self):
        """Draw the popup background"""
        if self.is_active:
            if self.background_sprite:
                # Use sprite if available
                width = self.display_surface.get_width() // 2 + 75
                height = self.display_surface.get_height() // 2 + 200
                size = (width, height)
                x = self.display_surface.get_width() // 2
                y = self.display_surface.get_height() // 2
                position = (x, y)
                draw_ui_sprite(self.background_sprite, size, position, anchor_point='center')
            else:
                # Fallback background
                bg_surface = py.Surface((self.rect.width, self.rect.height), py.SRCALPHA)
                bg_surface.fill((50, 50, 100, 200))
                py.draw.rect(bg_surface, WHITE, bg_surface.get_rect(), 2)
                self.display_surface.blit(bg_surface, self.rect)

    def draw_highest_level(self):
        """Draw the 'HIGHEST LEVEL X' row"""
        if self.is_active:
            # Draw "HIGHEST" text
            file_name = self.text_sprites['highest']
            width = (300)
            height = (75)
            size = (width, height)
            x = self.display_surface.get_width() // 2 - height + 10
            y = self.display_surface.get_height() // 2 - 150
            position = (x, y)
            draw_ui_sprite(file_name, size, position, anchor_point='center')
            
            # Draw the highest level number
            level_str = str(self.highest_level)
            digit_width = 50
            digit_height = 50
            x_start = self.display_surface.get_width() // 2 - (len(level_str) * digit_width) // 2
            for i, digit_char in enumerate(level_str):
                digit_sprite = self.digits.get(int(digit_char))
                if digit_sprite:
                    digit_x = x_start + i * digit_width
                    digit_y = self.display_surface.get_height() // 2 - 55
                    draw_ui_sprite(digit_sprite, (digit_width, digit_height), (digit_x, digit_y), anchor_point='center')
            
            # Draw "LEVEL" text
            level_file_name = self.text_sprites['level']
            level_width = (300)
            level_height = (75)
            level_size = (level_width, level_height)
            level_x = self.display_surface.get_width() // 2 + height + 20
            level_y = self.display_surface.get_height() // 2 - 150
            level_position = (level_x, level_y)
            draw_ui_sprite(level_file_name, level_size, level_position, anchor_point='center')

    def draw_annihilated(self):
        """Draw the 'ANNIHILATED X' row"""
        if self.is_active:
            # Draw "ANNIHILATED" text
            file_name = self.text_sprites['annihilated']
            width = (300)
            height = (75)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2 + 50
            position = (x, y)
            draw_ui_sprite(file_name, size, position, anchor_point='center')
            
            # Draw the annihilated number (as a string of digits)
            annihilated_str = str(self.annihilated)
            digit_width = 50
            digit_height = 50
            x_start = self.display_surface.get_width() // 2 - (len(annihilated_str) * digit_width) // 2
            for i, digit_char in enumerate(annihilated_str):
                digit_sprite = self.digits.get(int(digit_char))
                if digit_sprite:
                    digit_x = x_start + i * digit_width
                    digit_y = y + 100
                    draw_ui_sprite(digit_sprite, (digit_width, digit_height), (digit_x, digit_y), anchor_point='center')

    def draw_debug_info(self):
        """Draw debug information (optional)"""
        if not self.is_active:
            return
            
        if hasattr(self, 'font') and self.font:
            font = self.font.get('small', py.font.Font(None, 24))
            debug_text = f"Level: {self.highest_level}, Killed: {self.annihilated}"
            debug_surface = font.render(debug_text, True, WHITE)
            debug_rect = debug_surface.get_rect()
            debug_rect.bottomright = (self.display_surface.get_width() - 10, 
                                    self.display_surface.get_height() - 10)
            self.display_surface.blit(debug_surface, debug_rect)

    def display(self):
        """Main display method - draws all popup elements"""
        if self.is_active:
            print(f"MyStatsPopup drawing - Level: {self.highest_level}, Annihilated: {self.annihilated}")
            
            self.background()
            self.draw_highest_level()
            self.draw_annihilated()
            # Uncomment if you want debug info displayed
            # self.draw_debug_info()