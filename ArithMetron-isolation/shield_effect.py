import pygame
import math
import random

class ShieldEffect:
    def __init__(self, player_sprite):
        self.player = player_sprite
        self.active = False
        self.shield_radius = 60
        self.base_alpha = 100  
        self.pulse_speed = 0.005
        self.pulse_offset = 0
        self.bubble_particles = []
        self.spark_particles = []
        
        # Shield colors - create a nice bubble effect
        self.shield_colors = [
            (100, 200, 255, self.base_alpha),  
            (150, 220, 255, self.base_alpha),  
            (200, 240, 255, self.base_alpha),  
        ]
        
        # Initialize bubble particles with slightly larger size
        for _ in range(10):  
            angle = random.uniform(0, 2 * math.pi)
            self.bubble_particles.append({
                'angle': angle,
                'radius': random.uniform(40, 55),
                'speed': random.uniform(0.001, 0.003),
                'size': random.uniform(5, 10),  
                'alpha': random.uniform(50, 100)  
            })

    def activate(self):
        self.active = True
        self.pulse_offset = 0
        
    def deactivate(self):
        self.active = False
        
    def update(self, dt):
        if not self.active:
            return
            
        # Update pulse effect
        self.pulse_offset += self.pulse_speed * dt
        
        # Update bubble particles
        for particle in self.bubble_particles:
            particle['angle'] += particle['speed'] * dt
            # Slight radius variation for organic movement
            particle['radius'] = 45 + 10 * math.sin(particle['angle'] * 2 + self.pulse_offset)
            
        # Occasionally create spark particles when shield is hit or active
        if random.random() < 0.1:  # 10% chance each frame
            self.create_spark_particle()
            
        # Update spark particles
        for spark in self.spark_particles[:]:
            spark['life'] -= dt * 0.003
            spark['x'] += spark['vx'] * dt
            spark['y'] += spark['vy'] * dt
            spark['alpha'] *= 0.995
            
            if spark['life'] <= 0 or spark['alpha'] < 10:
                self.spark_particles.remove(spark)

    def create_spark_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(35, 50)
        x = self.player.rect.centerx + math.cos(angle) * distance
        y = self.player.rect.centery + math.sin(angle) * distance
        
        spark = {
            'x': x,
            'y': y,
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-0.5, 0.5),
            'life': 1.0,
            'alpha': 150,
            'size': random.uniform(2, 4)
        }
        self.spark_particles.append(spark)

    def draw(self, screen):
        if not self.active:
            return
            
        # Calculate pulsing alpha
        pulse_alpha = self.base_alpha + 30 * math.sin(self.pulse_offset)
        pulse_alpha = max(30, min(150, pulse_alpha))  
        
        # Create shield surface
        shield_size = (self.shield_radius * 2 + 20, self.shield_radius * 2 + 20)
        shield_surf = pygame.Surface(shield_size, pygame.SRCALPHA)
        center = (shield_size[0] // 2, shield_size[1] // 2)
        
        # Draw multiple shield layers for depth
        for i, base_color in enumerate(self.shield_colors):
            radius = self.shield_radius - i * 5
            alpha = int(pulse_alpha * (0.8 - i * 0.2))
            color = (*base_color[:3], alpha)
            
            # Draw outer glow
            for glow_radius in range(radius + 10, radius - 1, -2):
                glow_alpha = max(10, alpha // (glow_radius - radius + 2))  
                glow_color = (*base_color[:3], glow_alpha)
                pygame.draw.circle(shield_surf, glow_color, center, glow_radius)
            
            # Draw main shield circle with thicker yellow outline
            pygame.draw.circle(shield_surf, (255, 255, 0, alpha), center, radius, 5)  
            
        # Draw bubble particles with yellow color
        for particle in self.bubble_particles:
            bubble_x = center[0] + math.cos(particle['angle']) * particle['radius']
            bubble_y = center[1] + math.sin(particle['angle']) * particle['radius']
            
            bubble_color = (255, 255, 0, int(particle['alpha'])) 
            pygame.draw.circle(shield_surf, bubble_color, 
                             (int(bubble_x), int(bubble_y)), 
                             int(particle['size']))
            # Add highlight to bubble
            highlight_color = (255, 255, 150, int(particle['alpha'] * 1.5)) 
            pygame.draw.circle(shield_surf, highlight_color, 
                             (int(bubble_x - particle['size']/3), int(bubble_y - particle['size']/3)), 
                             max(1, int(particle['size']/3)))
        
        # Draw hexagonal pattern overlay for sci-fi effect
        self.draw_hex_pattern(shield_surf, center, self.shield_radius, int(pulse_alpha * 0.4))  
        
        # Position shield around player
        shield_rect = shield_surf.get_rect(center=self.player.rect.center)
        screen.blit(shield_surf, shield_rect)
        
        # Draw spark particles
        for spark in self.spark_particles:
            spark_color = (100, 200, 255, int(spark['alpha']))
            pygame.draw.circle(screen, spark_color, 
                             (int(spark['x']), int(spark['y'])), 
                             max(1, int(spark['size'])))
    
    def draw_hex_pattern(self, surface, center, radius, alpha):
        if alpha < 15:  
            return
            
        hex_size = 12
        color = (150, 220, 255, alpha)
        
        for row in range(-3, 4):
            for col in range(-3, 4):
                hex_x = center[0] + col * hex_size * 1.5
                hex_y = center[1] + row * hex_size * math.sqrt(3) / 2
                
                if col % 2:
                    hex_y += hex_size * math.sqrt(3) / 4
                
                # Only draw if within shield radius
                distance = math.sqrt((hex_x - center[0])**2 + (hex_y - center[1])**2)
                if distance < radius - 10:
                    self.draw_hexagon(surface, (int(hex_x), int(hex_y)), hex_size // 3, color)
    
    def draw_hexagon(self, surface, center, size, color):
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(surface, color, points, 1)

    def create_impact_effect(self):
        if not self.active:
            return
            
        # Create multiple spark particles in a burst
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(40, 60)
            x = self.player.rect.centerx + math.cos(angle) * distance
            y = self.player.rect.centery + math.sin(angle) * distance
            
            spark = {
                'x': x,
                'y': y,
                'vx': math.cos(angle) * random.uniform(1, 3),
                'vy': math.sin(angle) * random.uniform(1, 3),
                'life': 1.0,
                'alpha': 255,
                'size': random.uniform(3, 6)
            }
            self.spark_particles.append(spark)
        
        # Create temporary shield pulse
        self.pulse_offset += math.pi / 4  # Jump the pulse forward for impact effect