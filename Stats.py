import os
import pygame
from settings import *

class StatsDisplay:
    """
    My-Stats pop-up that sits on tab.png and shows
        HIGHEST <digit> LEVEL
        ANNIHILATED <digit>
    """

    # ---------- one-time asset table ----------
    _digits  = {}          # 0-9
    _text    = {}          # 'highest', 'level', 'annihilated'
    _bg      = None        # tab.png

    @classmethod
    def _load(cls):
        """Load PNGs once, safe to call many times."""
        if cls._bg is not None:
            return
        base = "assets/ui_ux/settings"
        # background
        cls._bg = pygame.image.load(os.path.join(base, "tab.png")).convert_alpha()
        # digits
        for n in range(10):
            cls._digits[n] = pygame.image.load(os.path.join(base, "number", f"{n}.png")).convert_alpha()
        # text labels
        for name in ("highest", "level", "annihilated"):
            cls._text[name] = pygame.image.load(os.path.join(base, "text", f"{name}.png")).convert_alpha()

    # ---------- instance ----------
    def __init__(self, screen):
        self.screen = screen
        self._load()

        # background rect (centred)
        self.w, self.h = self._bg.get_size()
        self.x = (SCREEN_WIDTH - self.w) // 2
        self.y = (SCREEN_HEIGHT - self.h) // 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # state
        self.is_active = False
        self.highest_level = 0
        self.annihilated   = 0

    # ------------------------------------------------------------------
    #  API
    # ------------------------------------------------------------------
    def update(self, data):
        self.highest_level = data.get("highest_level", 0)
        self.annihilated   = data.get("annihilated", 0)

    def toggle(self):
        self.is_active = not self.is_active

    def display(self):
        """Draw the pop-up only when active."""
        if not self.is_active:
           return
        print("StatsDisplay drawing at", self.x, self.y, "is_active =", self.is_active) 

        # background
        self.screen.blit(self._bg, (self.x, self.y))

        # ---- row 1: HIGHEST <digit> LEVEL ----
        hi = self._text["highest"]
        lv = self._text["level"]
        dg = self._digits[self.highest_level % 10]

        total_w = hi.get_width() + dg.get_width() + lv.get_width() + 20
        x_start = SCREEN_WIDTH // 2 - total_w // 2
        y1 = self.y + 120

        self.screen.blit(hi,  (x_start, y1))
        self.screen.blit(dg,  (x_start + hi.get_width() + 10, y1))
        self.screen.blit(lv,  (x_start + hi.get_width() + 10 + dg.get_width() + 10, y1))

        # ---- row 2: ANNIHILATED <digit> ----
        ann = self._text["annihilated"]
        dig = self._digits[min(self.annihilated, 9)]

        total2 = ann.get_width() + dig.get_width() + 10
        x2 = SCREEN_WIDTH // 2 - total2 // 2
        y2 = y1 + 80

        self.screen.blit(ann, (x2, y2))
        self.screen.blit(dig, (x2 + ann.get_width() + 10, y2))