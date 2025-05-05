import random as ran
import pygame as py

from objects import Ground, Dino, Cactus, Ptera, Cloud, Star

py.init()
SCREEN = WIDTH, HEIGHT = (750, 250)
win = py.display.set_mode(SCREEN, py.NOFRAME) # creates the window
# py.display.set_caption("Deepthi's Dino game")

clock = py.time.Clock() # to control game speed
FPS = 60 # sets the frame rate

# COLORS
WHITE = (225,225,225)
GRAY = (32, 33, 36)
LIGHT_GRAY = (172, 172, 172)

# IMAGES
game_over_img = py.image.load(f'Assets/game_over.png')
game_over_img = py.transform.scale(game_over_img, (269, 45))

replay_img = py.image.load(f'Assets/replay.png')
replay_img = py.transform.scale(replay_img, (40, 38))
replay_rect = replay_img.get_rect()
replay_rect.centerx = WIDTH//2
replay_rect.y = 100

start_dino_img = py.image.load(f'Assets/Dino/1.png')
start_dino_img = py.transform.scale(start_dino_img, (52, 58))
start_dino_rect = start_dino_img.get_rect()
start_dino_rect.x = 50
start_dino_rect.bottom = 210 


numbers_img = py.image.load(f'Assets/numbers.png')
numbers_img = py.transform.scale(numbers_img, (180, 18))

# OBJECTS & GROUPS
ground = Ground()
dino = Dino(50, 210)

cactus_group = py.sprite.Group()
ptera_group = py.sprite.Group()
cloud_group = py.sprite.Group()
star_group = py.sprite.Group()

# VARIABLES 
counter = 0
enemy_time = 100
cloud_time = ran.choice([200, 300])
star_time = 175

SPEED = 6
jump = False
duck = False

score = 0
high_score = 0

start_page = True 
mouse_pos = (-1, -1) 
# special value that indicates that the mouse position is unknown or invalid

running = True

# SFX
jump_fx = py.mixer.Sound('Sounds/jump.mp3')
die_fx = py.mixer.Sound('Sounds/die.mp3')
points_fx = py.mixer.Sound('Sounds/points.mp3')

# FUNCTION
def reset():
	global counter, SPEED, score, high_score
	
	if score and score > high_score:
		high_score = score
	
	score = 0  
	counter = 0
	SPEED = 5

	cactus_group.empty()
	ptera_group.empty()
	cloud_group.empty()
	star_group.empty()

	dino.reset()

# CHEATCODES
keys = []
GODMODE = False
DAYMODE = False
IAMRICH = False
HISCORE = False
SPEEDUP = False

while running:
	jump = False
	if DAYMODE :
		win.fill(WHITE)
	else:
		win.fill(GRAY)

	for event in py.event.get(): # checks for events
		if event.type == py.QUIT:
			running = False

		if event.type == py.KEYDOWN: # when a key is pressed
			if event.key == py.K_ESCAPE or event.key == py.K_q:
				running = False

			if event.key == py.K_SPACE:
				if start_page:
					start_page = False
				elif dino.alive:
					jump = True
					jump_fx.play()
				else: 
					reset()

			if event.key == py.K_UP:
				if start_page:
					start_page = False
				elif dino.alive:
					jump = True
					jump_fx.play()

			if event.key == py.K_DOWN:
				duck = True

			key = py.key.name(event.key)
			keys.append(key)
			keys = keys[-7:] # to get the last 7 keystrokes

			if ''.join(keys).upper() == 'GODMODE':
				GODMODE = not GODMODE

			if ''.join(keys).upper() == 'DAYMODE':
				DAYMODE = not DAYMODE

			if ''.join(keys).upper() == 'IAMRICH':
				score += 10000

			if ''.join(keys).upper() == 'HISCORE':
				high_score = 99999

			if ''.join(keys).upper() == 'SPEEDUP':
				SPEED += 2

		if event.type == py.KEYUP: # when a key is released
			if event.key == py.K_SPACE or event.key == py.K_UP:
				jump = False

			if event.key == py.K_DOWN:
				duck = False
		
		if event.type == py.MOUSEBUTTONDOWN:
			mouse_pos = event.pos
			# Check if game over and player clicked on replay button
			if not dino.alive and replay_rect.collidepoint(mouse_pos):
				reset()
				mouse_pos = (-1, -1)  # Reset mouse position after use

		if event.type == py.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)

	# Draw the ground on both screens
	ground.update(SPEED if not start_page else 0)  # Only move if game started
	ground.draw(win)

	if start_page:
		# Draw the start screen dino
		win.blit(start_dino_img, start_dino_rect)
			
	else:
		if dino.alive: 
			counter += 1
			if counter % enemy_time == 0:
				if ran.randint(1, 10) == 5:
					y = ran.choice([130, 165])
					ptera = Ptera(WIDTH, y)
					ptera_group.add(ptera)
				else:
					type = ran.randint(1, 5)
					cactus = Cactus(type)
					cactus_group.add(cactus)

			if counter % cloud_time == 0:
				y = ran.choice([50, 75, 100])
				cloud = Cloud(WIDTH, y)
				cloud_group.add(cloud)

			if counter % star_time == 0:
				type = ran.randint(1,3)
				y = ran.randint(40,100)
				star = Star(WIDTH, y,type)
				star_group.add(star)
				
			if counter % 5 == 0:
				score += 1
				
				# Play sound when reaching multiples of 100
				if score > 0 and score % 100 == 0:
					points_fx.play()
					# Increase difficulty at score milestones
					SPEED += 0.1
					enemy_time -= 0.5

			if not GODMODE:
				for cactus in cactus_group:
					if py.sprite.collide_mask(dino, cactus):
						SPEED = 0
						dino.alive = False
						die_fx.play()  # Play death sound when collision happens
			
				for ptera in ptera_group:
					if py.sprite.collide_mask(dino, ptera):
						SPEED = 0
						dino.alive = False
						die_fx.play()  # Play death sound when collision happens

		cactus_group.update(SPEED, dino)
		cactus_group.draw(win)

		ptera_group.update(SPEED + 1, dino)
		ptera_group.draw(win)

		cloud_group.update(SPEED - 3, dino)
		cloud_group.draw(win)

		star_group.draw(win)
		star_group.update(SPEED - 3, dino)
		
		dino.update(jump, duck)
		dino.draw(win)
		
		string_score = str(score).zfill(5)
		for i, num in enumerate(string_score):
			win.blit(numbers_img, (WIDTH - 90 + (i * 15), 15), (15 * int(num), 0, 15, 18))
		
		if high_score:
			
			win.blit(numbers_img, (WIDTH - 210, 15), (150, 0, 30, 18))
			
			# Draw high score
			string_score = str(high_score).zfill(5)
			for i, num in enumerate(string_score):
				win.blit(numbers_img, (WIDTH - 175 + (i * 15), 15), (15 * int(num), 0, 15, 18))

		if not dino.alive:
			win.blit(game_over_img, (WIDTH//2 - 134, 55))
			win.blit(replay_img, replay_rect)

	py.draw.rect(win, LIGHT_GRAY, (0, 0, WIDTH, HEIGHT), 7)
	clock.tick(FPS) # limits the frame rate
	py.display.update() # updates the display

py.quit()