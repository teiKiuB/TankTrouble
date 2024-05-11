from os import path
import pygame
vector = pygame.math.Vector2

# define colors based on  (R, G, B)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (120, 120, 120)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (120, 104, 82)
BLUE = (0, 0, 255)
# game settings

WIDTH = 1024 #768
HEIGHT = 768 #512
FPS = 60
TITLE = "TANK TROUBLE"
BGCOLOR = WHITE

SQSIZE = 16 #16
GRIDWIDTH = WIDTH / SQSIZE
GRIDHEIGHT = HEIGHT / SQSIZE

# player settings

playerSpeed = 100  # in second
enemySpeed = 100


PLAYER_IMAGE = 'tank_blue.png'
ENEMY_IMAGE = 'tank_green.png'
WALL_IMAGE = 'dirt.png'
SHIELD_ITEM_IMAGE = 'tank-shield.png'
SHIELD_IMAGE = 'tank-shield-circle.png'

RotationSpeedOfPlayer = 120  # degree in second
RotationSpeedOfEnemy = 120

player_box = pygame.Rect(0, 0, 30, 30)
enemy_box = pygame.Rect(0, 0, 30, 30)
bullet_box = pygame.Rect(0, 0, 15, 15)
shield_box = pygame.Rect(0, 0, 80, 80)


# shooting setting
BULLET_IMAGE = 'BULLET.png'
bulletSpeed = 300
Bullet_life_time = 4000  # 1 second
bullet_repeating = 300
bullet_rate = 2000  # HOW FAST THE BULLET GET PRODUCED
turret = vector(0, 30)


def collide(sprite1, sprite2):
    return sprite1.hit_rect.colliderect(sprite2.rect)


font_name = pygame.font.match_font('arial')


# def drawing_text(surf, text, size, x, y, color):
#     font = pygame.font.Font(font_name, size)   # create font object file
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surf.blit(text_surface, text_rect)
    
def drawing_text(surf, text, size, x, y, color, bg_color=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)

    if bg_color is not None:
        bg_surface = pygame.Surface(text_surface.get_size())
        bg_surface.fill(bg_color)
        surf.blit(bg_surface, text_rect)

    surf.blit(text_surface, text_rect)