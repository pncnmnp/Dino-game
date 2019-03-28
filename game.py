import pygame
from time import sleep
from random import shuffle, uniform

'''
TODO:
>> pause feature
>> high score feature [ done ]
>> infinite vertical scrolling
>> game sound
'''

class Characters(pygame.sprite.Sprite):
	def __init__(self, pos, image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

class Canvas:
	def __init__(self):
		self.width = 1250
		self.height = 300
		self.fps = 50
		self.rel_height = 0.64
		self.display = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()
		self.x = self.width * 0.005
		self.y = self.height * self.rel_height
		self.choose = 3
		self.duck_choose = 3
		self.is_jump = False
		self.is_duck = False
		self.duck_count = 10
		self.PAINT = (150, 150, 150)
		self.velocity = 10
		self.mass = 0.6
		self.duck_y = 20
		self.dino_rect = None
		self.pos = [0.5, 1, 2, 3, 1.5, 2.5]
		self.clouds = [(0.5, 0.8), (1.3, 1.7), (2, 2.4)]
		self.cloud_pos = self.get_cloud_values()
		self.cactus_choose = list()
		self.cactus_rect = list()
		self.score = 0
		self.score_jump = 10
		self.highscore_file = './highscore.txt'
		self.highscore = self.get_highscore()

	def get_highscore(self):
		try:
			with open(self.highscore_file, 'r') as f:
				return f.readlines()[0]
		except:
			self.highscore = 0

	def update_score(self):
		self.score_jump -= 1
		if self.score_jump == 0:
			self.score += 1
			self.score_jump = 10
		num_width = 0
		for num in str(self.score):
			self.display.blit(self.numbers[int(num)], (1050+num_width, self.height*0.10))
			num_width += 20
		if self.score > int(self.highscore):
			self.display.blit(self.H_img, (1050+num_width+20, self.height*0.10))
			self.display.blit(self.I_img, (1050+num_width+40, self.height*0.10))

	def get_cloud_values(self):	
		return [round(uniform(self.clouds[i][0], self.clouds[i][1]), 2) for i in range(3)]

	def cactus_load(self):
		self.cactus_rect = list()
		for index in range(len(self.cactus_choose)):
			coordinates = (int(self.width/4)*self.pos[index], self.height*0.52 + 40 + self.cactus_choose[index][2])
			self.display.blit(self.cactus_choose[index][0], coordinates)
			self.cactus_rect.append((Characters((self.x, self.y), self.cactus_choose[index][0]), self.cactus_choose[index][0].get_rect(center=coordinates)))

	def cloud_load(self):
		for index in range(len(self.cloud_pos)):
			self.display.blit(self.cloud, (int(self.width/4)*self.cloud_pos[index], self.height*0.30))

	def ground_load(self):
		self.display.blit(self.ground, (20, self.height*0.52 + 75))

	def sun_load(self):
		self.display.blit(self.sun, (1000, self.height*0.30))

	def check_next_frame(self):
		if self.x >= 1100:
			shuffle(self.pos)
			shuffle(self.cactus_choose)
			self.x = self.width * 0.005
			self.cactus_load()
			self.cloud_pos = self.get_cloud_values()
			self.fps += 5

	def loop(self):
		self.crashed = False
		while self.crashed == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.crashed = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						if not self.is_duck:
							if self.velocity == 1: self.velocity = 10
							self.is_jump = True
					if event.key == pygame.K_DOWN:
						if not self.is_jump and not self.is_duck:
							self.is_duck = True
							self.y += self.duck_y
			self.display.fill(self.PAINT)
			self.load_elements()
			self.check_collision()
			self.x += 2
			pygame.display.update()
			self.clock.tick(self.fps)
		self.save_highscore()
		self.quit_message()

	def save_highscore(self):
		if self.score > int(self.highscore):
			with open(self.highscore_file, 'w') as f:
				f.write(str(self.score))
				f.close()

	def quit_message(self):
		self.fps = 50
		self.display.blit(self.game_over, (self.width/3, self.height*0.4))
		pygame.display.flip()
		sleep(1)

	def check_collision(self):
		for cactus in self.cactus_rect:
			offset_x = cactus[1].center[0] - self.dino_rect[1].center[0]
			offset_y = cactus[1].center[1] - self.dino_rect[1].center[1]
			if self.dino_rect[1].colliderect(cactus[1]):
				result = (self.dino_rect[0].mask).overlap(cactus[0].mask, (offset_x, offset_y))
				if result:
					self.crashed = True

	def load_elements(self):
		self.sun_load()
		self.cloud_load()
		self.cactus_load()
		self.update_score()
		self.dino()
		self.ground_load()
		self.check_next_frame()

	def jump(self):
		if self.is_jump:
			if self.velocity > 0:
				force = (0.5 * self.mass * (self.velocity**2))
			else:
				force = -(0.5 * self.mass * (self.velocity**2))				
			self.y -= force
			self.x += 3.5
			self.velocity -= 1

			if self.y > self.height * self.rel_height:
				self.y = self.height * self.rel_height
				self.is_jump = False
				self.velocity = 10

	def load_images(self):
		self.dino_img1 = pygame.image.load('./data/dinos/run1.png').convert_alpha()
		self.dino_img2 = pygame.image.load('./data/dinos/run2.png').convert_alpha()
		self.dino_jump = pygame.image.load('./data/dinos/jump.png').convert_alpha()
		self.dino_duck1 = pygame.image.load('./data/dino_duck/duck1.png').convert_alpha()
		self.dino_duck2 = pygame.image.load('./data/dino_duck/duck2.png').convert_alpha()
		self.cactus1 = pygame.image.load('./data/cactus/c1.png').convert_alpha()
		self.cactus2 = pygame.image.load('./data/cactus/c2.png').convert_alpha()
		self.cactus3 = pygame.image.load('./data/cactus/c3.png').convert_alpha()
		self.cactus4 = pygame.image.load('./data/cactus/c4.png').convert_alpha()
		self.cactus5 = pygame.image.load('./data/cactus/c5.png').convert_alpha()
		self.ground = pygame.image.load('./data/misc/ground.png').convert_alpha()
		self.sun = pygame.image.load('./data/misc/sun.png').convert_alpha()
		self.cloud = pygame.image.load('./data/misc/cloud.png').convert_alpha()
		self.game_over = pygame.image.load('./data/misc/game_over.png').convert_alpha()
		self.H_img = pygame.image.load('./data/numbers/H.png').convert_alpha()
		self.I_img = pygame.image.load('./data/numbers/I.png').convert_alpha()

		nums = [None for i in range(10)]
		self.numbers = dict()

		for num in range(len(nums)):
			nums[num] = pygame.image.load('./data/numbers/'+str(num)+'.png')
			self.numbers[num] = nums[num]

		# arranged according to image, image_name, dist. from ground
		self.cactus_choose = [(self.cactus1, 'c1', 0), (self.cactus2, 'c2', 10), (self.cactus3, 'c3', 10), (self.cactus4, 'c4', 0), (self.cactus5, 'c5', 0)]

	def dino(self):
		if self.is_jump == True:
			self.display.blit(self.dino_jump, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_jump), self.dino_jump.get_rect(center=(self.x, self.y)))
			self.jump()
		elif self.is_duck == True:
			if self.duck_choose > 0:
				self.display.blit(self.dino_duck1, (self.x, self.y))
				self.dino_rect = (Characters((self.x, self.y), self.dino_duck1), self.dino_duck1.get_rect(center=(self.x, self.y)))
			self.duck_count -= 1
			if self.duck_count == 0:
				self.duck_count = 10
				self.is_duck = False
				self.y -= self.duck_y
		elif self.choose > 0:
			self.display.blit(self.dino_img1, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_img1), self.dino_img1.get_rect(center=(self.x, self.y)))
			self.choose -= 1
		elif self.choose <= 0:
			self.display.blit(self.dino_img2, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_img2), self.dino_img2.get_rect(center=(self.x, self.y)))
			self.choose -= 1
			if self.choose == -5:
				self.choose *= -1

	def game_flow(self):
		pygame.display.set_caption('T-Rex Rush')
		self.load_images()
		# self.ground_load()
		self.cactus_load()
		self.loop()

if __name__ == '__main__':
	pygame.init()
	obj = Canvas()
	obj.game_flow()
	pygame.quit()