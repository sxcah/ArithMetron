import pygame, math

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, speed=0):
        super().__init__()
        self.original_frames = frames
        self.frames = frames
        self.frame_index = 0
        if not self.frames:
            self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
            self.image.fill((255, 0, 0, 100))
        else:
            self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.animation_timer = 0
        self.animation_speed = 100
        self.rotation = 0

    def update(self, dt):
        if self.speed != 0:
            self.rect.y += self.speed

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.frames:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.original_frames[self.frame_index]
                self.image = pygame.transform.rotate(self.image, self.rotation)
                self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate_to(self, target_pos):
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.rotation = angle