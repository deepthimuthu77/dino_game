# 🦖 Dino Runner Game

A Python remake of the classic "Chrome Dino" game, built with **Pygame**!  
Run, jump, duck, and survive as long as you can while dodging obstacles in a desert landscape.

---

## Game Features

- Smooth 60 FPS gameplay
- Running, jumping, and ducking mechanics
- Randomly generated obstacles (Cactus and Ptera)
- Moving clouds and stars in the background
- Increasing difficulty with time
- Cheat codes for fun and testing
- Custom pixelated score display
- Game over screen and high score tracking
- Sound effects for jumping, dying, and point milestones

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/dino-runner.git
   cd dino-runner

2. **Install Required Libraries**

bash
```
pip install pygame
```

3. **Prepare the Assets**

- Create a folder named Assets/
- Inside it, add subfolders:
    -   Assets/Dino/ (Dino images)
    -   Assets/Cactus/ (Cactus images)
    -   Assets/Ptera/ (Bird images)
    -   Assets/ (for ground, cloud, game_over, replay, numbers.png, stars.png)
    -   Sounds Folder
        - Create a Sounds/ folder
        - Add sounds:
            - jump.mp3
            - die.mp3
            - points.mp3

4. **How to Play**
- SPACE or UP Arrow → Jump
- DOWN Arrow → Duck
- ESC or Q → Quit Game
- Mouse Click on "Replay" → Restart after dying

5. **Cheat Codes**
While playing, you can type these codes (no need to press ENTER):
- GODMODE ~	Become invincible (no collision death)
- DNCYCLE ~ Toggle day/night background
- IAMRICH ~	Instantly add 10,000 points
- HISCORE ~	Set high score to 99,999
- SPEEDUP ~	Increase game speed

6. **Project Structure**

dino-runner/
├── Assets/
│   ├── Cactus/
│   ├── Dino/
│   ├── Ptera/
│   ├── cloud.png
│   ├── ground.png
│   ├── game_over.png
│   ├── numbers.png
│   ├── replay.png
│   └── stars.png
├── Sounds/
│   ├── jump.mp3
│   ├── die.mp3
│   └── points.mp3
├── main.py
├── objects.py
└── README.md

7. **Future Improvements (Optional Ideas)**
- Add a Pause/Resume feature
- Power-ups (e.g., Shield, Double Jump, Speed Boost)
- Day and Night cycle after a certain score
- New enemy types (meteor showers, rolling rocks)
- Background music
- Online Leaderboard integration

8. **License**
This project is open-sourced for learning and fun.
Feel free to modify and use it — but give credit if you share it publicly! 😊

9. **Acknowledgements**
Inspired by the Google Chrome offline Dino Game.
Built using Python and Pygame <3.

# main.py
'''
import random as ran  # Importing random module for generating obstacles
import pygame as py   # Importing Pygame for game graphics and mechanics

# Initialize Pygame
py.init()

# Define screen size
SCREEN = WIDTH, HEIGHT = (750, 250)

# Create game window without a title bar
win = py.display.set_mode(SCREEN, py.NOFRAME)

# Set up game clock for frame rate control
clock = py.time.Clock()
FPS = 60  # Limit the game to 60 frames per second

# Define colors for UI elements
WHITE = (225,225,225)  # Color for daytime mode
BLACK = (0, 0, 0)       # Unused, but could be used for UI
GRAY = (32, 33, 36)     # Default background color
LIGHT_GRAY = (172, 172, 172)  # Border color

# Load images for game over and replay screens
game_over_img = py.image.load(f'Assets/game_over.png')  # Game over text
game_over_img = py.transform.scale(game_over_img, (269, 45))  # Resizing

replay_img = py.image.load(f'Assets/replay.png')  # Replay button
replay_img = py.transform.scale(replay_img, (40, 38))  # Resizing
replay_rect = replay_img.get_rect()  # Get button boundaries
replay_rect.x = WIDTH//2 - 20  # Center horizontally
replay_rect.y = 100  # Position vertically

# Load images for start screen Dino and score display
start_dino_img = py.image.load(f'Assets/Dino/1.png')  # Initial Dino image
start_dino_img = py.transform.scale(start_dino_img, (52, 58))  # Resize
start_dino_rect = start_dino_img.get_rect()  # Get bounding box
start_dino_rect.x = 50  # Position Dino on the left
start_dino_rect.bottom = 210  # Align Dino with the ground

numbers_img = py.image.load(f'Assets/numbers.png')  # Score display
numbers_img = py.transform.scale(numbers_img, (180, 18))  # Resize

# Create game objects
ground = Ground()  # Ground object
dino = Dino(50, 210)  # Dino object at position (50,210)

# Groups for obstacles and background elements
cactus_group = py.sprite.Group()  # Cactus obstacles
ptera_group = py.sprite.Group()  # Flying dinosaurs
cloud_group = py.sprite.Group()  # Floating clouds
star_group = py.sprite.Group()  # Stars for night mode

# Game variables
counter = 0  # Frame counter for timing events
enemy_time = 100  # Time interval for enemy appearance
cloud_time = ran.choice([200, 300])  # Random cloud appearance timing
star_time = 175  # Fixed star appearance timing

SPEED = 6  # Initial movement speed
jump = False  # Track whether Dino is jumping
duck = False  # Track whether Dino is ducking

score = 0  # Current game score
high_score = 0  # Highest score recorded

start_page = True  # Determines if game is at start screen
mouse_pos = (-1, -1)  # Track mouse position for clicks
running = True  # Game loop condition

# Load sound effects
jump_fx = py.mixer.Sound('Sounds/jump.mp3')  # Sound when jumping
die_fx = py.mixer.Sound('Sounds/die.mp3')  # Sound when Dino dies
points_fx = py.mixer.Sound('Sounds/points.mp3')  # Sound when reaching milestones

# Function to reset game state after losing
def reset():
    global counter, SPEED, score, high_score
    if score and score > high_score:
        high_score = score  # Update high score if needed
    score = 0  # Reset score
    counter = 0  # Reset event counter
    SPEED = 5  # Reset speed

    # Clear obstacles from screen
    cactus_group.empty()
    ptera_group.empty()
    cloud_group.empty()
    star_group.empty()

    # Reset Dino's position and state
    dino.reset()

# Cheat code variables
keys = []  # Stores recent key presses
GODMODE = False  # Invincibility mode
DAYMODE = False  # Toggle day/night background
IAMRICH = False  # Instantly add points
HISCORE = False  # Set high score manually
SPEEDUP = False  # Increase game speed

# Main game loop
while running:
    jump = False  # Reset jump state each frame

    # Adjust background color for night mode
    win.fill(WHITE if DAYMODE else GRAY)

    # Event handling loop
    for event in py.event.get():
        if event.type == py.QUIT:  # Detect window close event
            running = False

        if event.type == py.KEYDOWN:  # Detect key press
            if event.key == py.K_ESCAPE or event.key == py.K_q:
                running = False  # Quit game
            
            if event.key == py.K_SPACE or event.key == py.K_UP:
                if start_page:
                    start_page = False  # Start game if in start screen
                elif dino.alive:
                    jump = True  # Make Dino jump
                    jump_fx.play()  # Play jump sound
            
            if event.key == py.K_DOWN:
                duck = True  # Make Dino duck

            # Cheat code handling
            key = py.key.name(event.key)
            keys.append(key)
            keys = keys[-7:]  # Keep last 7 keypresses

            # Activate cheats if matching sequence detected
            if ''.join(keys).upper() == 'GODMODE':
                GODMODE = not GODMODE  # Toggle invincibility

            if ''.join(keys).upper() == 'DAYMODE':
                DAYMODE = not DAYMODE  # Toggle day/night mode

            if ''.join(keys).upper() == 'IAMRICH':
                score += 10000  # Add 10,000 points

            if ''.join(keys).upper() == 'HISCORE':
                high_score = 99999  # Set high score to max

            if ''.join(keys).upper() == 'SPEEDUP':
                SPEED += 2  # Increase game speed

        if event.type == py.KEYUP:  # Detect key release
            if event.key == py.K_SPACE or event.key == py.K_UP:
                jump = False  # Stop jumping
            if event.key == py.K_DOWN:
                duck = False  # Stop ducking
        
        if event.type == py.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # Track click position
            
            # Check if replay button clicked after losing
            if not dino.alive and replay_rect.collidepoint(mouse_pos):
                reset()  # Restart game
                mouse_pos = (-1, -1)  # Reset mouse tracking

        if event.type == py.MOUSEBUTTONUP:
            mouse_pos = (-1, -1)  # Reset mouse position

    # Draw ground movement
    ground.update(SPEED if not start_page else 0)  # Only move if playing
    ground.draw(win)

    # Check if game is starting
    if start_page:
        win.blit(start_dino_img, start_dino_rect)  # Show Dino on start screen
    else:
        if dino.alive:
            counter += 1  # Increment frame counter

            # Generate obstacles at intervals
            if counter % enemy_time == 0:
                if ran.randint(1, 10) == 5:
                    y = ran.choice([130, 165])
                    ptera = Ptera(WIDTH, y)  # Create flying enemy
                    ptera_group.add(ptera)
                else:
                    type = ran.randint(1, 5)
                    cactus = Cactus(type)  # Create cactus
                    cactus_group.add(cactus)

            # Spawn background objects (clouds, stars)
            if counter % cloud_time == 0:
                y = ran.choice([50, 75, 100])
                cloud = Cloud(WIDTH, y)
                cloud_group.add(cloud)

            if counter % star_time == 0:
                type = ran.randint(1,3)
                y = ran.randint(40,100)
                star = Star(WIDTH, y, type)
                star_group.add(star)

            # Score increase logic
            if counter % 5 == 0:
                score += 1  # Add points
'''

# objects.py

import pygame as py

SCREEN = WIDTH, HEIGHT = (750, 250)

class Ground():
	def __init__(self):
		self.image = py.image.load('Assets/ground.png')

		self.width = self.image.get_width()
		self.x1 = 0 
		self.x2 = self.width 
		self.y = 200

	def update(self, speed):
		self.x1 -= speed # makes the obj move towards the left
		self.x2 -= speed 

		if self.x1 <= -self.width: # obj at the left edge moved to the right edge
			self.x1 = self.width

		if self.x2 <= -self.width: # obj at the right edge moved to the left edge
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))

class Dino: 
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.duck_list = []

		for i in range(2, 4): # loads the images required for the dino running 
			img = py.image.load(f'Assets/Dino/{i}.png')
			img = py.transform.scale(img, (52, 58)) # resizes the image
			self.run_list.append(img) # adds the image to the list

		for i in range(4, 6): # loads the images required for the dino ducking
			img = py.image.load(f'Assets/Dino/{i}.png')
			img = py.transform.scale(img, (70, 38)) 
			self.duck_list.append(img) # adds the image to the list

		self.dead_img = py.image.load(f'Assets/Dino/8.png')
		self.dead_img = py.transform.scale(self.dead_img, (52, 58))

		self.reset() 

		# Initialize jump mechanics variables
		self.vel = 0 # Vertical velocity - starts at 0 (not moving)
		self.gravity = 0.75 # Gravity pulls dino down by 0.75 pixel per frame
		self.jumpHeight = 15 # Maximum jump/fall speed is 15 pixels per frame
		self.isJumping = False # Tracks if dino is currently in a jump

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x # sets the x coordinate of the dino
		self.rect.bottom = self.base # sets the y coordinate of the dino

		self.counter = 0
		self.alive = True

	def update(self, jump, duck):
		if self.alive:
			# Start jump if on ground and jump button pressed
			if not self.isJumping and jump:
				self.vel = -self.jumpHeight # Set upward velocity (negative is up)
				self.isJumping = True # Mark as jumping
				
			# Apply gravity to velocity each frame
			self.vel += self.gravity # Gradually slows ascent and increases descent
			if self.vel >= self.jumpHeight: # Cap downward velocity
				self.vel = self.jumpHeight
				
			# Move dinosaur based on current velocity
			self.rect.y += self.vel
			if self.rect.bottom > self.base: # If dinosaur hits the ground
				self.rect.bottom = self.base # Prevent falling through ground
				self.isJumping = False # Reset jump state

			if duck:
				self.counter += 1
				if self.counter >= 7: # updates the dino running every 7 frames	
					self.index = (self.index + 1) % len(self.duck_list) # changes between 4,  5 to show the ducking animation
					self.image = self.duck_list[self.index]
					self.rect = self.image.get_rect() # updates the rect	
					self.rect.x = self.x # updates the x coordinate
					self.rect.bottom = self.base # updates the y coordinate
					self.counter = 0 # resets the counter
			elif self.isJumping:
				self.index = 0
				self.counter = 0
				self.image = self.run_list[self.index]
			else:
				self.counter += 1
				if self.counter >= 6: # updates the dino running every 6 frames	
					self.index = (self.index + 1) % (len(self.run_list)) # changes between 1, 2, 3 to show the running animation
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect() # updates the rect	
					self.rect.x = self.x # updates the x coordinate
					self.rect.bottom = self.base # updates the y coordinate
					self.counter = 0 # resets the counter
			
			self.mask = py.mask.from_surface(self.image)
		else:
			self.image = self.dead_img

	def draw(self, win):
		win.blit(self.image, self.rect)

class Cactus(py.sprite.Sprite):
	def __init__(self, type):
		super(Cactus, self).__init__()

		self.image_list = []
		for i in range(5):
			scale = 0.65
			img = py.image.load(f'Assets/Cactus/{i+1}.png')
			w, h = img.get_size()
			img = py.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 215

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()
			
			self.mask = py.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)
				
class Ptera(py.sprite.Sprite):
	def __init__(self, x, y):
		super(Ptera, self).__init__()

		self.image_list = []
		for i in range(2):
			scale = 0.65
			img = py.image.load(f'Assets/Ptera/{i+1}.png')
			w, h = img.get_size()
			img = py.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center = (x, y)) # sets the rect to the center of the image
		self.counter = 0

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.counter += 1
			if self.counter >= 6:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

			self.mask = py.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)				

class Cloud(py.sprite.Sprite):
	def __init__(self, x, y):
		super(Cloud, self).__init__()

		self.image = py.image.load('Assets/cloud.png')
		self.image = py.transform.scale(self.image,(60, 18))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)

class Star(py.sprite.Sprite):
	def __init__(self, x, y, type):
		super(Star, self).__init__()

		image = py.image.load('Assets/stars.png')
		self.image_list = []
		for i in range(3):
			img = image.subsurface(0, 20*(i), 18, 18)
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)