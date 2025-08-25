import pygame as py

from support import surface_blit, load_image, load_font
from settings import *

class SettingsPopup():
    def __init__(self):
        self.display_surface = py.display.get_surface()

        self.background_sprite = load_image(settings_background)
        self.settings_sprite = load_image(settings_settings_text)
        self.music_sprite = load_image(settings_music_text)
        self.bar_sprite = load_image(settings_bar_sprite)
        self.bar_knob_sprite = load_image(settings_knob_sprite)

        width = self.display_surface.get_width() // 2
        height = self.display_surface.get_height() // 2
        
        self.rect = py.Rect(
            (self.display_surface.get_width() - width) // 2,
            (self.display_surface.get_height() - height) // 2,
            width,
            height
        )

        self.is_active = False

        self.font = load_font(FONT, FONT_SIZE)

        # Music system variables
        self.music_volume = 0.3  # Default volume (0.0 to 1.0)
        self.sfx_volume = 0.5    # Sound effects volume
        self.music_enabled = True
        self.sfx_enabled = True
        
        # Current music state
        self.current_music = None  # Track what music is currently playing
        self.music_position = 0    # Position in current track
        
        # Slider interaction
        self.dragging_music = False
        self.dragging_sfx = False
        
        # Initialize pygame mixer if not already done
        if not py.mixer.get_init():
            py.mixer.init()

    def play_menu_music(self):
        """Play menu background music"""
        if self.music_enabled and menu_bgm:
            try:
                if self.current_music != "menu":
                    py.mixer.music.load(menu_bgm)
                    py.mixer.music.play(loops=-1)
                    self.current_music = "menu"
                py.mixer.music.set_volume(self.music_volume)
            except py.error as e:
                print(f"Warning: Could not load menu music: {e}")

    def play_game_music(self):
        """Play game background music"""
        if self.music_enabled and game_bgm:
            try:
                if self.current_music != "game":
                    py.mixer.music.load(game_bgm)
                    py.mixer.music.play(loops=-1)
                    self.current_music = "game"
                py.mixer.music.set_volume(self.music_volume)
            except py.error as e:
                print(f"Warning: Could not load game music: {e}")

    def stop_music(self):
        """Stop all music"""
        py.mixer.music.stop()
        self.current_music = None

    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if py.mixer.music.get_busy():
            py.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            py.mixer.music.pause()
        else:
            py.mixer.music.unpause()

    def handle_event(self, event):
        """Handle mouse events for slider interaction"""
        if not self.is_active:
            return
            
        # Music slider bounds
        bar_size = (325, 50)
        bar_pos_x = self.display_surface.get_width() // 2
        bar_pos_y = self.display_surface.get_height() // 2 - 100
        music_slider_rect = py.Rect(
            bar_pos_x - bar_size[0] // 2,
            bar_pos_y - bar_size[1] // 2,
            bar_size[0],
            bar_size[1]
        )
        
        # SFX slider bounds (below music slider)
        sfx_bar_pos_y = bar_pos_y + 80
        sfx_slider_rect = py.Rect(
            bar_pos_x - bar_size[0] // 2,
            sfx_bar_pos_y - bar_size[1] // 2,
            bar_size[0],
            bar_size[1]
        )

        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if music_slider_rect.collidepoint(event.pos):
                    self.dragging_music = True
                    # Calculate new volume based on click position
                    relative_x = event.pos[0] - music_slider_rect.left
                    new_volume = relative_x / bar_size[0]
                    self.set_music_volume(new_volume)
                elif sfx_slider_rect.collidepoint(event.pos):
                    self.dragging_sfx = True
                    # Calculate new SFX volume
                    relative_x = event.pos[0] - sfx_slider_rect.left
                    new_volume = relative_x / bar_size[0]
                    self.set_sfx_volume(new_volume)

        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_music = False
                self.dragging_sfx = False

        elif event.type == py.MOUSEMOTION:
            if self.dragging_music:
                # Update music volume while dragging
                relative_x = event.pos[0] - music_slider_rect.left
                new_volume = max(0.0, min(1.0, relative_x / bar_size[0]))
                self.set_music_volume(new_volume)
            elif self.dragging_sfx:
                # Update SFX volume while dragging
                relative_x = event.pos[0] - sfx_slider_rect.left
                new_volume = max(0.0, min(1.0, relative_x / bar_size[0]))
                self.set_sfx_volume(new_volume)

    def background(self):
        """Draw the settings popup background"""
        if self.is_active:
            file_name = self.background_sprite
            width = (self.display_surface.get_width() // 2)
            height = (self.display_surface.get_height() // 2 + 200)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2
            position = (x, y)
            self.draw_ui_sprite(file_name, size, position, anchor_point='center')

    def draw_music_controls(self):
        """Draw music label and slider"""
        if self.is_active:
            # Music label
            file_name = self.music_sprite
            width = (225)
            height = (50)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2 - 150
            position = (x, y)
            self.draw_ui_sprite(file_name, size, position, anchor_point='center')
            
            # Music slider
            self.draw_slider(
                y_offset=-80,
                volume=self.music_volume,
                label="Music"
            )

    def draw_sfx_controls(self):
        """Draw SFX label and slider"""
        if self.is_active:
            # SFX label (create text since we might not have sprite)
            font = self.font['med']
            sfx_text = font.render("Sound Effects", True, WHITE)
            sfx_rect = sfx_text.get_rect(center=(
                self.display_surface.get_width() // 2,
                self.display_surface.get_height() // 2
            ))
            self.display_surface.blit(sfx_text, sfx_rect)
            
            # SFX slider
            self.draw_slider(
                y_offset= 50,
                volume=self.sfx_volume,
                label="SFX"
            )

    def draw_slider(self, y_offset, volume, label):
        """Draw a volume slider"""
        if self.is_active:
            # Slider bar
            bar_size = (325, 50)
            bar_pos_x = self.display_surface.get_width() // 2
            bar_pos_y = self.display_surface.get_height() // 2 + y_offset
            bar_position = (bar_pos_x, bar_pos_y)

            # Draw the slider bar
            self.draw_ui_sprite(
                self.bar_sprite,
                bar_size,
                bar_position,
                anchor_point='center'
            )

            # Calculate knob position - constrained within slider bounds
            knob_size = (50, 50)
            # Calculate the usable width (bar width minus knob width)
            usable_width = bar_size[0] - knob_size[0]
            # Calculate knob position within bounds
            knob_offset_from_left = int(volume * usable_width)
            knob_pos_x = bar_pos_x - bar_size[0] // 2 + knob_size[0] // 2 + knob_offset_from_left
            knob_pos_y = bar_pos_y
            knob_position = (knob_pos_x, knob_pos_y)

            # Draw the slider knob
            self.draw_ui_sprite(
                self.bar_knob_sprite,
                knob_size,
                knob_position,
                anchor_point='center'
            )

            # Draw volume percentage
            font = self.font['med']
            volume_text = font.render(f"{int(volume * 100)}%", True, WHITE)
            volume_rect = volume_text.get_rect(center=(
                bar_pos_x + bar_size[0] // 2 + 60,
                bar_pos_y
            ))
            self.display_surface.blit(volume_text, volume_rect)

    def draw_toggle_buttons(self):
        """Draw music/SFX toggle buttons"""
        if self.is_active:
            font = self.font['med']
            
            # Music toggle button
            music_color = GREEN if self.music_enabled else RED
            music_text = font.render("Music: ON" if self.music_enabled else "Music: OFF", True, music_color)
            music_rect = music_text.get_rect(center=(
                self.display_surface.get_width() // 2 - 150,
                self.display_surface.get_height() // 2 + 100
            ))
            self.display_surface.blit(music_text, music_rect)
            
            # Store rect for click detection
            self.music_toggle_rect = music_rect
            
            # SFX toggle button
            sfx_color = GREEN if self.sfx_enabled else RED
            sfx_text = font.render("SFX: ON" if self.sfx_enabled else "SFX: OFF", True, sfx_color)
            sfx_rect = sfx_text.get_rect(center=(
                self.display_surface.get_width() // 2 + 150,
                self.display_surface.get_height() // 2 + 100
            ))
            self.display_surface.blit(sfx_text, sfx_rect)
            
            # Store rect for click detection
            self.sfx_toggle_rect = sfx_rect

    def draw_ui_sprite(self, surface, size, position, anchor_point):
        """Helper method to draw UI sprites"""
        if surface:
            scaled = py.transform.scale(surface, size)
            rect = scaled.get_rect(**{anchor_point: position})
            surface_blit(scaled, rect)
            return True
        return False

    def display(self):
        """Main display method - draws all components"""
        if self.is_active:
            self.background()
            self.draw_music_controls()
            self.draw_sfx_controls()
            self.draw_toggle_buttons()
        


        

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