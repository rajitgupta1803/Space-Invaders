import pygame
#screen dimensions
width = 1000
height = 750
#screen dimensions

#screen
screen = pygame.display.set_mode((width, height))
pygame.init()
#screen

#images
bg = pygame.transform.scale(pygame.image.load('images/background.png'), (width, height))
player_ship = pygame.image.load('images/ship.png')
alien = pygame.image.load('images/alien.png')
bullet = pygame.image.load('images/bullet.png')
#images

speed = 1
enemies = []
wave_size = 2
alien_vel = 1
timer = 0
count = 0
score = 0
bullet_timer = 0
lives = 5
wave = 1
player_bullets = []
bullet_vel = 8

player_ship_pos = [width/2, height/2]

running = True
spawned = False
game_over = False

score_font = pygame.font.SysFont("Cascadia mono", 50)
lives_font = pygame.font.SysFont("Cascadia mono", 50)
game_over_font = pygame.font.SysFont("Cascadia mono", 150)
space_to_start_font = pygame.font.SysFont("Cascadia mono", 55)
wave_font = pygame.font.SysFont("Cascadia Mono", 50)