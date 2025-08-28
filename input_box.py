import pygame

from settings import FONT, FONT_SIZE

pygame.init()

class InputBox:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(FONT, FONT_SIZE['med'])
        self.color = (60, 60, 60)
        self.text_color = (255, 255, 255)
        self.text = ''
        self.active = True
        self.txt_surface = font.render(self.text, True, self.text_color)
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                submitted_text = self.text
                self.text = ''
                self.txt_surface = self.font.render(self.text, True, self.text_color)
                return submitted_text
            else:
                if event.unicode.isdigit():
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.text_color)
            self.cursor_timer = 0
        return None

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer > 500:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        if self.cursor_visible and self.active:
            cursor_pos = self.txt_surface.get_width() + 5
            pygame.draw.line(screen, self.text_color, (self.rect.x + cursor_pos, self.rect.y + 5), (self.rect.x + cursor_pos, self.rect.y + self.rect.height - 5), 2)
