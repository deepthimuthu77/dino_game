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