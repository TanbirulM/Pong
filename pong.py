# Simple pong game
import random
import pygame
import sys

# Ball movement speeds
easy = 30
medium = 60
hard = 90
pro = 120

difficulty = input('Select Your Difficulty:\n1: Easy\n2: Medium\n3: Hard\n4: Pro\n')
while (int(difficulty) != 1 and int(difficulty) != 2 and int(difficulty) != 3 and int(difficulty) != 4):
    print('Please pick a number according to your desired game difficulty')
    difficulty = input('1: Easy\n2: Medium\n3: Hard\n4: Pro\n')

if int(difficulty) == 1:
    difficulty = easy
if int(difficulty) == 2:
    difficulty = medium
if int(difficulty) == 3:
    difficulty = hard
if int(difficulty) == 4:
    difficulty = pro

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
		
	# Player Score
	if ball.left <= 0: 
		score_time = pygame.time.get_ticks()
		player_score += 1
		
	# Opponent Score
	if ball.right >= screen_width:
		score_time = pygame.time.get_ticks()
		opponent_score += 1
		
	if ball.colliderect(player) and ball_speed_x > 0:
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0:
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

def player_animation():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()

	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,(255,255,255))
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = basic_font.render("2",False,(255,255,255))
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = basic_font.render("1",False,(255,255,255))
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7 * random.choice((1,-1))
		score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Virtual Pong')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10,140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,140)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
ball_moving = False
score_time = True

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 6
			if event.key == pygame.K_DOWN:
				player_speed += 6
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 6
			if event.key == pygame.K_DOWN:
				player_speed -= 6
	
	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()

	# Visuals 
	screen.fill('grey12')
	pygame.draw.rect(screen, (40,60,80), player)
	pygame.draw.rect(screen, (40,60,80), opponent)
	pygame.draw.ellipse(screen, (255,165,0), ball)
	pygame.draw.aaline(screen, (0,0,0), (screen_width / 2, 0),(screen_width / 2, screen_height))

	if score_time:
		ball_start()

	player_text = basic_font.render(f'{player_score}',False,(255,250,250))
	screen.blit(player_text,(660,470))

	opponent_text = basic_font.render(f'{opponent_score}',False,(255,250,250))
	screen.blit(opponent_text,(600,470))

	pygame.display.flip()
	clock.tick(difficulty)