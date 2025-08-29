import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60
SPAWN_EVENT = pygame.USEREVENT + 1

DARK_PURPLE = (29, 21, 46)
GOLD = (255, 192, 0)
WHITE = (255, 255, 255)
LIGHT_PURPLE = (80, 60, 100)
TRANSLUCENT_BLACK = (0, 0, 0, 150)
DARK_BLUE = (10, 10, 25)
TEXT_COLOR = (230, 235, 245)
SHIP_COLOR = (100, 180, 255)
ENEMY_COLOR = (255, 120, 120)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

menu_bgm = r'assets/sfx/music/bgm.mp3'
game_bgm = r'assets/sfx/music/game_bgm.mp3'

# Sound effects
new_level_sfx = r'assets/sfx/sound effects/new level/going-to-the-next-level-114480.mp3'
score_sfx = r'assets/sfx/sound effects/score/achievement-video-game-type-1-230515.mp3'
game_over_sfx = r'assets/sfx/sound effects/gameover/gameover.wav'
explosion_sfx = r'assets/sfx/sound effects/explosions/8-bit-explosion-10-340462.mp3'
laser_sfx       = r'assets/sfx/sound effects/laser/laser-104024.mp3'
hover_sfx = r'assets/sfx/sound effects/hoverbutton1.wav'

LIVES = 3

player_folder_path = 'assets/entity/player/'
enemy_folder_path = 'assets/entity/enemy/'
explosion_folder_path = 'assets/vfx/explosion/'
laser_travelling_folder_path = 'assets/vfx/laser/travelling/'
laser_firing_folder_path = 'assets/vfx/laser/firing/'
settings_text_folder_path = 'assets/ui_ux/main_menu/'
mystats_text_folder_path = 'assets/ui_ux/main_menu/'
quit_text_folder_path = 'assets/ui_ux/main_menu/'

player_filenames = [f"{player_folder_path}1.png",
                    f"{player_folder_path}2.png"
                    ]
enemy_filenames = [f"{enemy_folder_path}1.png",
                   f"{enemy_folder_path}2.png"
                   ]

explosion_filenames = [f"{explosion_folder_path}1.png",
                       f"{explosion_folder_path}2.png",
                       f"{explosion_folder_path}3.png",
                       f"{explosion_folder_path}4.png",
                       f"{explosion_folder_path}5.png",
                       f"{explosion_folder_path}6.png",
                       f"{explosion_folder_path}7.png",
                       ]

laser_filenames = [f"{laser_firing_folder_path}1.png",
                   f"{laser_firing_folder_path}2.png",
                   f"{laser_travelling_folder_path}1.png",
                   f"{laser_travelling_folder_path}2.png",
                   ]

levels_filename = "levels.png"
settings_filename = f"{settings_text_folder_path}settings.png"
my_stats_filename = f"{mystats_text_folder_path}my_stats.png"
quit_filename = f"{quit_text_folder_path}exit.png"


FONT = 'assets/fonts/minecraft.ttf'

FONT_SIZE = {
    'big' : 48,
    'med' : 24,
    'small' : 18
}

# Stages
DIFFICULTY_STAGES = [
    # Stage 1
    {"spawn_interval": 1000,"enemy_speed": 2, "enemies_to_clear": 3},
    # Stage 2
    {"spawn_interval": 1000,"enemy_speed": 2, "enemies_to_clear": 4},
    # Stage 3   
    {"spawn_interval": 1000,"enemy_speed": 2, "enemies_to_clear": 5},
    # Stage 4
    {"spawn_interval": 1000,"enemy_speed": 2, "enemies_to_clear": 6},
    # Stage 5
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 7},
    # Stage 6
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 8},
    # Stage 7
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 10},
    # Stage 8
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 10},
    # Stage 9
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 10},
    # Stage 10
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 10},
    # Stage 11
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 12},
    # Stage 12
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 14},
    # Stage 13
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 16},
    # Stage 14
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 18},
    # Stage 15
    {"spawn_interval": 1000, "enemy_speed": 2, "enemies_to_clear": 20},
]

DIFFICULTY_STAGESS = [
    # Stage 1
    {"spawn_interval": 1000,"enemy_speed": 3, "enemies_to_clear": 3}
]

settings_background = 'assets/ui_ux/settings/tab.png'
settings_settings_text = 'assets/ui_ux/settings/text/settings.png'


settings_bar_sprite = 'assets/ui_ux/settings/bar.png'
settings_knob_sprite = 'assets/ui_ux/settings/bar_knob.png'

settings_music_text = 'assets/ui_ux/settings/text/music.png'
settings_sounds_text = 'assets/ui_ux/settings/text/sound.png'

menu_background = 'assets/background/main_background.png'