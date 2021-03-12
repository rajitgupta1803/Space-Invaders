import pygame
import random
clock = pygame.time.Clock()
pygame.font.init()
from constants import *

def spawn_enemy():
	global enemies
	enemy_x = random.randint(alien.get_width() + 10, width - alien.get_width() - 10)
	enemy_y = -30
	enemies.append([enemy_x, enemy_y])

def despawn_enemies():
	global enemies
	global lives
	for k in enemies:
		if k[1] > height:
			enemies.pop(enemies.index(k))
			lives -= 1

def despawn_bullets():
	global player_bullets
	for k in player_bullets:
		if k[1] + bullet.get_height() >= height or k[1] + bullet.get_height() <= 0:
			player_bullets.pop(player_bullets.index(k))

def check_collision(curr_alien):
	global score
	global enemies
	global player_bullets

	for bullets in player_bullets:
		if bullets[0] in range(curr_alien[0] - 1, curr_alien[0] + alien.get_width() + 1) and bullets[1] <= curr_alien[1] + alien.get_height() and bullets[0] in range(0, width) and bullets[1] in range(0, height): 
			player_bullets.pop(player_bullets.index(bullets))
			enemies.pop(enemies.index(curr_alien))
			score += 1

def draw_bullets(player_bullets, bullet_vel):
	for j in player_bullets:
		screen.blit(bullet, (j))
		j[1] -= bullet_vel

def move_enemies(player_bullets, alien, alien_vel):
	global enemies
	for k in enemies:
		check_collision(k)
		k[1] += alien_vel
		screen.blit(alien, (k))

def dont_spawn_enemies():
	global count
	global wave_size
	global spawned
	global timer
	global wave

	if count == wave_size:
		spawned = True

	if spawned:
		if len(enemies) == 0:
			wave_size += 1
			wave += 1
			spawned = False
			timer = 0
			count = 0

def draw_enemies(wave_size, spawned):
	global timer
	global count

	timer += 1
	for _ in range(wave_size):
		if timer == 65:
			if not spawned:
				spawn_enemy()
				count += 1
				timer = 0
			if spawned:
				break

def draw_score_label(score_font, score):
	global score_label
	score_label = score_font.render(f"Score: {score}", True, (255, 255, 255))
	screen.blit(score_label, (10, 10))

def draw_lives_label(lives_font, lives):
	lives_label = lives_font.render(f"Lives: {lives}", True, (255, 255, 255))
	screen.blit(lives_label, (width - 10 - lives_label.get_width(), 10))

def draw_wave_label(wave_font, wave):
	wave_label = wave_font.render(f"Wave: {wave}", True, (255, 255, 255))
	screen.blit(wave_label, (width/2 - wave_label.get_width()/2, 10))

def is_game_over(game_over, spawned, count, wave_size):
	if game_over:
		spawned = True
		count = 0
		wave_size = 0

def game_over_screen(game_over, game_over_font, player_ship, space_start_font):
	global score_label
	game_over_label = game_over_font.render("GAME OVER", True, (255, 255, 255))
	space_start_label = space_start_font.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
	if game_over:
		screen.blit(game_over_label, ((width/2) - (game_over_label.get_width()/2), height/2 - game_over_label.get_height()))
		screen.blit(player_ship, (width/2 - player_ship.get_width()/2, height - player_ship.get_height()))
		screen.blit(score_label, (width/2 - score_label.get_width()/2, height/2 + game_over_label.get_height()/3))
		screen.blit(space_start_label, (width/2 - space_start_label.get_width()/2, height - player_ship.get_height() - space_start_label.get_height() * 1.5))

def restart_game():
	global count
	global spawned
	global wave_size
	global game_over
	global lives
	global score
	global enemies
	global timer
	global wave

	count = 0
	timer = 0
	wave = 1
	spawned = False
	wave_size = 2
	game_over = False
	lives = 5
	score = 0
	enemies = []
	draw_enemies(wave_size, spawned)

while running:
	fps = clock.tick(280)
	screen.blit(bg, (0, 0))

	if bullet_timer < 280/4:
		bullet_timer += 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if not game_over:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_a] and player_ship_pos[0] - speed >= 0:
				pygame.key.set_repeat(1,1)
				player_ship_pos[0] -= speed
			if keys[pygame.K_d] and player_ship_pos[0] + player_ship.get_width() + speed <= width:
				pygame.key.set_repeat(1,1)
				player_ship_pos[0] += speed
			if keys[pygame.K_w] and player_ship_pos[1] - speed >= 0:
				pygame.key.set_repeat(1,1)
				player_ship_pos[1] -= speed
			if keys[pygame.K_s] and player_ship_pos[1] + player_ship.get_height() + speed <= height :
				pygame.key.set_repeat(1,1)
				player_ship_pos[1] += speed
			if keys[pygame.K_SPACE]:
				if bullet_timer == 280/4:
					player_bullets.append(player_ship_pos[:])
					bullet_timer = 0

	if not game_over:
		draw_score_label(score_font, score)
		draw_lives_label(lives_font, lives)
		draw_wave_label(wave_font, wave)
		screen.blit(player_ship, player_ship_pos)

	draw_enemies(wave_size, spawned)

	if not game_over:
		move_enemies(player_bullets, alien, alien_vel)
	draw_bullets(player_bullets, bullet_vel)
	despawn_enemies()
	if lives == 0:
		game_over = True
	despawn_bullets()
	dont_spawn_enemies()
	is_game_over(game_over, spawned, count, wave_size)
	game_over_screen(game_over, game_over_font, player_ship, space_to_start_font)

	if game_over:
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			restart_game()

	pygame.display.update()
