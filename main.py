import os
import pygame
import sys
import asyncio

# Initialize PyGame and Mixer
pygame.init()
pygame.mixer.init()

# Get the screen resolution
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Base resolution (development resolution)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

# Scale factors
SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

# Set up the game window in borderless fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Riley's Adventures")

# Set up the game clock
clock = pygame.time.Clock()

# Define TILE_SIZE (scaled)
TILE_SIZE = int(50 * SCALE_X)

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (50, 50, 50)

# Define fonts (scaled)
font = pygame.font.Font(None, int(74 * SCALE_Y))
small_font = pygame.font.Font(None, int(36 * SCALE_Y))

# Define game states
MAIN_MENU = 0
LEVEL_SELECT = 1
GAME_RUNNING = 2
CUTSCENE_START = 3
CUTSCENE_END = 4

# Level layouts (unchanged)
level_layouts = [
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        " s                                                                                                          ",
        "                                       C                                                                    ",
        "                                                                                                            ",
        "                             C    V                                                                         ",
        "                          C   GGG   GGGGG               C                                                   ",
        "                  V       GGG                                               V                               ",
        "      C       X     GGG                   P      K     P        E               E         E     C  E      F ",
        "TTTTTTTR    LTTTTR                         LTTTTTTTTTTR   LTTTTTTTTTTTTTTR     LTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGHHHHHHGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGHHHHHGGGGGGGGGGGGGGHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGHHHHHHGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGHHHHHGGGGGGGGGGGGGGHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                           C                                                ",
        "                                                                                                            ",
        "                                                        K                                                   ",
        "                     C     E   E         V   E      LTTTTTTTTTR   V                                         ",
        " s  C              LTTTTTTTTTTTTTTTTTTR    LTTTTTR                                                          ",
        "      I                                                                    C                                ",
        "      LTTTTTTTTTR                                               LTTTTTTTTTTTTR                              ",
        "                          C    X                                                                            ",
        "                    LTTTTTTTTTTTR                                               C                           ",
        "             C         X                                                       LTTTTR  V                   C",
        "          LTTTTTTTTTTTTR                                                                      B         F   ",
        "TTTTTTTR                                                                       LTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        " I B C                                                                                                      ",
        " LTTTTR                                                                                                     ",
        "          C                                                                                                 ",
        "       LTTTTTTR       C                                                                                     ",
        "                   LTTTTR                                                                                   ",
        " s                             C                                                                            ",
        "                            LTTTTTTTTTR                                                                     ",
        "                                                                                                            "
        "                                                                                                            ",
        "                                             K    E    C                                                    ",
        "                            C       X   LTTTTTTTTTTTTTTTR             E     C                               ",
        "               E       LTTTTTTTTTTTTTTR                   V LTTTTTTTTTTTTTTTTTTTTTTR     C                  ",
        "            LTTTTR                                                                LTTTTTR V   E    C     F  ",
        "TTTTTTTR                                                                                    LTTTTTTTTTTTTTTT",
        "GGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGGGGGG",
        "GGGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                           ",
        "                                                                                                           ",
        "                                                                                                           ",
        "                                                                                                          G",
        "                                                                                                          G",
        "                                                                                                        CIG",
        "                                                                                               C       LTTT",
        "                                                                                             LTTTTR        ",
        "                                                                                   C                       ",
        "                                                                                  LTTTTTTTR      C         ",
        "                                                                                              LTTTTTR      ",
        "                                                                                           C               ",
        "                                                                                     C   LTTTTTR           ",
        " s                                                                                LTTTR                    ",
        "                                                                         C K C                             ",
        "                                                                       LTTTTTTR                            ",
        "                                                                C C C                                      ",
        "                                                              LTTTTTR                                      ",
        "                                                     LTTTTTR                                               ",
        "     BI        I  X   X    X   B     E   E   E     I         E   E   E            E E E E E             F  ",
        "TTTTTTTTR    LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR  LTTTTTTTTTTTTTTTTTTTTTR  V  LTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGGHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHGGGGGGGGGGGGGGGGGGGGGHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
        "GGGGGGGGHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHHGGGGGHHHGGGGGGGGGGGGGHHHHHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                           F",
        "                                                                                                      C  LTT",
        "                                                                  C                                  LTR    ",
        "                                                        C K      LTTTTTR                        C           ",
        "                                                      LTTTTR                            C     LTR           ",
        "                                       C                                  V    C      LTTTR                 ",
        "                                    LTTTTTTTTTTTTR   V                       LTTTR                          ",
        "                        C                                                                                   ",
        "                       LTTTTTTTR                                                                            ",
        "                                         C               C                                                  ",
        "                                   LTTTTTTTTTTTR     LTTTTTR      C                                         ",
        " s                                                              LTTTTTTR                                    ",
        "                                                             C                                              ",
        "                                      C   C               LTTTTTTTR                                         ",
        "                                             LTTTTTTTTTR V                                                  ",
        "                   C  C        V LTTTTTTTTTR                                                                ",
        "                LTTTTTTTTTTTTR                                                                              ",
        "   B        X        X    V      E     V       E        E          V           V      E    E     E        I ",
        "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                     B   C                  ",
        "                                                                                 LTTTTTTTTTTTR               ",
        "                                 C          E       C       E    C   E                               C      ",
        "                       C      LTTTTTR    LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR                     LTTTTTR   ",
        "             C        LTTTR                                                                C                ",
        "          LTTTTTTR                                                                     LTTTTTTTTR           ",
        "F                                                                           KC                              ",
        "TTTR                                                                   LTTTTTTTTTTTR                        ",
        "                                                                                        LTTTTTTTTTTR        ",
        " s                                                                                                          ",
        "                                                                                                       LTTTT",
        "                                                                                                            ",
        "                                                                                               LTTTTTR      ",
        "                                                                                          C                 ",
        "                                                                              LTTR  V  LTTTTR               ",
        "            E      C          X  C  E    V        C          P                                              ",
        "TTTTTTTTTTTTTTTTTTTTTR   LTTTTTTTTTTTTTTR  LTTTTTTTTTTTTTR  LTTTTTTTTTTTTTTTTTTTR  LTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGGGGGGGGGGGGGGGHHHHHGGGGGGGGGGGGGHHHHHGGGGGGGGGGGGGHHHHGGGGGGGGGGGGGGGGGGGHHHHGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGHHHHHGGGGGGGGGGGGGHHHHHGGGGGGGGGGGGGHHHHGGGGGGGGGGGGGGGGGGGHHHHGGGGGGGGGGGGGGGGGGGGGGGG"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                                              I             ",
        "                                                                                  C        LTTTTR           ",
        "                                                                               LTTTTR                       ",
        "                                                       C            E              E                        ",
        "                                                 LTTTTTTTTR    LTTTTTTTTTTTTTTTTTTTTTTTR                    ",
        "                                            C                                                               ",
        " s                                    LTTTTTTTR                                                             ",
        "                                 C                                                                          ",
        "                            LTTTTTTTTR                                                                      ",
        "                       C                                                                                    ",
        "                 LTTTTTTTTR                                                                                 ",
        "                                                                                                            ",
        "         P  B     X E   E  X  E   E        V            V     P  C        P   C        P     E      P     F ",
        "TTTTTTTR   LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR   LTTTTTTTTR  LTTTTTTTTTR  LTTTTTTTTTR  LTTTTTTTTTTTR  LTTTTTTTTT",
        "GGGGGGGGHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHGGGGGGGGGGHHGGGGGGGGGGGHHGGGGGGGGGGGHHGGGGGGGGGGGGGHHGGGGGGGGGG",
        "GGGGGGGGHHHGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGHHHGGGGGGGGGGHHGGGGGGGGGGGHHGGGGGGGGGGGHHGGGGGGGGGGGGGHHGGGGGGGGGG"
    ],
    [
        "                                                                                    C          E           F",
        "                                                                         C      LTTTTR   LTTTTTTTTR  LTTTTTT",
        "                                          C                C          LTTTTTR                               ",
        "                             C    B    LTTTTTTR          LTTTTTTR  V                                        ",
        "           C   E           LTTTTTTTR               C                                                        ",
        "       LTTTTTTTTTTTTTTTR                         LTTTTTTR                                                   ",
        " K                                                                                                          ",
        "TTTR                                                                                                        ",
        "            E  C                C                           E                                               ",
        "     LTTTTTTTTTTTTTTR V LTTTTTTTTTTTTTR                 LTTTTTTTTTTTTTTTR                      G            ",
        "                                            C                              LTTTR               G            ",
        "                                         LTTTTTTTTR                                  BCK       G            ",
        "                                                                                  LTTTTTTR     G            ",
        " s                                                                         LTTTTR              G            ",
        "                                                                        C                      G            ",
        "                                                        C        LTTTTTTR                      G            ",
        "                                                      LTTTTTR                                  G            ",
        "                       C   X      E      E         LTR                                         G            ",
        "              C     LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR                                            G            ",
        "    B     LTTTTR                                                                                            ",
        "TTTTTTR                                                                                                     ",
        "GGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",
        "GGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    ],
    [
        "                                                                                                            ",
        "                                                                                                            ",
        "                                                                 C   C   CCCCC                              ",
        "                                                                 C   C   C   C                              ",
        "                                                                 CCCCC   CCCCC                              ",
        "                                                                 C   C   C   C                              ",
        "                                                                 C   C   CCCCC                              ",
        "                                                                                                            ",
        "                                                                 CCCCC  C  C      CCCCC C     C             ",
        "                                                                 C   C  C  C      C      C   C              ",
        "                                                                 CCCCC  C  C      CCC     C C               ",
        "                                                                 C CC   C  C      C        C                ",
        "                                                                 C   C  C  CCCCC  CCCCC    C               F",
        " s                                                           LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "                                                    LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "                                            LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "                                      LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "                               LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "                     LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "           LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
    ]
]

# Initialize game state
game_state = MAIN_MENU
current_level_index = 0  # Ensure current_level_index is initialized

# Initialize joystick
pygame.joystick.init()
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

# Load sound effects and background music
base_path = os.path.dirname(__file__)  # Get the directory of the script
sounds_path = os.path.join(base_path, "sounds")
images_path = os.path.join(base_path, "player")

jump_sound = pygame.mixer.Sound(os.path.join(sounds_path, "jump.wav"))
collect_sound = pygame.mixer.Sound(os.path.join(sounds_path, "collect.wav"))
damage_sound = pygame.mixer.Sound(os.path.join(sounds_path, "damage.wav"))
checkpoint_sound = pygame.mixer.Sound(os.path.join(sounds_path, "checkpoint.wav"))

# Load background music
pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%

# Load menu background image
menu_bg_img = pygame.image.load(os.path.join(images_path, "menupic.png")).convert()

def load_assets(level_index):
    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, 'assets', f'level{level_index + 1}')

    # Load background
    background_img = pygame.image.load(os.path.join(assets_path, 'backgrounds', 'background.png')).convert()

    # Load platform images
    platform_img = pygame.image.load(os.path.join(assets_path, 'platforms', 'platform.png')).convert_alpha()

    # Load tile images
    topground_img = pygame.image.load(os.path.join(assets_path, 'tiles', 'topground.png')).convert_alpha()
    underground_img = pygame.image.load(os.path.join(assets_path, 'tiles', 'underground.png')).convert_alpha()
    edgegroundleft_img = pygame.image.load(os.path.join(assets_path, 'tiles', 'edgegroundleft.png')).convert_alpha()
    edgegroundright_img = pygame.image.load(os.path.join(assets_path, 'tiles', 'edgegroundright.png')).convert_alpha()

    # Load enemy images
    enemy_img = pygame.image.load(os.path.join(assets_path, 'enemies', 'enemy1.png')).convert_alpha()
    vertical_enemy_img = pygame.image.load(os.path.join(assets_path, 'enemies', 'vertical_enemy.png')).convert_alpha()
    shooting_enemy_img = pygame.image.load(os.path.join(assets_path, 'enemies', 'shooting_enemy.png')).convert_alpha()

    # Load collectible images
    collectible_img = pygame.image.load(os.path.join(assets_path, 'collectibles', 'collectible.png')).convert_alpha()

    # Load power-up images
    speed_boost_img = pygame.image.load(os.path.join(assets_path, 'powerups', 'speed_boost.png')).convert_alpha()
    invincibility_img = pygame.image.load(os.path.join(assets_path, 'powerups', 'invincibility.png')).convert_alpha()
    shield_booster_img = pygame.image.load(os.path.join(assets_path, 'powerups', 'shield_booster.png')).convert_alpha()

    # Load checkpoint images
    checkpoint_img = pygame.image.load(os.path.join(assets_path, 'checkpoints', 'checkpoint.png')).convert_alpha()

    # Load flag images
    flag_img = pygame.image.load(os.path.join(assets_path, 'flags', 'flag.png')).convert_alpha()

    # Load music
    music_path = os.path.join(assets_path, 'music', 'background.mp3')

    return {
        'background': background_img,
        'platform': platform_img,
        'topground': topground_img,
        'underground': underground_img,
        'edgegroundleft': edgegroundleft_img,
        'edgegroundright': edgegroundright_img,
        'enemy': enemy_img,
        'vertical_enemy': vertical_enemy_img,
        'shooting_enemy': shooting_enemy_img,
        'collectible': collectible_img,
        'speed_boost': speed_boost_img,
        'invincibility': invincibility_img,
        'shield_booster': shield_booster_img,
        'checkpoint': checkpoint_img,
        'flag': flag_img,
        'music': music_path
    }


def draw_text_with_bg(surface, text, font, text_color, bg_color, x, y):
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (x, y)
    bg_rect = text_rect.inflate(int(20 * SCALE_X), int(10 * SCALE_Y))
    pygame.draw.rect(surface, bg_color, bg_rect)
    surface.blit(text_surf, text_rect)

def main_menu():
    global current_level_index, game_state
    menu_options = ["Start Game", "Level Select", "Quit"]
    selected_option = 0
    joystick_delay = 0

    while True:
        screen.blit(pygame.transform.scale(menu_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        # draw_text(screen, "Riley's Adventures", font, WHITE, SCREEN_WIDTH // 2 - 200, 50)

        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else GRAY
            bg_color = HIGHLIGHT if i == selected_option else BLACK
            draw_text_with_bg(screen, option, small_font, color, bg_color, SCREEN_WIDTH // 2 - int(100 * SCALE_X), int(200 * SCALE_Y) + i * int(50 * SCALE_Y))

        pygame.display.flip()

        joystick_delay = max(0, joystick_delay - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected_option == 0:  # Start Game
                        current_level_index = 0
                        game_state = CUTSCENE_START
                        return
                    elif selected_option == 1:  # Level Select
                        game_state = LEVEL_SELECT
                        return
                    elif selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    if selected_option == 0:  # Start Game
                        current_level_index = 0
                        game_state = CUTSCENE_START
                        return
                    elif selected_option == 1:  # Level Select
                        game_state = LEVEL_SELECT
                        return
                    elif selected_option == 2:  # Quit
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:  # D-pad up
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.value[1] == -1:  # D-pad down
                    selected_option = (selected_option + 1) % len(menu_options)
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and joystick_delay == 0:  # Vertical axis
                    if event.value > 0.5:
                        selected_option = (selected_option + 1) % len(menu_options)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling
                    elif event.value < -0.5:
                        selected_option = (selected_option - 1) % len(menu_options)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling


def level_select():
    global current_level_index, game_state
    selected_option = 0
    joystick_delay = 0

    while True:
        screen.fill(BLACK)
        draw_text(screen, 'Select Level', font, WHITE, SCREEN_WIDTH // 2 - int(100 * SCALE_X), int(50 * SCALE_Y))

        for i, layout in enumerate(level_layouts):
            color = WHITE if i == selected_option else GRAY
            bg_color = HIGHLIGHT if i == selected_option else BLACK
            draw_text_with_bg(screen, f'Level {i + 1}', small_font, color, bg_color, SCREEN_WIDTH // 2 - int(100 * SCALE_X), int(200 * SCALE_Y) + i * int(50 * SCALE_Y))

        pygame.display.flip()

        joystick_delay = max(0, joystick_delay - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(level_layouts)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(level_layouts)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    current_level_index = selected_option
                    game_state = CUTSCENE_START
                    return
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    current_level_index = selected_option
                    game_state = CUTSCENE_START
                    return
                elif event.button == 1:  # B button
                    game_state = MAIN_MENU
                    return
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and joystick_delay == 0:  # Vertical axis
                    if event.value > 0.5:
                        selected_option = (selected_option + 1) % len(level_layouts)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling
                    elif event.value < -0.5:
                        selected_option = (selected_option - 1) % len(level_layouts)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling

def load_cutscene_images(folder_path):
    images = []
    base_path = os.path.dirname(__file__)
    assets_path = os.path.join(base_path, folder_path)
    if os.path.exists(assets_path):
        for filename in sorted(os.listdir(assets_path)):
            if filename.endswith(".png"):
                img_path = os.path.join(assets_path, filename)
                image = pygame.image.load(img_path).convert()
                images.append(image)
    return images


def play_cutscene(folder_path):
    cutscene_images = load_cutscene_images(folder_path)
    if not cutscene_images:
        return  # If no cutscene images, return immediately

    current_image_index = 0

    while True:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(cutscene_images[current_image_index], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    current_image_index += 1
                    if current_image_index >= len(cutscene_images):
                        return  # Cutscene finished, return to previous game state
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    current_image_index += 1
                    if current_image_index >= len(cutscene_images):
                        return  # Cutscene finished, return to previous game state

def handle_flags(player, flags, end_game):
    if pygame.sprite.spritecollideany(player, flags):
        end_game()

def handle_checkpoints(player, checkpoints):
    checkpoint = pygame.sprite.spritecollideany(player, checkpoints)
    if checkpoint:
        player.respawn_point = checkpoint.rect.topleft
        player.checkpoint_reached = True  # Set checkpoint flag
        player.checkpoint_timer = 120  # Display notification for 2 seconds (60 frames per second)
        pygame.mixer.Sound.play(checkpoint_sound)
        checkpoint.kill()  # Remove the checkpoint after it's touched


def handle_collisions(player, tiles, platforms):
    # Check for vertical collisions
    player.on_platform = False
    collisions = pygame.sprite.spritecollide(player, tiles, False) + pygame.sprite.spritecollide(player, platforms, False)
    for tile in collisions:
        if player.velocity_y > 0:  # Falling down
            player.rect.bottom = tile.rect.top
            player.velocity_y = 0
            player.reset_jumps()
            if isinstance(tile, Platform):
                player.on_platform = True
        elif player.velocity_y < 0:  # Jumping up
            player.rect.top = tile.rect.bottom
            player.velocity_y = 0

    # Check for horizontal collisions
    collisions = pygame.sprite.spritecollide(player, tiles, False) + pygame.sprite.spritecollide(player, platforms, False)
    for tile in collisions:
        if player.rect.right > tile.rect.left and player.rect.left < tile.rect.left:
            player.rect.right = tile.rect.left
        elif player.rect.left < tile.rect.right and player.rect.right > tile.rect.right:
            player.rect.left = tile.rect.right

    # Move the player with the platform
    if player.on_platform:
        for platform in platforms:
            if player.rect.bottom == platform.rect.top:
                player.rect.x += platform.velocity_x

def handle_enemy_collisions(player, enemies, vertical_enemies, shooting_enemies, projectiles, reset_map):
    # Handle collisions with normal enemies
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            if player.velocity_y > 0 and player.rect.bottom <= enemy.rect.centery:
                # Lock the enemy's horizontal position
                enemy.lock()
                player.rect.centerx = enemy.rect.centerx
                player.velocity_y = player.jump_power  # Bounce the player up
                enemy.jump_on()  # Register the jump on the enemy
            else:
                enemy.unlock()
                if not player.invincible and player.take_damage():
                    reset_map()
    
    # Handle collisions with vertical enemies
    vertical_enemy_hit = pygame.sprite.spritecollideany(player, vertical_enemies)
    if not player.invincible and vertical_enemy_hit:
        if player.take_damage():
            reset_map()

    # Handle collisions with shooting enemies
    shooting_enemy_hit = pygame.sprite.spritecollideany(player, shooting_enemies)
    if not player.invincible and shooting_enemy_hit:
        if player.take_damage():
            reset_map()

    # Handle collisions with projectiles
    projectile_hit = pygame.sprite.spritecollideany(player, projectiles)
    if not player.invincible and projectile_hit:
        if player.take_damage():
            projectile_hit.kill()  # Remove the projectile that hit the player
            reset_map()

def handle_collectibles(player, collectibles):
    collected = pygame.sprite.spritecollide(player, collectibles, True)
    for collectible in collected:
        player.score += 10
        pygame.mixer.Sound.play(collect_sound)

        if player.score > 49:
            player.lives += 1
            player.score = 0

def handle_power_ups(player, power_ups):
    collected = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in collected:
        power_up.apply(player)

def draw_hud(screen, player):
    font = pygame.font.Font(None, int(36 * SCALE_Y))
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    level_text = font.render(f"Level: {current_level_index + 1}", True, WHITE)
    screen.blit(score_text, (int(10 * SCALE_X), int(10 * SCALE_Y)))
    screen.blit(lives_text, (int(10 * SCALE_X), int(50 * SCALE_Y)))
    screen.blit(level_text, (int(10 * SCALE_X), int(90 * SCALE_Y)))

    y_offset = int(130 * SCALE_Y)
    if player.speed_boost_timer > 0:
        speed_text = font.render(f"Speed Boost: {player.speed_boost_timer // 60}", True, (0, 255, 255))
        screen.blit(speed_text, (int(10 * SCALE_X), y_offset))
        y_offset += int(40 * SCALE_Y)
    if player.invincibility_timer > 0:
        invincibility_text = font.render(f"Invincibility: {player.invincibility_timer // 60}", True, (255, 255, 0))
        screen.blit(invincibility_text, (int(10 * SCALE_X), y_offset))
        y_offset += int(40 * SCALE_Y)
    if player.checkpoint_reached:
        checkpoint_text = font.render("Checkpoint Reached", True, (0, 255, 0))
        screen.blit(checkpoint_text, (SCREEN_WIDTH // 2 - checkpoint_text.get_width() // 2, int(10 * SCALE_Y)))

def game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, int(74 * SCALE_Y))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    
    font = pygame.font.Font(None, int(36 * SCALE_Y))
    restart_text = font.render("Press any button to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
            if event.type == pygame.JOYBUTTONDOWN:
                waiting = False


def handle_controller_input(player):
    for joystick in joysticks:
        # Check left joystick input
        axis_x = joystick.get_axis(0)  # Left joystick horizontal axis
        if axis_x < -0.5:  # Move left
            player.rect.x -= player.speed
            player.moving_left = True
            player.moving_right = False
        elif axis_x > 0.5:  # Move right
            player.rect.x += player.speed
            player.moving_left = False
            player.moving_right = True
        else:
            player.moving_left = False
            player.moving_right = False

        # Check D-pad input using buttons
        if joystick.get_button(13):  # D-pad left
            player.rect.x -= player.speed
            player.moving_left = True
            player.moving_right = False
        elif joystick.get_button(14):  # D-pad right
            player.rect.x += player.speed
            player.moving_left = False
            player.moving_right = True

        # Check jump button (assuming button 0 for jump)
        if joystick.get_button(0):
            player.jump()
            #pygame.mixer.Sound.play(jump_sound)

        # Check pause button (Options button)
        if joystick.get_button(9):
            return 'pause'



def create_level(layout, assets):
    tiles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    vertical_enemies = pygame.sprite.Group()
    shooting_enemies = pygame.sprite.Group()
    checkpoints = pygame.sprite.Group()
    holes = pygame.sprite.Group()
    invisible_walls = pygame.sprite.Group()
    flags = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawn_point = None

    for row_index, row in enumerate(layout):
        for col_index, col in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if col == 'G':
                tile = Tile(x, y, TILE_SIZE, TILE_SIZE, assets['underground'])
                tiles.add(tile)
            elif col == 'T':
                tile = Tile(x, y, TILE_SIZE, TILE_SIZE, assets['topground'])
                tiles.add(tile)
            elif col == 'L':
                tile = Tile(x, y, TILE_SIZE, TILE_SIZE, assets['edgegroundleft'])
                tiles.add(tile)
            elif col == 'R':
                tile = Tile(x, y, TILE_SIZE, TILE_SIZE, assets['edgegroundright'])
                tiles.add(tile)
            elif col == 'P':
                platform = Platform(x, y, TILE_SIZE, TILE_SIZE, int(100 * SCALE_X), assets['platform'])
                platforms.add(platform)
            elif col == 'C':
                collectible = Collectible(x, y, assets['collectible'])
                collectibles.add(collectible)
            elif col == 'S':
                power_up = PowerUp(x, y, 'speed', assets['speed_boost'])
                power_ups.add(power_up)
            elif col == 'I':
                power_up = PowerUp(x, y, 'invincibility', assets['invincibility'])
                power_ups.add(power_up)
            elif col == 'B':
                power_up = PowerUp(x, y, 'shield_booster', assets['shield_booster'])
                power_ups.add(power_up)
            elif col == 'E':
                enemy = Enemy(x, y, int(400 * SCALE_X), assets['enemy'])
                enemies.add(enemy)
            elif col == 'V':
                vertical_enemy = VerticalEnemy(x, y, int(150 * SCALE_Y), assets['vertical_enemy'])
                vertical_enemies.add(vertical_enemy)
            elif col == 'X':
                shooting_enemy = ShootingEnemy(x, y, assets['shooting_enemy'])
                shooting_enemies.add(shooting_enemy)
            elif col == 'H':
                hole = Hole(x, y, TILE_SIZE, TILE_SIZE)
                holes.add(hole)
            elif col == 'K':
                checkpoint = Checkpoint(x, y, assets['checkpoint'])
                checkpoints.add(checkpoint)
            elif col == 'F':
                flag = Flag(x, y, assets['flag'])
                flags.add(flag)
            elif col == 's':
                spawn_point = (x, y)

    return tiles, collectibles, power_ups, vertical_enemies, shooting_enemies, checkpoints, holes, invisible_walls, flags, platforms, enemies, spawn_point

def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def pause_menu():
    paused_font = pygame.font.Font(None, int(74 * SCALE_Y))
    small_font = pygame.font.Font(None, int(36 * SCALE_Y))
    menu_options = ["Resume", "Quit to Main Menu"]
    selected_option = 0
    joystick_delay = 0

    while True:
        screen.fill(BLACK)
        draw_text(screen, 'Paused', paused_font, WHITE, SCREEN_WIDTH // 2 - int(100 * SCALE_X), SCREEN_HEIGHT // 2 - int(50 * SCALE_Y))

        for i, option in enumerate(menu_options):
            color = WHITE if i == selected_option else GRAY
            bg_color = HIGHLIGHT if i == selected_option else BLACK
            draw_text_with_bg(screen, option, small_font, color, bg_color, SCREEN_WIDTH // 2 - int(140 * SCALE_X), SCREEN_HEIGHT // 2 + i * int(40 * SCALE_Y))

        pygame.display.flip()

        joystick_delay = max(0, joystick_delay - 1)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected_option == 0:
                        return 'resume'
                    elif selected_option == 1:
                        return 'quit'
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    if selected_option == 0:
                        return 'resume'
                    elif selected_option == 1:
                        return 'quit'
            if event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:  # D-pad up
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.value[1] == -1:  # D-pad down
                    selected_option = (selected_option + 1) % len(menu_options)
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 and joystick_delay == 0:  # Vertical axis
                    if event.value > 0.5:
                        selected_option = (selected_option + 1) % len(menu_options)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling
                    elif event.value < -0.5:
                        selected_option = (selected_option - 1) % len(menu_options)
                        joystick_delay = 10  # Add delay to prevent rapid scrolling


def load_images():
    base_path = os.path.dirname(__file__)
    images_path = os.path.join(base_path, "player")

    # Load menu background image
    # Load the original images
    character1_img = pygame.image.load(os.path.join(images_path, "character1.png")).convert_alpha()
    character2_img = pygame.image.load(os.path.join(images_path, "character2.png")).convert_alpha()
    shielded_character1_img = pygame.image.load(os.path.join(images_path, "shielded_character1.png")).convert_alpha()
    shielded_character2_img = pygame.image.load(os.path.join(images_path, "shielded_character2.png")).convert_alpha()

    # Get the original dimensions of the images
    original_width, original_height = character1_img.get_size()

    # Define the target height
    target_height = int(50 * SCALE_Y * 1.35)  # 1.35x target height
    # Calculate the target width while preserving the aspect ratio
    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)

    # Scale the images to the target dimensions
    player_images_right = [
        pygame.transform.scale(character1_img, (target_width, target_height)),
        pygame.transform.scale(character2_img, (target_width, target_height))
    ]

    player_images_left = [
        pygame.transform.flip(player_images_right[0], True, False),
        pygame.transform.flip(player_images_right[1], True, False)
    ]

    shielded_images_right = [
        pygame.transform.scale(shielded_character1_img, (target_width, target_height)),
        pygame.transform.scale(shielded_character2_img, (target_width, target_height))
    ]

    shielded_images_left = [
        pygame.transform.flip(shielded_images_right[0], True, False),
        pygame.transform.flip(shielded_images_right[1], True, False)
    ]

    return player_images_right, player_images_left, shielded_images_right, shielded_images_left

class Player(pygame.sprite.Sprite):
    def __init__(self, player_images_right, player_images_left, shielded_images_right, shielded_images_left):
        super().__init__()
        self.player_images_right = player_images_right
        self.player_images_left = player_images_left
        self.shielded_images_right = shielded_images_right
        self.shielded_images_left = shielded_images_left

        self.image_right = self.player_images_right[0]
        self.image = self.image_right

        # Adjust hitbox dimensions
        self.rect = pygame.Rect(100 * SCALE_X, SCREEN_HEIGHT - TILE_SIZE - int(50 * SCALE_Y), int(50 * SCALE_X), int(50 * SCALE_Y * 1.35))  # 1.35x height
        self.rect.width = int(50 * SCALE_X)  # Maintain original width
        self.velocity_y = 0
        self.jump_power = -15 * SCALE_Y
        self.gravity = 1 * SCALE_Y
        self.lives = 3
        self.score = 0
        self.speed = 5 * SCALE_X
        self.jumps_left = 2  # Number of jumps available (1 initial jump + 1 double jump)
        self.jump_cooldown = 0  # Cooldown timer for jumps
        self.power_up_timer = 0
        self.invincible = False
        self.invincibility_timer = 0  # Timer for invincibility after taking damage
        self.speed_boost_timer = 0
        self.shield_active = False  # Shield booster flag
        self.respawn_point = (self.rect.x, self.rect.y)
        self.on_platform = False  # Whether the player is on a moving platform
        self.checkpoint_reached = False  # Flag to indicate if a checkpoint is reached
        self.checkpoint_timer = 0  # Timer for checkpoint notification
        self.fall_timer = 0  # Timer for falling into a hole
        self.animation_timer = 0
        self.image_index = 0
        self.moving_left = False
        self.moving_right = False
        self.game_over_flag = False  # Flag to handle game over

    def update(self):
        keys = pygame.key.get_pressed()
        self.moving_left = keys[pygame.K_LEFT]
        self.moving_right = keys[pygame.K_RIGHT]
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()
    
        handle_controller_input(self)  # Update player position based on controller input
    
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
    
        if self.fall_timer > 0:
            self.fall_timer -= 1
            if self.fall_timer <= 0:
                self.lives -= 1
                #self.lives -= 1
                if self.lives > 0:
                    self.respawn()
                else:
                    self.game_over_flag = True  # Flag to handle game over in the main loop
                    self.invincible = True  # Activate invincibility after taking damage
                    self.invincibility_timer = 240  # 4 seconds of invincibility
                    self.respawn_point = (100 * SCALE_X, SCREEN_HEIGHT - TILE_SIZE - int(50 * SCALE_Y))  # Reset to initial start point
    
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.reset_jumps()
    
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
    
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = 5 * SCALE_X
    
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            if self.invincibility_timer == 0:
                self.invincible = False
    
        if self.checkpoint_timer > 0:
            self.checkpoint_timer -= 1
            if self.checkpoint_timer == 0:
                self.checkpoint_reached = False
    
        # Update animation
        if self.moving_left or self.moving_right:
            self.animation_timer += 1
            if self.animation_timer >= 10:  # Change frame every 10 ticks
                self.image_index = (self.image_index + 1) % 2
                self.animation_timer = 0
        else:
            self.image_index = 0  # Default to first frame if not moving

        # Set the appropriate image based on direction and shield status
        if self.shield_active:
            if self.moving_left:
                self.image = self.shielded_images_left[self.image_index]
            else:
                self.image = self.shielded_images_right[self.image_index]
        else:
            if self.moving_left:
                self.image = self.player_images_left[self.image_index]
            else:
                self.image = self.player_images_right[self.image_index]

    def jump(self):
        if self.jumps_left > 0 and self.jump_cooldown == 0:
            self.velocity_y = self.jump_power
            self.jumps_left -= 1
            self.jump_cooldown = 10  # Cooldown to prevent double input
            pygame.mixer.Sound.play(jump_sound)  # Play jump sound

    def reset_jumps(self):
        self.jumps_left = 2

    def speed_boost(self):
        self.speed = 10 * SCALE_X
        self.speed_boost_timer = 300  # Speed boost lasts for 5 seconds

    def invincibility(self):
        self.invincible = True
        self.invincibility_timer = 300  # Invincibility lasts for 5 seconds

    def shield_boost(self):
        self.shield_active = True  # Activate shield booster

    def is_game_over(self):
        return self.lives <= 0

    def respawn(self):
        self.rect.topleft = self.respawn_point
        self.velocity_y = 0
        self.reset_jumps()
        self.on_platform = False
        self.invincible = True  # Make the player invincible briefly to prevent instant death on respawn
        self.invincibility_timer = 60  # 1 second of invincibility

    def take_damage(self):
        if not self.invincible:
            if self.shield_active:
                self.shield_active = False  # Deactivate shield booster
                self.invincible = True  # Activate invincibility after taking damage
                self.invincibility_timer = 240  # 4 seconds of invincibility
                return False  # Indicate that the player did not take a fatal hit
            else:
                self.lives -= 1
                if self.lives > 0:
                    self.respawn()
                else:
                    self.game_over_flag = True  # Flag to handle game over in the main loop
                self.invincible = True  # Activate invincibility after taking damage
                self.invincibility_timer = 240  # 4 seconds of invincibility
                return True  # Indicate that the player took a fatal hit
        return False  # No damage taken due to invincibility

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_coords(self, x, y):
        return pygame.Rect(x + self.camera.x, y + self.camera.y, 0, 0)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # Limit scrolling to level size
        x = min(0, x)  # Left side
        y = min(0, y)  # Top side
        x = max(-(self.width - SCREEN_WIDTH), x)  # Right side
        y = max(-(self.height - SCREEN_HEIGHT), y)  # Bottom side

        self.camera = pygame.Rect(x, y, self.width, self.height)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, patrol_distance, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.end_x = x + patrol_distance
        self.velocity_x = 2 * SCALE_X

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.left <= self.start_x or self.rect.right >= self.end_x:
            self.velocity_x *= -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance, image):
        super().__init__()
        self.original_image = pygame.transform.scale(image, (int(50 * SCALE_X), int(50 * SCALE_Y)))  # Save the original image
        self.image = self.original_image.copy()  # Use a copy for the current image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.end_x = x + patrol_distance
        self.velocity_x = 2 * SCALE_X
        self.jump_counter = 0
        self.frozen = False
        self.frozen_timer = 0
        self.detection_range = 150 * SCALE_X
        self.lost_sight_range = 350 * SCALE_X
        self.original_x = x
        self.original_y = y
        self.state = 'patrol'
        self.buffer_distance = 60 * SCALE_X
        self.locked = False  # Flag to lock enemy movement

        # Load enemy images for animation
        base_path = os.path.dirname(__file__)
        assetspath = os.path.join(base_path, 'assets', f'level{current_level_index + 1}')
        images_path = os.path.join(assetspath, "enemies")
        self.enemy_images_right = [
            pygame.transform.scale(pygame.image.load(os.path.join(images_path, "enemy1.png")).convert_alpha(), (int(50 * SCALE_X), int(50 * SCALE_Y))),
            pygame.transform.scale(pygame.image.load(os.path.join(images_path, "enemy2.png")).convert_alpha(), (int(50 * SCALE_X), int(50 * SCALE_Y)))
        ]
        self.enemy_images_left = [
            pygame.transform.flip(self.enemy_images_right[0], True, False),
            pygame.transform.flip(self.enemy_images_right[1], True, False)
        ]
        self.image_index = 0
        self.animation_timer = 0

        # Load frozen image
        self.frozen_image = pygame.transform.scale(pygame.image.load(os.path.join(base_path, "player", "ice.png")).convert_alpha(), (int(50 * SCALE_X), int(50 * SCALE_Y)))

    def update(self, player, enemies):
        if self.frozen:
            self.frozen_timer -= 1
            if self.frozen_timer <= 0:
                self.frozen = False
                self.jump_counter = 0
                self.locked = False
                self.state = 'patrol'
                self.image = self.original_image  # Restore the original image
            return

        if self.locked:
            return

        if self.state == 'chase':
            if abs(self.rect.x - player.rect.x) > self.lost_sight_range:
                self.state = 'return'
            else:
                if self.rect.x < player.rect.x:
                    self.velocity_x = 2 * SCALE_X
                else:
                    self.velocity_x = -2 * SCALE_X
                self.rect.x += self.velocity_x
                self.update_animation()
                return

        if self.state == 'return':
            if abs(self.rect.x - self.original_x) > 2 * SCALE_X:
                if self.rect.x < self.original_x:
                    self.velocity_x = 2 * SCALE_X
                else:
                    self.velocity_x = -2 * SCALE_X
                self.rect.x += self.velocity_x
                self.update_animation()
            else:
                self.rect.x = self.original_x
                self.state = 'patrol'
                return

        if self.state == 'patrol':
            self.rect.x += self.velocity_x
            if self.rect.left <= self.start_x or self.rect.right >= self.end_x:
                self.velocity_x *= -1

            if abs(self.rect.x - player.rect.x) < self.detection_range and abs(self.rect.y - player.rect.y) < self.detection_range:
                self.state = 'chase'
                if self.rect.x < player.rect.x:
                    self.velocity_x = 2 * SCALE_X
                else:
                    self.velocity_x = -2 * SCALE_X

        for enemy in enemies:
            if enemy != self and abs(self.rect.x - enemy.rect.x) < self.buffer_distance:
                if self.rect.x < enemy.rect.x:
                    self.rect.x -= 2 * SCALE_X
                else:
                    self.rect.x += 2 * SCALE_X

        self.update_animation()

    def jump_on(self):
        self.jump_counter += 1
        if self.jump_counter >= 2:
            self.frozen = True
            self.frozen_timer = 480
            self.image = self.frozen_image  # Change to the frozen image

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Change frame every 10 ticks
            self.image_index = (self.image_index + 1) % 2
            self.animation_timer = 0

        if self.velocity_x > 0:
            self.image = self.enemy_images_right[self.image_index]
        else:
            self.image = self.enemy_images_left[self.image_index]

class VerticalEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(50 * SCALE_X), int(50 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_y = y
        self.end_y = y + patrol_distance
        self.velocity_y = 2 * SCALE_Y

    def update(self):
        self.rect.y += self.velocity_y
        if self.rect.top <= self.start_y or self.rect.bottom >= self.end_y:
            self.velocity_y *= -1

class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(50 * SCALE_X), int(50 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_timer = 0
        self.detection_range = TILE_SIZE * 10  # 10 blocks detection range

    def update(self, player, projectiles):
        # Check if player is within detection range and line of sight
        if abs(self.rect.x - player.rect.x) < self.detection_range and abs(self.rect.y - player.rect.y) < TILE_SIZE:
            if self.shoot_timer <= 0:
                self.shoot(projectiles, player)
                self.shoot_timer = 120  # Shoot every 2 seconds (120 frames at 60 fps)
            else:
                self.shoot_timer -= 1

    def shoot(self, projectiles, player):
        if player.rect.x > self.rect.x:
            velocity_x = 3 * SCALE_X  # Shoot to the right
            projectile_x = self.rect.right + int(5 * SCALE_X)  # Start outside the enemy's hitbox
        else:
            velocity_x = -3 * SCALE_X  # Shoot to the left
            projectile_x = self.rect.left - int(15 * SCALE_X)  # Start outside the enemy's hitbox
        
        projectile = Projectile(projectile_x, self.rect.centery, velocity_x)
        projectiles.add(projectile)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x):
        super().__init__()
        base_path = os.path.dirname(__file__)
        assetspath = os.path.join(base_path, 'assets', f'level{current_level_index + 1}')
        images_path = os.path.join(assetspath, "enemies")
        

        # Load and scale the projectile image
        self.image = pygame.image.load(os.path.join(images_path, "projectile.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(10 * SCALE_X), int(10 * SCALE_Y)))  # Adjust the size as needed

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity_x = velocity_x

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(30 * SCALE_X), int(30 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(30 * SCALE_X), int(30 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.power_type = power_type

    def apply(self, player):
        if self.power_type == 'speed':
            player.speed_boost()
        elif self.power_type == 'invincibility':
            player.invincibility()
        elif self.power_type == 'shield_booster':
            player.shield_boost()

class ShieldBooster(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(30 * SCALE_X), int(30 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply(self, player):
        player.shield_boost()

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(50 * SCALE_X), int(50 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface
        self.image.fill((0, 0, 0, 0))  # Invisible
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class InvisibleWall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface
        self.image.fill((0, 0, 0, 0))  # Invisible
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(50 * SCALE_X), int(50 * SCALE_Y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

async def main():
    global game_state, current_level_index

    def reset_map():
        nonlocal tiles, collectibles, power_ups, vertical_enemies, shooting_enemies, checkpoints, holes, invisible_walls, flags, platforms, enemies, projectiles, all_sprites, spawn_point, background_img
        assets = load_assets(current_level_index)
        tiles, collectibles, power_ups, vertical_enemies, shooting_enemies, checkpoints, holes, invisible_walls, flags, platforms, enemies, spawn_point = create_level(level_layouts[current_level_index], assets)
        projectiles = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(vertical_enemies)
        all_sprites.add(shooting_enemies)
        all_sprites.add(checkpoints)
        all_sprites.add(holes)
        all_sprites.add(invisible_walls)
        all_sprites.add(flags)
        all_sprites.add(platforms)
        all_sprites.add(enemies)
        all_sprites.add(projectiles)
    
        # Update player position to the respawn point or spawn point
        if player.checkpoint_reached:
            player.rect.topleft = player.respawn_point  # Use the checkpoint as the respawn point
        elif spawn_point:
            player.rect.topleft = spawn_point
            player.respawn_point = spawn_point  # Set the default spawn point
    
        player.checkpoint_reached = False  # Reset checkpoint flag if needed
    
        # Update the background image and music
        background_img = assets['background']
        pygame.mixer.music.load(assets['music'])
        pygame.mixer.music.play(-1)

    def handle_holes(player, holes, reset_map):
        hole_collision = pygame.sprite.spritecollideany(player, holes)
        if hole_collision:
            player.fall_timer = 1  # Set fall delay timer (0.5 seconds at 60 fps)
            return
    
        if player.fall_timer > 0:
            player.fall_timer -= 1
            if player.fall_timer == 0:
                player.lives -= 1
                if player.lives > 0:
                    player.respawn()
                    reset_map()
                else:
                    game_over_screen()  # Transition to game over screen
    
    def end_game():
        global current_level_index
        if current_level_index < len(level_layouts) - 1:
            cutscene_folder_path = os.path.join('assets', f'level{current_level_index+1}', 'cutscenes', 'end')
            #print('playing scene', cutscene_folder_path)
            play_cutscene(cutscene_folder_path)

            game_state = CUTSCENE_END  # Transition to the end cutscene state
            current_level_index = current_level_index+1# Level indices are 0-based, so level 3 is index 2
            cutscene_folder_path = os.path.join('assets', f'level{current_level_index + 1}', 'cutscenes', 'start')
            #print('playing scene', cutscene_folder_path)
            play_cutscene(cutscene_folder_path)
            reset_map()
        else:
            
            cutscene_folder_path = os.path.join('assets', f'level{current_level_index+1}', 'cutscenes', 'end')
            #print('playing scene', cutscene_folder_path)
            play_cutscene(cutscene_folder_path)
            current_level_index = 0
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            end_text = font.render("Congratulations!", True, (255, 255, 255))
            screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - end_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            game_state = MAIN_MENU
            main_menu()
            
            reset_map()

    player_images_right, player_images_left, shielded_images_right, shielded_images_left = load_images()

    while True:
        if game_state == MAIN_MENU:
            main_menu()
        elif game_state == LEVEL_SELECT:
            level_select()
        elif game_state == GAME_RUNNING:
            running = True
            paused = False

            # Create player
            player = Player(player_images_right, player_images_left, shielded_images_right, shielded_images_left)
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)

            # Create level
            assets = load_assets(current_level_index)
            tiles, collectibles, power_ups, vertical_enemies, shooting_enemies, checkpoints, holes, invisible_walls, flags, platforms, enemies, spawn_point = create_level(level_layouts[current_level_index], assets)

            # Set player position to spawn point
            if spawn_point:
                player.rect.topleft = spawn_point
                player.respawn_point = spawn_point

            # Create camera
            level_width = len(level_layouts[current_level_index][0]) * TILE_SIZE
            level_height = len(level_layouts[current_level_index]) * TILE_SIZE
            camera = Camera(level_width, level_height)

            # Create projectiles group
            projectiles = pygame.sprite.Group()

            all_sprites.add(vertical_enemies)
            all_sprites.add(shooting_enemies)
            all_sprites.add(checkpoints)
            all_sprites.add(holes)
            all_sprites.add(invisible_walls)
            all_sprites.add(flags)
            all_sprites.add(platforms)
            all_sprites.add(enemies)
            all_sprites.add(projectiles)

            background_img = assets['background']
            pygame.mixer.music.load(assets['music'])
            pygame.mixer.music.play(-1)

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_state = MAIN_MENU  # Go back to the main menu instead of quitting the game
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = not paused
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 9:  # Assuming button 9 is the pause button
                            paused = not paused

                if paused:
                    paused_option = pause_menu()
                    if paused_option == 'quit':
                        running = False
                        game_state = MAIN_MENU  # Go back to the main menu instead of quitting the game
                    elif paused_option == 'resume':
                        paused = False

                if not paused:
                    # Update player
                    player.update()

                    # Update tiles (e.g., moving platforms)
                    tiles.update()
                    platforms.update()

                    # Update enemies
                    for enemy in enemies:
                        enemy.update(player, enemies)
                    for v_enemy in vertical_enemies:
                        v_enemy.update()
                    for s_enemy in shooting_enemies:
                        s_enemy.update(player, projectiles)

                    # Update projectiles
                    projectiles.update()

                    # Handle collisions
                    handle_collisions(player, tiles, platforms)
                    handle_enemy_collisions(player, enemies, vertical_enemies, shooting_enemies, projectiles, reset_map)
                    handle_collectibles(player, collectibles)
                    handle_power_ups(player, power_ups)
                    handle_checkpoints(player, checkpoints)
                    handle_holes(player, holes, reset_map)
                    handle_flags(player, flags, end_game)

                    if player.is_game_over():
                        running = False
                        game_over_screen()
                        continue

                    # Update camera
                    camera.update(player)

                    # Draw everything
                    screen.fill((135, 206, 235))
                    for y in range(0, level_height, background_img.get_height()):
                        for x in range(0, level_width, background_img.get_width()):
                            screen.blit(background_img, camera.apply_coords(x, y))
                    for sprite in all_sprites:
                        screen.blit(sprite.image, camera.apply(sprite))
                    for tile in tiles:
                        screen.blit(tile.image, camera.apply(tile))
                    for collectible in collectibles:
                        screen.blit(collectible.image, camera.apply(collectible))
                    for power_up in power_ups:
                        screen.blit(power_up.image, camera.apply(power_up))
                    for projectile in projectiles:
                        screen.blit(projectile.image, camera.apply(projectile))

                    # Draw HUD
                    draw_hud(screen, player)

                    # Update the display
                    pygame.display.flip()

                    # Cap the frame rate
                    clock.tick(60)

                    await asyncio.sleep(0)

        elif game_state == CUTSCENE_START:
            cutscene_folder_path = os.path.join('assets', f'level{current_level_index + 1}', 'cutscenes', 'start')
            play_cutscene(cutscene_folder_path)
            game_state = GAME_RUNNING  # Transition to game running state
        elif game_state == CUTSCENE_END:
            cutscene_folder_path = os.path.join('assets', f'level{current_level_index + 1}', 'cutscenes', 'end')
            play_cutscene(cutscene_folder_path)
            current_level_index += 1  # Move to the next level
            if current_level_index < len(level_layouts):
                game_state = CUTSCENE_START  # Transition to start cutscene of the next level
            else:
                game_state = MAIN_MENU  # Return to the main menu after the last level

#if __name__ == "__main__":
#    main()

asyncio.run(main())
