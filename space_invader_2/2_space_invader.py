import pygame
import random
import math
from pygame import mixer

# Initialise the pygame
pygame.init()
clock = pygame.time.Clock()

# Creating the window
height, width = 800, 600
screen = pygame.display.set_mode((height,width))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Loading bullet image
bullet = pygame.image.load('bullet.png')

# Title and Icon
pygame.display.set_caption("space invadors")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_change_x = 0

# Enemy

enemy_img = []
enemy_x = []
enemy_y = []
enemy_change_x = []
enemy_change_y = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemy_img.append(pygame.image.load('enemy.png'))
	enemy_x.append(random.randint(0, width))
	enemy_y.append(random.randint(0,150))
	enemy_change_x.append(3)
	enemy_change_y.append(40)

# Bullet

# Ready - you can't see the bullet on the screen

# fire - The bullet is currently moving


bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_change_x = 0
bullet_change_y = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

text_x =10
text_y =10

# Game over font
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
	score = font.render("score : "+ str(score_value), True, (255,255,255))
	screen.blit(score,(x, y))

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255,255,255))
	screen.blit(over_text,(200, 250))


def player(x, y):
	screen.blit(player_img,(x, y))

def enemy(x, y , i):
	screen.blit(enemy_img[i],(x, y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet_img, (x+16, y+10))

def is_collision(enemy_x,enemy_y,bullet_x, bullet_y):
	distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
	if distance < 27:
		return True
	else:
		return False



running = True
while running:
	# RGB - red, green , blue (0-255)
	screen.fill((0,0,0))

	# background image
	screen.blit(background,(0,0))
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# if keystroke is a pressed check weather its right or left

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				player_change_x = -5
			elif event.key == pygame.K_d:
				player_change_x = +5
			elif event.key == pygame.K_SPACE:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					#getting x axis of spaceship, to make sure bullet doesnt follow us
					bullet_x = player_x
					fire_bullet(player_x,bullet_y)

		if event.type == pygame.KEYUP:  
			if event.key == pygame.K_a or event.key == pygame.K_d:
				player_change_x = 0


	
	# Checking for boundaries of spaceship
	player_x += player_change_x

	if player_x <= 0:
		player_x = 0
	elif player_x >= 736:
		player_x=736


	# Enemy Movement

	for i in range(num_of_enemies):
		
		# Game over\
		if enemy_y[i] > 440:
			for j in range(num_of_enemies):
				enemy_y[i] = 2000
			game_over_text()
			break


		enemy_x[i] += enemy_change_x[i]

		if enemy_x[i] <= 0:
			enemy_change_x[i] = 3
			enemy_y[i] += enemy_change_y[i]
		elif enemy_x[i] >= 736:
			enemy_change_x[i] = -3
			enemy_y[i] += enemy_change_y[i]

		# Collision
		collision = is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
		if collision:
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bullet_y = 480
			bullet_state = "ready"
			score_value += 1

			enemy_x[i] = random.randint(0, width)
			enemy_y[i] = random.randint(0,150)

		enemy(enemy_x[i],enemy_y[i], i)

	# Bullet Movement
	if bullet_y <= 0:
		bullet_y =480
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bullet_x,bullet_y)
		bullet_y -= bullet_change_y


	player(player_x,player_y)
	show_score(text_x,text_y)
	pygame.display.update()