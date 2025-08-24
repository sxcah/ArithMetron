# main

import pygame, sys, random, os, math
from settings import *
from animated_sprite import AnimatedSprite

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

'''menu_bgm = r"bgm.mp3"
game_bgm = r"game_bgm.mp3"'''

menu_bgm = None
game_bgm = None

def play_menu_music():
    try:
        pygame.mixer.music.load(menu_bgm)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
    except pygame.error as e:
        print(f"Warning: Could not load menu music: {e}")

def play_game_music():
    """Plays the game BGM."""
    try:
        pygame.mixer.music.load(game_bgm)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)
    except pygame.error as e:
        print(f"Warning: Could not load game music: {e}")

def stop_music():
    pygame.mixer.music.stop()


player_filenames = ["player1.png", "player2.png"]
enemy_filenames = ["enemy1.png", "enemy2.png"]
explosion_filenames = ["explosion.png"]
laser_filenames = ["lazer.png"]
levels_filename = "levels.png"
settings_filename = "settings.png"
my_stats_filename = "my_stats.png"
quit_filename = "quit.png"

def load_frames(filenames, default_color, is_player=True):
    frames = []
    script_dir = "" 
    
    try:
        for filename in filenames:
            path = os.path.join(script_dir, filename)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            frames.append(img)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Warning: Could not load assets: {e}. Using placeholders.")
        frames = []
        for i in range(4):
            surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            if is_player:
                pygame.draw.circle(surf, SHIP_COLOR, (30, 30), 30)
                pulsing_color = (100 + i*20, 180 + i*10, 255 - i*20)
                pygame.draw.circle(surf, pulsing_color, (30, 30), 20)
            else:
                pygame.draw.rect(surf, ENEMY_COLOR, (0, 0, 60, 60), border_radius=15)
                pulsing_color = (255 - i*20, 120 + i*10, 120 + i*20)
                pygame.draw.rect(surf, pulsing_color, (10, 10, 40, 40), border_radius=10)
            frames.append(surf)

    return frames

def load_button_images(base_name, scale=None):
    states = {}
    suffixes = {"default": "default", "pressed1": "pressed1", "pressed2": "pressed2"}
    for state, suffix in suffixes.items():
        filename = f"{base_name}_{suffix}.png"
        try:
            img = pygame.image.load(filename).convert_alpha()
            if scale:
                img = pygame.transform.scale(img, scale)
            states[state] = img
        except Exception as e:
            print(f"Warning: Could not load {filename}: {e}")
            surf = pygame.Surface(scale, pygame.SRCALPHA)
            surf.fill((200, 50, 50))
            font = pygame.font.Font(None, 24)
            text_surf = font.render(base_name.capitalize(), True, WHITE)
            text_rect = text_surf.get_rect(center=(surf.get_width() // 2, surf.get_height() // 2))
            surf.blit(text_surf, text_rect)
            states[state] = surf
    return states

def load_static_button(filename, scale=None):
    try:
        img = pygame.image.load(filename).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        surf = pygame.Surface(scale, pygame.SRCALPHA)
        surf.fill(LIGHT_PURPLE) 
        font = pygame.font.Font(None, 24)
        text_surf = font.render(filename.split('.')[0].capitalize().replace('_', ' '), True, GOLD)
        text_rect = text_surf.get_rect(center=(surf.get_width() // 2, surf.get_height() // 2))
        surf.blit(text_surf, text_rect)
        return surf

def generate_problem(score):
    if score <= 100:
        ops = ["+"]
        a = random.randint(1, 10)
        b = random.randint(1, 10)
    elif score <= 200:
        ops = ["+", "-"]
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        if random.choice(ops) == "-":
            a, b = max(a, b), min(a, b)
    else:
        ops = ["+", "-", "*"]
        a = random.randint(2, 12)
        b = random.randint(2, 12)

    op = random.choice(ops)
    if op == "+":
        ans = a + b
        q = f"{a}+{b}"
    elif op == "-":
        ans = a - b
        q = f"{a}-{b}"
    else:
        ans = a * b
        q = f"{a}×{b}"

    return q, ans

class Button(pygame.sprite.Sprite):
    def __init__(self, states, position, action=None):
        super().__init__()
        self.states = states
        self.current_state = "default"
        self.image = self.states[self.current_state]
        self.rect = self.image.get_rect(center=position)
        self.action = action
        self.state_change_time = 0
        self.transitioning = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.transitioning:
            if self.rect.collidepoint(event.pos):
                self.start_transition()

    def start_transition(self):
        self.transitioning = True
        self.current_state = "pressed1"
        self.image = self.states[self.current_state]
        self.state_change_time = pygame.time.get_ticks()

    def update(self):
        if self.transitioning:
            now = pygame.time.get_ticks()
            if self.current_state == "pressed1" and now - self.state_change_time > 100: 
                self.current_state = "pressed2"
                self.image = self.states[self.current_state]
                self.state_change_time = now
            elif self.current_state == "pressed2" and now - self.state_change_time > 100:
                if self.action:
                    self.action()
                self.transitioning = False
                self.current_state = "default"
                self.image = self.states[self.current_state]

class AnimatedEnemy(AnimatedSprite):
    def __init__(self, frames, font, score, speed):
        super().__init__(frames, random.randint(40, SCREEN_WIDTH - 140), -100, speed)
        self.font = font
        self.question, self.answer = generate_problem(score)
        
        self.text_surf = self.font.render(self.question, True, TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery))

    def update(self, dt):
        super().update(dt)
        self.text_rect.center = (self.rect.centerx, self.rect.centery)

    def draw_text(self, screen):
        box_padding = 5
        box_rect = self.text_rect.inflate(box_padding * 2, box_padding * 2)
        s = pygame.Surface(box_rect.size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        screen.blit(s, box_rect.topleft)
        screen.blit(self.text_surf, self.text_rect)

class Laser(AnimatedSprite):
    def __init__(self, frames, start_pos, target_pos):
        super().__init__(frames, start_pos[0], start_pos[1])
        self.animation_speed = 30
        
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude > 0:
            dx /= magnitude
            dy /= magnitude
        
        self.speed = 15
        self.speed_x = dx * self.speed
        self.speed_y = dy * self.speed
        
        self.rotate_to(target_pos)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.frames:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.original_frames[self.frame_index]
                self.image = pygame.transform.rotate(self.image, self.rotation)
        
        if not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(self.rect):
            self.kill()

class Explosion(AnimatedSprite):
    def __init__(self, frames, pos):
        super().__init__(frames, pos[0], pos[1])
        self.animation_speed = 50
        self.one_time_animation_done = False

    def update(self, dt):
        if not self.one_time_animation_done:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index += 1
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.frame_index]
                else:
                    self.one_time_animation_done = True
                    self.kill()

class Spaceship(AnimatedSprite):
    def __init__(self, frames, position):
        super().__init__(frames, position[0], position[1])
        self.speed = -5 

    def update(self, dt):
        super().update(dt)

class SettingsPopup:
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
            screen.blit(text, text_rect)

class MyStatsPopup:
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
            text = font.render("My Stats (Empty)", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

class LevelsSlideWindow:
    def __init__(self):
        self.is_active = False
        self.rect = pygame.Rect(SCREEN_WIDTH, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
        self.slide_speed = 10
        self.buttons = []
        self.create_buttons()
    
    def create_buttons(self):
        button_y = 100
        for i in range(1, 7):
            font = pygame.font.Font(None, 36)
            text_surface = font.render(f"Test {i}", True, WHITE)
            button = pygame.sprite.Sprite()
            button.image = text_surface
            button.rect = button.image.get_rect(center=(self.rect.centerx, button_y))
            self.buttons.append(button)
            button_y += 75

    def update(self):
        if self.is_active and self.rect.x > SCREEN_WIDTH * 2 // 3:
            self.rect.x -= self.slide_speed
        elif not self.is_active and self.rect.x < SCREEN_WIDTH:
            self.rect.x += self.slide_speed
    
    def draw(self, screen):
        if self.rect.x < SCREEN_WIDTH:
            pygame.draw.rect(screen, LIGHT_PURPLE, self.rect)
            for button in self.buttons:
                button.rect.centerx = self.rect.centerx
                screen.blit(button.image, button.rect)
    
    def handle_event(self, event):
        if self.is_active:
            for button in self.buttons:
                if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                    print(f"Level {button.rect.centery} clicked!")

from ui import UI
from input_box import InputBox

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Arithmetron")
        self.clock = pygame.time.Clock()
        self.game_state = "menu"
        self.is_animation_finished = False
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(120)]

        play_menu_music()

        self.font_big = pygame.font.Font(None, 48)
        self.font_med = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        self.menu_background = pygame.Surface(SCREEN_SIZE)
        self.menu_background.fill(DARK_PURPLE)
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.rect(self.menu_background, WHITE, (x, y, 2, 2))
        
        self.game_background = pygame.Surface(SCREEN_SIZE)
        self.game_background.fill(DARK_BLUE)

        self.player_frames = load_frames(player_filenames, SHIP_COLOR, is_player=True)
        self.enemy_frames = load_frames(enemy_filenames, ENEMY_COLOR, is_player=False)
        self.explosion_frames = load_frames(explosion_filenames, (255, 165, 0), is_player=False)
        self.laser_frames = load_frames(laser_filenames, (255, 50, 50), is_player=False)
        
        self.play_button_size = (180, 120)
        self.levels_button_size = (180, 40)
        self.settings_button_size = (320, 40)
        self.my_stats_button_size = (320, 40)
        self.quit_button_size = (140, 40)

        play_button_states = load_button_images("play", scale=self.play_button_size)
        levels_img   = load_static_button(levels_filename,   scale=self.levels_button_size)
        settings_img = load_static_button(settings_filename, scale=self.settings_button_size)
        my_stats_img = load_static_button(my_stats_filename, scale=self.my_stats_button_size)
        quit_img     = load_static_button(quit_filename,     scale=self.quit_button_size)

        self.spaceship_initial_y = SCREEN_HEIGHT * 0.25 
        self.spaceship = AnimatedSprite(self.player_frames, SCREEN_WIDTH // 2, self.spaceship_initial_y)
        self.spaceship_group = pygame.sprite.GroupSingle(self.spaceship)
        
        self.buttons = pygame.sprite.Group()
        self.menu_buttons_y_start = self.spaceship_initial_y + 150 
        self.button_spacing = 105
        
        button_data = [
                    ("Play", 
                    play_button_states, 
                    self.start_play_animation),

                    ("Levels",
                    levels_img,
                    self.toggle_levels),

                    ("Settings",
                    settings_img,
                    self.toggle_settings),

                    ("My Stats",
                    my_stats_img,
                    self.toggle_stats),

                    ("Quit",
                    quit_img,
                    self.quit_game)
                ]
        
        self.create_menu_buttons(button_data)
        
        self.title_surf = self.font_big.render("Arithmetron", True, GOLD)
        self.title_rect = self.title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.12))

        self.spaceship_launch_speed = -9
        self.menu_animation_speed = 40
        
        self.game_over = False
        self.paused = False
        self.victory = False
        self.score = 0
        self.lives = LIVES
        self.current_stage_index = 0
        self.enemies_cleared_in_stage = 0
        self.stage_completed = 0
        self.stage_to_complete = len(DIFFICULTY_STAGES)

        self.levels_window = LevelsSlideWindow()
        self.settings_popup = SettingsPopup()
        self.stats_popup = MyStatsPopup()
        self.input_box = InputBox(
            x=(SCREEN_WIDTH - 200) // 2,
            y=SCREEN_HEIGHT - 50,
            width=200,
            height=40,
            font=self.font_med
        )

        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.ui = UI()

    def create_menu_buttons(self, button_data):
        for i, (item, image_data, action) in enumerate(button_data):
            y_position = self.menu_buttons_y_start + i * self.button_spacing
            
            if isinstance(image_data, dict):
                button = Button(image_data, (SCREEN_WIDTH // 2, y_position), action)
                self.buttons.add(button)
            else:
                button = pygame.sprite.Sprite()
                button.image = image_data
                button.rect = button.image.get_rect(center=(SCREEN_WIDTH // 2, y_position))
                self.buttons.add(button)
                button.action = action

    def _handle_simple_button(self, event, action, rect):
        if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
            action()
    
    def reset_game(self):
        self.game_state = "play"
        self.game_over = False
        self.paused = False
        self.victory = False
        self.score = 0
        self.lives = LIVES
        self.ui.reset_lives()
        self.current_stage_index = 0
        self.stage_completed = 0
        self.enemies_cleared_in_stage = 0
        self.enemies.empty()
        self.lasers.empty()
        self.explosions.empty()
        self.all_sprites.empty()
        self.enemies_spawned_in_stage = 0
        
        self.player = AnimatedSprite(self.player_frames, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.all_sprites.add(self.player)
        
        self.current_stage = DIFFICULTY_STAGES[self.current_stage_index]
        pygame.time.set_timer(SPAWN_EVENT, self.current_stage["spawn_interval"])
        
        play_game_music()

    def update_menu_animation(self, dt):
        self.title_rect.y += self.menu_animation_speed
        for button in self.buttons:
            if isinstance(button, Button):
                 button.update()
            button.rect.y += self.menu_animation_speed
        
        self.spaceship_group.update(dt)
        self.spaceship.rect.y += self.spaceship_launch_speed

        if self.spaceship.rect.bottom <= 0:
            stop_music()
            self.reset_game()

    def start_play_animation(self):
        self.game_state = "play_animation"
        self.is_animation_finished = False
        self.spaceship.rect.center = (SCREEN_WIDTH // 2, self.spaceship_initial_y) 
        self.title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.12)
        for i, button in enumerate(self.buttons):
            if isinstance(button, Button):
                 button.rect.centery = self.menu_buttons_y_start + i * self.button_spacing
            else:
                 button.rect.centery = self.menu_buttons_y_start + i * self.button_spacing
    
    def toggle_levels(self):
        self.levels_window.is_active = not self.levels_window.is_active
    
    def toggle_settings(self):
        self.settings_popup.is_active = not self.settings_popup.is_active
        if self.settings_popup.is_active:
            self.stats_popup.is_active = False

    def toggle_stats(self):
        self.stats_popup.is_active = not self.stats_popup.is_active
        if self.stats_popup.is_active:
            self.settings_popup.is_active = False

    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        submitted_text = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # Handle pause toggle in play state (before other game state checks)
            if self.game_state == "play" and not self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = not self.paused
                    return submitted_text
            
            if self.game_state == "menu":
                for button in self.buttons:
                    if isinstance(button, Button):
                        button.handle_event(event)
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                            if hasattr(button, 'action'):
                                button.action()
                self.levels_window.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN and (self.settings_popup.is_active or self.stats_popup.is_active):
                    if not self.settings_popup.rect.collidepoint(event.pos) and not self.stats_popup.rect.collidepoint(event.pos):
                        self.settings_popup.is_active = False
                        self.stats_popup.is_active = False

            elif self.game_state == "play" and not self.game_over and not self.paused:
                submitted_text = self.input_box.handle_event(event)
                # Enemy spawning only happens when not paused
                if event.type == SPAWN_EVENT and self.enemies_spawned_in_stage < self.current_stage["enemies_to_clear"]:
                    e = AnimatedEnemy(self.enemy_frames, self.font_med, self.score, self.current_stage["enemy_speed"])
                    self.enemies.add(e)
                    self.all_sprites.add(e)
                    self.enemies_spawned_in_stage += 1
            
            elif self.game_state == "game_cleared":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.return_to_menu()
            
            elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.return_to_menu()

            elif self.game_state == "level_cleared":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Changed from K_SPACE to K_RETURN
                    self.proceed_to_next_stage()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.return_to_menu()

        return submitted_text

    def check_stage_completion(self):
        """Check if the current stage is completed and handle transition"""
        if self.enemies_cleared_in_stage >= self.current_stage["enemies_to_clear"]:
            # Check if all stages are completed
            if self.current_stage_index >= len(DIFFICULTY_STAGES) - 1:
                # All stages completed - transition to game cleared state
                self.game_state = "game_cleared"
                self.victory = True
                self.input_box.active = False
                pygame.time.set_timer(SPAWN_EVENT, 0)  # Stop spawning enemies
            else:
                # Stage cleared but more stages remain
                self.game_state = "level_cleared"
                pygame.time.set_timer(SPAWN_EVENT, 0)  # Stop spawning enemies temporarily

    def proceed_to_next_stage(self):
        """Proceed to the next stage after level cleared screen"""
        self.current_stage_index += 1
        self.enemies_cleared_in_stage = 0
        self.enemies_spawned_in_stage = 0
        
        if self.current_stage_index < len(DIFFICULTY_STAGES):
            self.current_stage = DIFFICULTY_STAGES[self.current_stage_index]
            pygame.time.set_timer(SPAWN_EVENT, self.current_stage["spawn_interval"])
            self.game_state = "play"  # Return to play state
            self.input_box.active = True  # Reactivate input

    def return_to_menu(self):
        """Better method to return to menu from any state"""
        self.game_state = "menu"
        self.game_over = False
        self.paused = False
        self.victory = False
        self.buttons.empty()
        
        # Reset button sizes and recreate them
        self.play_button_size = (180, 140)
        self.levels_button_size = (160, 60)
        self.settings_button_size = (180, 60)
        self.my_stats_button_size = (180, 60)
        self.quit_button_size = (150, 50)
        
        play_button_states = load_button_images("play", scale=self.play_button_size)
        levels_img   = load_static_button(levels_filename,   scale=self.levels_button_size)
        settings_img = load_static_button(settings_filename, scale=self.settings_button_size)
        my_stats_img = load_static_button(my_stats_filename, scale=self.my_stats_button_size)
        quit_img     = load_static_button(quit_filename,     scale=self.quit_button_size)

        self.spaceship_initial_y = SCREEN_HEIGHT * 0.25
        self.spaceship = AnimatedSprite(self.player_frames, SCREEN_WIDTH // 2, self.spaceship_initial_y)
        self.spaceship_group = pygame.sprite.GroupSingle(self.spaceship)

        self.buttons = pygame.sprite.Group()
        self.menu_buttons_y_start = self.spaceship_initial_y + 150
        self.button_spacing = 100 

        button_data = [
            ("Play", play_button_states, self.start_play_animation),
            ("Levels", levels_img, self.toggle_levels),
            ("Settings", settings_img, self.toggle_settings),
            ("My Stats", my_stats_img, self.toggle_stats),
            ("Quit", quit_img, self.quit_game)
        ]
        
        self.create_menu_buttons(button_data)
        
        self.spaceship = AnimatedSprite(self.player_frames, SCREEN_WIDTH // 2, self.spaceship_initial_y)
        self.spaceship_group.add(self.spaceship)
        
        play_menu_music()

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            submitted_text = self.handle_events()

            if self.game_state == "menu":
                self.screen.blit(self.menu_background, (0, 0))
                
                self.screen.blit(self.title_surf, self.title_rect)
                self.spaceship_group.update(dt) 
                self.spaceship_group.draw(self.screen)
                
                for button in self.buttons:
                    if isinstance(button, Button):
                         button.update()
                
                self.buttons.draw(self.screen)

                self.levels_window.update()
                self.levels_window.draw(self.screen)
                self.settings_popup.draw(self.screen)
                self.stats_popup.draw(self.screen)
            
            elif self.game_state == "play_animation":
                self.screen.blit(self.menu_background, (0, 0))
                
                self.screen.blit(self.title_surf, self.title_rect)

                self.update_menu_animation(dt) 
                
                self.buttons.draw(self.screen)
                self.spaceship_group.draw(self.screen)
                
                if self.spaceship.rect.bottom <= 0:
                    self.reset_game()
            
            elif self.game_state == "play":
                if not self.game_over and not self.paused:
                    self.all_sprites.update(dt)
                    self.input_box.update(dt)
                    
                    if submitted_text is not None:
                        try:
                            typed_val = int(submitted_text)
                        except ValueError:
                            typed_val = None
                        
                        if typed_val is not None:
                            matched = None
                            closest_y = -1
                            for e in self.enemies:
                                if typed_val == e.answer and e.rect.y > closest_y:
                                    closest_y = e.rect.y
                                    matched = e
                            if matched:
                                self.player.rotate_to(matched.rect.center)
                                laser = Laser(self.laser_frames, self.player.rect.center, matched.rect.center)
                                self.lasers.add(laser)
                                self.all_sprites.add(laser)

                    # Handle Hits for hitting enemy
                    hits = pygame.sprite.groupcollide(self.lasers, self.enemies, True, True)
                    for laser, enemies_hit in hits.items():
                        for enemy in enemies_hit:
                            explosion = Explosion(self.explosion_frames, enemy.rect.center)
                            self.explosions.add(explosion)
                            self.all_sprites.add(explosion)
                            
                            self.score += 10
                            self.enemies_cleared_in_stage += 1

                            self.check_stage_completion()

                    # Handles Losing Life
                    for e in list(self.enemies):
                        if e.rect.bottom >= SCREEN_HEIGHT - 60:
                            self.enemies.remove(e)
                            self.all_sprites.remove(e)
                            self.ui.lose_life()
                            self.lives = self.ui.lives
                            self.input_box.text = ""
                            self.enemies_spawned_in_stage -= 1
                            if self.lives <= 0:
                                self.game_over = True
                                self.input_box.active = False
                
                self.screen.blit(self.game_background, (0, 0))
                self.stars = [((x - 1) % SCREEN_WIDTH, (y + 1) % SCREEN_HEIGHT) for (x, y) in self.stars]
                for (x, y) in self.stars:
                    self.screen.fill((200, 200, 220), (x, y, 2, 2))

                pygame.draw.line(self.screen, (60, 80, 120), (0, SCREEN_HEIGHT - 60), (SCREEN_WIDTH, SCREEN_HEIGHT - 60), 2)
                self.all_sprites.draw(self.screen)
                self.input_box.draw(self.screen)
                
                for enemy in self.enemies:
                    enemy.draw_text(self.screen)

                self.ui.display(stage_number=self.current_stage_index + 1, score=self.score)

                if self.paused:
                    pause_overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
                    pause_overlay.fill((0, 0, 0, 128))  # Semi-transparent black
                    self.screen.blit(pause_overlay, (0, 0))
                    
                    pause_text = self.font_big.render("PAUSED", True, WHITE)
                    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    self.screen.blit(pause_text, pause_rect)
                    
                    resume_text = self.font_med.render("Press P to Resume", True, TEXT_COLOR)
                    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                    self.screen.blit(resume_text, resume_rect)

                if self.game_over:
                    over = self.font_big.render("GAME OVER", True, (255, 180, 180))
                    hint = self.font_small.render("Press R to Restart", True, (230, 230, 240))
                    self.screen.blit(over, over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10)))
                    self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 26)))

            elif self.game_state == "game_cleared":
                # Draw the game background with victory screen
                self.screen.blit(self.game_background, (0, 0))
                
                # Draw stars
                self.stars = [((x - 1) % SCREEN_WIDTH, (y + 1) % SCREEN_HEIGHT) for (x, y) in self.stars]
                for (x, y) in self.stars:
                    self.screen.fill((200, 200, 220), (x, y, 2, 2))

                # Continue updating and drawing sprites for visual effect
                self.all_sprites.update(dt)
                self.all_sprites.draw(self.screen)

                # Victory overlay
                victory_overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
                victory_overlay.fill((0, 50, 0, 180))  # Semi-transparent green
                self.screen.blit(victory_overlay, (0, 0))
                
                # Victory text
                victory_text = self.font_big.render("VICTORY!", True, (255, 255, 100))
                victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
                self.screen.blit(victory_text, victory_rect)
                
                # All stages cleared text
                cleared_text = self.font_med.render("All Stages Cleared!", True, (200, 255, 200))
                cleared_rect = cleared_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(cleared_text, cleared_rect)
                
                # Final score
                final_score_text = self.font_med.render(f"Final Score: {self.score}", True, (255, 255, 255))
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(final_score_text, final_score_rect)
                
                # Instructions
                restart_text = self.font_small.render("Press R to Return to Menu", True, (230, 230, 240))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(restart_text, restart_rect)

            elif self.game_state == "level_cleared":
                # Draw the game background with victory screen
                self.screen.blit(self.game_background, (0, 0))
                
                # Draw stars
                self.stars = [((x - 1) % SCREEN_WIDTH, (y + 1) % SCREEN_HEIGHT) for (x, y) in self.stars]
                for (x, y) in self.stars:
                    self.screen.fill((200, 200, 220), (x, y, 2, 2))

                # Continue updating and drawing sprites for visual effect
                self.all_sprites.update(dt)
                self.all_sprites.draw(self.screen)

                # Victory overlay
                victory_overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
                victory_overlay.fill((0, 50, 0, 180))  # Semi-transparent green
                self.screen.blit(victory_overlay, (0, 0))
                
                # Victory text
                victory_text = self.font_big.render("VICTORY!", True, (255, 255, 100))
                victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
                self.screen.blit(victory_text, victory_rect)
                
                # All stages cleared text
                cleared_text = self.font_med.render("Stage Cleared", True, (200, 255, 200))
                cleared_rect = cleared_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
                self.screen.blit(cleared_text, cleared_rect)
                
                # Final score
                final_score_text = self.font_med.render(f"Current Score: {self.score}", True, (255, 255, 255))
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(final_score_text, final_score_rect)
                
                # Instructions
                next_stage_text = self.font_small.render("Press Enter to Continue to next Stage", True, (230, 230, 240))
                next_stage_rect = next_stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(next_stage_text, next_stage_rect)

                return_text = self.font_small.render("Press R to return to menu", True, (230, 230, 240))
                return_text_rect = return_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
                self.screen.blit(return_text, return_text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)
if __name__ == "__main__":
    game = Game()
    game.run()