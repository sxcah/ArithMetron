import pygame
import random
import math
import os
from animated_sprite import AnimatedSprite

class PowerUp(AnimatedSprite):
    def __init__(self, frames, x, y, powerup_type="slow"):
        super().__init__(frames, x, y, speed=1)  # Slow downward movement
        self.powerup_type = powerup_type
        self.animation_speed = 150  # Slower animation for visibility
        self.lifetime = 8000  # 8 seconds before disappearing
        self.spawn_time = pygame.time.get_ticks()
        self.bob_offset = 0
        self.bob_speed = 0.003
        self.original_y = y
        
        # Visual effects
        self.glow_radius = 30
        self.glow_alpha = 100
        self.pulse_direction = 1

    def update(self, dt):
        # Basic movement and animation
        super().update(dt)
        
        # Bobbing effect
        self.bob_offset += self.bob_speed * dt
        self.rect.y = self.original_y + math.sin(self.bob_offset) * 5
        self.original_y += self.speed
        
        # Pulsing glow effect
        self.glow_alpha += self.pulse_direction * 2
        if self.glow_alpha >= 150:
            self.pulse_direction = -1
        elif self.glow_alpha <= 50:
            self.pulse_direction = 1
        
        # Check if powerup should expire
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()
        
        # Remove if off screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

    def draw_glow(self, screen):
        glow_surf = pygame.Surface((self.glow_radius * 2, self.glow_radius * 2), pygame.SRCALPHA)
        
        # Create gradient glow based on powerup type
        for i in range(self.glow_radius):
            alpha = int(self.glow_alpha * (1 - i / self.glow_radius))
            if self.powerup_type == "slow":
                color = (0, 150, 255, alpha)  # Blue glow for slow powerup
            elif self.powerup_type == "bomb":
                color = (255, 50, 50, alpha)  # Red glow for bomb powerup
            else:
                color = (255, 255, 0, alpha)  # Yellow glow for other types
            
            pygame.draw.circle(glow_surf, color, 
                             (self.glow_radius, self.glow_radius), 
                             self.glow_radius - i)
        
        glow_rect = glow_surf.get_rect(center=self.rect.center)
        screen.blit(glow_surf, glow_rect)

class PowerUpManager:
    def __init__(self):
        self.powerups = pygame.sprite.Group()
        self.active_effects = {}
        self.stored_powerups = []  # Store claimed but unused powerups
        self.max_stored = 1  # Changed to 1 to prevent collecting new power-ups if one is stored
        self.slow_effect_duration = 5000  # 5 seconds
        self.slow_factor = 0.3  # Enemies move at 30% speed when slowed
        
    def create_powerup_frames(self, powerup_type="slow"):
        frames = []
        if powerup_type == "slow":
            image_path = r"assets\powerups\POWERUP-Clock.png"
        elif powerup_type == "bomb":
            image_path = r"assets\powerups\POWERUP-Bomb.png"
        else:
            image_path = r"assets\powerups\POWERUP-Clock.png"  # Fallback to clock
        
        try:
            # Try to load the powerup image
            img = pygame.image.load(image_path).convert_alpha()
            # Scale to appropriate size
            img = pygame.transform.scale(img, (40, 40))
            
            # Create 4 frames with slight rotation for animation effect
            for i in range(4):
                rotated_img = pygame.transform.rotate(img, i * 5)  # Slight rotation for each frame
                frames.append(rotated_img)
                
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load {powerup_type} powerup image: {e}. Using placeholder.")
            # Fallback to original diamond shapes if image can't be loaded
            for i in range(4):
                surf = pygame.Surface((40, 40), pygame.SRCALPHA)
                points = [
                    (20, 5),   # top
                    (35, 20),  # right
                    (20, 35),  # bottom
                    (5, 20)    # left
                ]
                
                # Rotating color based on frame and powerup type
                base_color = 150 + i * 20
                if powerup_type == "slow":
                    color = (base_color % 255, (base_color + 85) % 255, (base_color + 170) % 255)
                elif powerup_type == "bomb":
                    color = (255, 50, 50)  # Red for bomb
                else:
                    color = (base_color % 255, (base_color + 85) % 255, (base_color + 170) % 255)
                pygame.draw.polygon(surf, color, points)
                
                # Inner glow
                inner_points = [
                    (20, 10),
                    (30, 20),
                    (20, 30),
                    (10, 20)
                ]
                inner_color = (255, 255, 255, 150)
                pygame.draw.polygon(surf, inner_color, inner_points)
                
                frames.append(surf)
        
        return frames
    
    def spawn_powerup(self, x, y, powerup_type="slow"):
        # Randomly select powerup type if not specified
        if powerup_type == "random":
            powerup_type = random.choice(["slow", "bomb"])
        frames = self.create_powerup_frames(powerup_type)
        powerup = PowerUp(frames, x, y, powerup_type)
        self.powerups.add(powerup)
        return powerup
    
    def auto_claim_powerup(self, chance=0.2):
        if random.random() < chance:
            if len(self.stored_powerups) < self.max_stored:
                powerup_type = random.choice(["slow", "bomb"])
                self.stored_powerups.append(powerup_type)
                return powerup_type
        return None
    
    def use_stored_powerup(self):
        if self.stored_powerups:
            powerup_type = self.stored_powerups.pop(0)
            if powerup_type == "slow":
                self.activate_slow_effect()
                return True
            elif powerup_type == "bomb":
                return True  
        return False
    
    def has_stored_powerups(self):
        return len(self.stored_powerups) > 0
    
    def get_stored_count(self):
        return len(self.stored_powerups)
    
    def check_player_collision(self, player_sprite):
        if self.has_stored_powerups():  # Prevent collecting if a power-up is stored
            return None
        collected = pygame.sprite.spritecollide(player_sprite, self.powerups, True)
        
        for powerup in collected:
            if len(self.stored_powerups) < self.max_stored:
                self.stored_powerups.append(powerup.powerup_type)
                return powerup.powerup_type
        
        return None
    
    def activate_slow_effect(self):
        self.active_effects["slow"] = {
            "start_time": pygame.time.get_ticks(),
            "duration": self.slow_effect_duration
        }
    
    def is_slow_active(self):
        if "slow" not in self.active_effects:
            return False
        
        current_time = pygame.time.get_ticks()
        effect = self.active_effects["slow"]
        
        if current_time - effect["start_time"] > effect["duration"]:
            del self.active_effects["slow"]
            return False
        
        return True
    
    def get_enemy_speed_modifier(self):
        if self.is_slow_active():
            return self.slow_factor
        return 1.0
    
    def get_remaining_slow_time(self):
        if not self.is_slow_active():
            return 0
        
        current_time = pygame.time.get_ticks()
        effect = self.active_effects["slow"]
        elapsed = current_time - effect["start_time"]
        remaining = max(0, effect["duration"] - elapsed)
        
        return remaining
    
    def update(self, dt):
        self.powerups.update(dt)
    
    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw_glow(screen)
            screen.blit(powerup.image, powerup.rect)
    
    def draw_effect_indicator(self, screen, font, x=10, y=10):
        current_y = y
        
        # Show active slow effect
        if self.is_slow_active():
            remaining_time = self.get_remaining_slow_time() / 1000.0  
            text = font.render(f"SLOW ACTIVE: {remaining_time:.1f}s", True, (0, 150, 255))
            
            # Draw background
            bg_rect = text.get_rect()
            bg_rect.x = x
            bg_rect.y = current_y
            bg_rect.inflate_ip(10, 5)
            
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(screen, (0, 150, 255), bg_rect, 2)
            
            screen.blit(text, (x + 5, current_y + 2))
            current_y += 35
        
        if self.stored_powerups:
            # Load appropriate icon based on powerup type
            powerup_type = self.stored_powerups[0]
            icon = None
            try:
                if powerup_type == "slow":
                    icon_path = r"assets\powerups\POWERUP-Clock.png"
                elif powerup_type == "bomb":
                    icon_path = r"assets\powerups\POWERUP-Bomb.png"
                icon = pygame.image.load(icon_path).convert_alpha()
                icon = pygame.transform.scale(icon, (50, 50)) 
            except:
                # Fallback diamond if image can't be loaded
                icon = pygame.Surface((50, 50), pygame.SRCALPHA)
                points = [(25, 5), (45, 25), (25, 45), (5, 25)]
                if powerup_type == "slow":
                    pygame.draw.polygon(icon, (0, 150, 255), points)
                elif powerup_type == "bomb":
                    pygame.draw.polygon(icon, (255, 50, 50), points)
                pygame.draw.polygon(icon, (255, 255, 255), points, 3)
            
            box_size = 60
            box_x = x
            box_y = current_y
            
            box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
            pygame.draw.rect(screen, (0, 0, 0), box_rect) 
            pygame.draw.rect(screen, (255, 215, 0), box_rect, 3) 
            
            if icon:
                icon_rect = icon.get_rect(center=box_rect.center)
                screen.blit(icon, icon_rect)
            
            if len(self.stored_powerups) > 1:
                count_text = font.render(f"x{len(self.stored_powerups)}", True, (0, 0, 0)) 
                count_rect = count_text.get_rect()
                count_rect.bottomright = (box_rect.right - 2, box_rect.bottom - 2)
                
                count_bg = count_rect.copy()
                count_bg.inflate_ip(4, 2)
                pygame.draw.rect(screen, (255, 255, 255, 200), count_bg)  
                screen.blit(count_text, count_rect)
            
            # Draw instruction text next to the box
            instruction_text = font.render("Press SPACE", True, (200, 200, 200))
            screen.blit(instruction_text, (box_x + box_size + 10, box_y + 20))
    
    def clear_all(self):        
        self.powerups.empty()
        self.active_effects.clear()