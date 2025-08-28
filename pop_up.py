import pygame as py

from support import surface_blit, load_image, load_font, draw_ui_sprite
from settings import *
from stats import *

class SettingsPopup():
    def _init_sounds(self):
        self.sounds = {
            'laser'    : py.mixer.Sound(laser_sfx),
            'explosion': py.mixer.Sound(explosion_sfx),
            'score'    : py.mixer.Sound(score_sfx),
            'newlevel' : py.mixer.Sound(new_level_sfx),
            'gameover' : py.mixer.Sound(game_over_sfx),
            'hover'    : py.mixer.Sound(hover_sfx),
        }

    def __init__(self):
        self.display_surface = py.display.get_surface()

        self.background_sprite = load_image(settings_background)
        self.settings_sprite = load_image(settings_settings_text)
        self.music_sprite = load_image(settings_music_text)
        self.sound_sprite = load_image(settings_sounds_text)
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

        self.music_volume = 0.3  
        self.sfx_volume = 0.5    
        self.music_enabled = True
        self.sfx_enabled = True
        
        # Current music state
        self.current_music = None  
        self.music_position = 0    

        # Current sound state
        self.current_sound = None
        self.sound_position = 0
        
        # Slider interaction
        self.dragging_music = False
        self.dragging_sfx = False
        
        if not py.mixer.get_init():
            py.mixer.init()

        self.sounds = {}
        self._init_sounds()
    
    def play_menu_music(self):
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
        if self.music_enabled and game_bgm:
            try:
                if self.current_music != "play":
                    py.mixer.music.load(game_bgm)
                    py.mixer.music.play(loops=-1)
                    self.current_music = "play"
                py.mixer.music.set_volume(self.music_volume)
            except py.error as e:
                print(f"Warning: Could not load game music: {e}")

    def stop_music(self):
        py.mixer.music.stop()
        self.current_music = None

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if py.mixer.music.get_busy():
            py.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for key, snd in self.sounds.items():
            if key == 'explosion':
                snd.set_volume(self.sfx_volume * 1.8)
            else:
                snd.set_volume(self.sfx_volume)

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            py.mixer.music.pause()
        else:
            py.mixer.music.unpause()

    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled
        if not self.sfx_enabled:
            for sound in self.sounds.values():
                sound.set_volume(0)  # Mute all sounds
        else:
            self.set_sfx_volume(self.sfx_volume)

    def handle_event(self, event):
        if not self.is_active:
            return
            
        # Music slider bounds
        bar_size = (325, 50)
        bar_pos_x = self.display_surface.get_width() // 2
        bar_pos_y = self.display_surface.get_height() // 2 - 80
        music_slider_rect = py.Rect(
            bar_pos_x - bar_size[0] // 2,
            bar_pos_y - bar_size[1] // 2,
            bar_size[0],
            bar_size[1]
        )
        
        sfx_bar_pos_y = self.display_surface.get_height() // 2 + 70

        sfx_slider_rect = py.Rect(
            bar_pos_x - bar_size[0] // 2,
            sfx_bar_pos_y - bar_size[1] // 2,
            bar_size[0],
            bar_size[1]
        )

        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                if music_slider_rect.collidepoint(event.pos):
                    self.dragging_music = True
                    print(self.dragging_music, "Dragging Music")
                    relative_x = event.pos[0] - music_slider_rect.left
                    new_volume = relative_x / bar_size[0]
                    self.set_music_volume(new_volume)
                elif sfx_slider_rect.collidepoint(event.pos):
                    self.dragging_sfx = True
                    print(self.dragging_sfx, "Dragging Sounds")
                    relative_x = event.pos[0] - sfx_slider_rect.left
                    new_volume = relative_x / bar_size[0]
                    self.set_sfx_volume(new_volume)

        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_music = False
                self.dragging_sfx = False

        elif event.type == py.MOUSEMOTION:
            if self.dragging_music:
                relative_x = event.pos[0] - music_slider_rect.left
                new_volume = max(0.0, min(1.0, relative_x / bar_size[0]))
                self.set_music_volume(new_volume)
            elif self.dragging_sfx:
                relative_x = event.pos[0] - sfx_slider_rect.left
                new_volume = max(0.0, min(1.0, relative_x / bar_size[0]))
                self.set_sfx_volume(new_volume)

    def background(self):
        if self.is_active:
            file_name = self.background_sprite
            width = (self.display_surface.get_width() // 2 + 75)
            height = (self.display_surface.get_height() // 2 + 200)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2
            position = (x, y)
            draw_ui_sprite(file_name, size, position, anchor_point='center')

    def draw_music_controls(self):
        if self.is_active:
            file_name = self.music_sprite
            width = (225)
            height = (50)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2 - 150
            position = (x, y)
            draw_ui_sprite(file_name, size, position, anchor_point='center')
            
            self.draw_slider(
                y_offset=-80,
                volume=self.music_volume,
                label="Music"
            )

    def draw_sfx_controls(self):
        if self.is_active:
            file_name = self.sound_sprite
            width = (225)
            height = (50)
            size = (width, height)
            x = self.display_surface.get_width() // 2
            y = self.display_surface.get_height() // 2
            position = (x, y)
            draw_ui_sprite(file_name, size, position, anchor_point='center')
            
            self.draw_slider(
                y_offset= 70,
                volume=self.sfx_volume,
                label="Sound"
            )

    def draw_slider(self, y_offset, volume, label):
        if self.is_active:
            bar_size = (325, 50)
            bar_pos_x = self.display_surface.get_width() // 2
            bar_pos_y = self.display_surface.get_height() // 2 + y_offset
            bar_position = (bar_pos_x, bar_pos_y)

            draw_ui_sprite(
                self.bar_sprite,
                bar_size,
                bar_position,
                anchor_point='center'
            )

            knob_size = (50, 50)
            usable_width = bar_size[0] - knob_size[0]
            knob_offset_from_left = int(volume * usable_width)
            knob_pos_x = bar_pos_x - bar_size[0] // 2 + knob_size[0] // 2 + knob_offset_from_left
            knob_pos_y = bar_pos_y
            knob_position = (knob_pos_x, knob_pos_y)

            draw_ui_sprite(
                self.bar_knob_sprite,
                knob_size,
                knob_position,
                anchor_point='center'
            )

            font = self.font['med']
            volume_text = font.render(f"{int(volume * 100)}%", True, WHITE)
            volume_rect = volume_text.get_rect(center=(
                bar_pos_x + bar_size[0] // 2 + 20,
                bar_pos_y
            ))
            self.display_surface.blit(volume_text, volume_rect)

    def draw_toggle_buttons(self):
        if self.is_active:
            font = self.font['med']
            
            music_color = GREEN if self.music_enabled else RED
            music_text = font.render("Music: ON" if self.music_enabled else "Music: OFF", True, music_color)
            music_rect = music_text.get_rect(center=(
                self.display_surface.get_width() // 2 - 100,
                self.display_surface.get_height() // 2 + 150
            ))
            self.display_surface.blit(music_text, music_rect)
            
            self.music_toggle_rect = music_rect
            
            sfx_color = GREEN if self.sfx_enabled else RED
            sfx_text = font.render("SFX: ON" if self.sfx_enabled else "SFX: OFF", True, sfx_color)
            sfx_rect = sfx_text.get_rect(center=(
                self.display_surface.get_width() // 2 + 100,
                self.display_surface.get_height() // 2 + 150
            ))
            self.display_surface.blit(sfx_text, sfx_rect)
            
            self.sfx_toggle_rect = sfx_rect

    def display(self):
        if self.is_active:
            self.background()
            self.draw_sfx_controls()
            self.draw_music_controls()
            self.draw_toggle_buttons()