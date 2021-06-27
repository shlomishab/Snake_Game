import pygame
import random
from pygame.locals import *

# Gets Called in a Collision.
# Shows the Score and ends the game
def is_game_over():
	buzzer.play()
	screen.fill((0,0,0))
	game_over = 'GAME OVER!'
	show_score = 'Your Score: '+str(score)
	font = pygame.font.Font(None, 50)
	game_text = font.render(game_over ,255, (255, 255, 255))
	score_text = font.render(show_score ,255, (255, 255, 255))
	screen.blit(game_text, (score_pos,score_pos))
	screen.blit(score_text, (score_pos,score_pos+100))
	pygame.display.update()
	pygame.time.delay(1300)
	print("GAME OVER! Your Score = ", score)
	return False

# Changes 'velocity' according 
# to the pressed key
def change_diraction(diraction):
	if diraction == 'right':
		return velocity
	elif diraction == 'left':
		return -velocity
	elif diraction == 'up':
		return -velocity
	elif diraction == 'down':
		return velocity

# update x OR y movement
# and inserts new head of snake
def move_head():
	head_pos[0] += vel_x
	head_pos[1] += vel_y
	snake_pos.insert(0, list(head_pos))

# Initialise screen
pygame.init()
width = height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
point_gain = pygame.mixer.Sound('point.wav')
buzzer = pygame.mixer.Sound('buzz.wav')

# Starting coordinates:
head_x = head_y = 250
head_pos = [head_x, head_y]

# i units snake:
snake_pos = []
for i in range(11):
	snake_pos.insert(i, [head_x-i*10, head_y]) 

# 3 units snake:
#snake_pos = [[head_x, head_y],[head_x-1*10, head_y],[head_x-2*10, head_y]]

# Snake & Food's size
snake_w, snake_h = 10, 10
max_food_pos = (width/10) -1
score = 0
score_pos = width - 350
over_pos = width - 350

# Snake Moves to the Right at the start
velocity = 10
vel_x = velocity
vel_y = 0

# Random Starting Food Posotion
food_pos = [random.randint(0, max_food_pos)*10, random.randint(0, max_food_pos)*10]

gaming = True

while gaming:
	# Event Loop
	for event in pygame.event.get():
		if event.type == QUIT:
			gaming = False
		elif event.type == KEYDOWN:
			vel_x = vel_y = 0
			if event.key == pygame.K_RIGHT:
				vel_x = change_diraction('right')
			elif event.key == pygame.K_LEFT:
				vel_x = change_diraction('left')
			elif event.key == pygame.K_UP:
				vel_y = change_diraction('up')
			elif event.key == pygame.K_DOWN:
				vel_y = change_diraction('down')

	move_head()

	# Check if Food was eaten
	# and create new food at a
	# new random location
	if snake_pos[0] == food_pos:
		point_gain.play()
		score += 1
		food_pos = None
		while food_pos is None:
			new_food = [random.randint(0, max_food_pos)*10, random.randint(0, max_food_pos)*10]
			if new_food not in snake_pos:
				food_pos = new_food
			else:
				food_pos = None
	else:
		snake_pos.pop()

	# Show Snake on Screen
	screen.fill((80,100,100))
	food = pygame.draw.rect(screen, (0,255,0), (food_pos[0], food_pos[1], 10, 10))
	for pos in snake_pos:
		pygame.draw.rect(screen, (255,0,0), (pos[0],pos[1], snake_w, snake_h))
	pygame.display.update()
	pygame.display.flip()
	pygame.time.delay(60)

	# Check of Collisions - GAME OVER
	if head_pos[0] in [0, width] or head_pos[1] in [0, height] or snake_pos[0] in snake_pos[1:]: 
		gaming = is_game_over()

pygame.quit()