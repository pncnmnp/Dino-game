import pygame
from time import sleep
from random import shuffle, uniform, randint

'''
TODO:
>> infinite vertical scrolling
>> add 'birds' obstacle
>> training AI to play this game
>> pause feature [ done ]
>> high score feature [ done ]
>> game sound [ done ]
>> start menu [ done ]
'''

class Characters(pygame.sprite.Sprite):
	def __init__(self, pos, image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

class Canvas:
	def __init__(self):
		self.width = 900
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
		self.mass = 0.4
		self.duck_y = 20
		self.dino_rect = None
		self.pos = [0.5, 1, 2, 3, 1.5, 2.5]
		self.clouds = [(0.5, 0.8), (1.3, 1.7), (2, 2.4)]
		self.cloud_pos = self.get_cloud_values()
		self.cactus_choose = list()
		self.cactus_rect = list()
		self.cactus_curr_img = None
		self.score = 0
		self.score_jump = 10
		self.highscore_file = './highscore.txt'
		self.highscore = self.get_highscore()
		self.scroll_ground = 1

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
		num_width, relative = 0, self.width-300
		self.display.blit(self.H_img, (relative+num_width+20, self.height*0.10))
		self.display.blit(self.I_img, (relative+num_width+40, self.height*0.10))
		num_width += 80
		for num in str(self.highscore):
			self.display.blit(self.numbers[int(num)], (relative+num_width, self.height*0.10))
			num_width += 20
		num_width += 60
		for num in str(self.score):
			self.display.blit(self.numbers[int(num)], (relative+num_width, self.height*0.10))
			num_width += 20

	def cactus_load(self):
		rand_index = randint(0, 4)
		self.cactus_curr_img = self.cactus_choose[rand_index][0]
		self.cactus_rect = self.cactus_choose[rand_index][0].get_rect()
		self.cactus_rect.bottom = self.height*0.52 + 80 + self.cactus_choose[rand_index][2]
		self.cactus_rect.left = self.width + self.cactus_rect.width

	def cactus_draw(self):
		self.display.blit(self.cactus_curr_img, self.cactus_rect)

	def cactus_update(self):
		move = [-4, 0]
		self.cactus_rect = self.cactus_rect.move(move)
		self.cactus_obj = Characters((self.x, self.y), self.cactus_curr_img)
		if self.cactus_rect.right < 0:
			# self.kill()
			pass

	def ground_load(self):
		self.ground_rect, self.ground_rect1 = self.ground.get_rect(), self.ground.get_rect()
		self.ground_rect.bottom, self.ground_rect1.bottom = self.height*0.52 + 90, self.height*0.52 + 90
		self.ground_rect.left = self.ground_rect1.right

	def ground_draw(self):
		self.display.blit(self.ground, self.ground_rect)
		self.display.blit(self.ground, self.ground_rect1)

	def ground_update(self):
		speed = -4
		self.ground_rect.left += speed
		self.ground_rect1.left += speed
		if self.ground_rect.right < 0:
			self.ground_rect.left = self.ground_rect1.right
		if self.ground_rect1.right < 0:
			self.ground_rect1.left = self.ground_rect.right

	def cloud_load(self):
		for index in range(len(self.cloud_pos)):
			self.display.blit(self.cloud, (int(self.width/4)*self.cloud_pos[index], self.height*0.30))

	def get_cloud_values(self):	
		return [round(uniform(self.clouds[i][0], self.clouds[i][1]), 2) for i in range(3)]

	def sun_load(self):
		self.display.blit(self.sun, (self.width-200, self.height*0.30))

	def space_to_start(self):
		self.display.blit(self.space_bar, (self.width/3, self.height*0.4))

	def check_next_frame(self):
		if self.x >= self.width-100:
			shuffle(self.pos)
			self.x = self.width * 0.005
			self.cactus_load()
			self.cloud_pos = self.get_cloud_values()
			self.fps += 5

	def load_paused_img(self):
		self.display.blit(self.paused, (self.width/2.5, self.height*0.4))

	def loop(self):
		self.crashed = False
		paused, not_started = False, True
		while self.crashed == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.crashed = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and not_started == True:
						not_started = not not_started
					elif event.key == pygame.K_UP:
						self.jump_sound.play()
						if not self.is_duck:
							if self.velocity == 1: self.velocity = 10
							self.is_jump = True
					elif event.key == pygame.K_DOWN:
						if not self.is_jump:
							if self.is_duck == False:
								self.y += self.duck_y
							self.is_duck = True
					elif event.key == pygame.K_p:
						self.pause_sound.play()
						paused = not paused
			if not_started:
				self.space_to_start()
			elif paused == False:
				self.not_paused()
			elif paused == True:
				self.load_paused_img()
			pygame.display.update()
			self.clock.tick(self.fps)
		self.game_over_sound.play()
		self.save_highscore()
		self.quit_message()

	def not_paused(self):
		self.display.fill(self.PAINT)
		self.load_elements()
		self.check_collision()
		self.x += 1.5

	def save_highscore(self):
		if self.score > int(self.highscore):
			with open(self.highscore_file, 'w') as f:
				f.write(str(self.score))
				f.close()

	def quit_message(self):
		self.fps = 50
		self.display.blit(self.game_over, (self.width/2.5, self.height*0.4))
		pygame.display.flip()
		sleep(3)

	def check_collision(self):
		offset_x = self.cactus_rect.center[0] - self.dino_rect[1].center[0]
		offset_y = self.cactus_rect.center[1] - self.dino_rect[1].center[1]
		if self.dino_rect[1].colliderect(self.cactus_rect):
			result = (self.dino_rect[0].mask).overlap(self.cactus_obj.mask, (offset_x, offset_y))
			if result:
				self.crashed = True

	def load_elements(self):
		self.sun_load()
		self.update_score()
		self.cloud_load()
		self.cactus_draw()
		self.cactus_update()
		self.dino()
		self.ground_update()
		self.ground_draw()
		self.check_next_frame()
		shuffle(self.cactus_choose)

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

	def load_images_and_audio(self):
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
		self.space_bar = pygame.image.load('./data/misc/space_to_start.png').convert_alpha()
		self.cloud = pygame.image.load('./data/misc/cloud.png').convert_alpha()
		self.game_over = pygame.image.load('./data/misc/game_over.png').convert_alpha()
		self.paused = pygame.image.load('./data/misc/paused.png').convert_alpha()
		self.H_img = pygame.image.load('./data/numbers/H.png').convert_alpha()
		self.I_img = pygame.image.load('./data/numbers/I.png').convert_alpha()

		self.jump_sound = pygame.mixer.Sound('./data/sound/jump.wav')
		self.game_over_sound = pygame.mixer.Sound('./data/sound/game_over.wav')
		self.pause_sound = pygame.mixer.Sound('./data/sound/pause.wav')

		nums = [None for i in range(10)]
		self.numbers = dict()

		for num in range(len(nums)):
			nums[num] = pygame.image.load('./data/numbers/'+str(num)+'.png')
			self.numbers[num] = nums[num]

		# arranged according to image, image_name, dist. from ground
		self.cactus_choose = [(self.cactus1, 'c1', 0), 
							  (self.cactus2, 'c2', 10), 
							  (self.cactus3, 'c3', 10), 
							  (self.cactus4, 'c4', 0), 
							  (self.cactus5, 'c5', 0)]

	def dino(self):
		if self.is_jump == True:
			self.display.blit(self.dino_jump, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_jump), 
								self.dino_jump.get_rect(center=(self.x, self.y)))
			self.jump()
		elif self.is_duck == True:
			if self.duck_choose > 0:
				self.display.blit(self.dino_duck1, (self.x, self.y))
				self.dino_rect = (Characters((self.x, self.y), self.dino_duck1), 
									self.dino_duck1.get_rect(center=(self.x, self.y)))
			self.duck_count -= 1
			if self.duck_count == 0:
				self.duck_count = 10
				self.is_duck = False
				self.y -= self.duck_y
		elif self.choose > 0:
			self.display.blit(self.dino_img1, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_img1), 
								self.dino_img1.get_rect(center=(self.x, self.y)))
			self.choose -= 1
		elif self.choose <= 0:
			self.display.blit(self.dino_img2, (self.x, self.y))
			self.dino_rect = (Characters((self.x, self.y), self.dino_img2), 
								self.dino_img2.get_rect(center=(self.x, self.y)))
			self.choose -= 1
			if self.choose == -5:
				self.choose *= -1

	def game_flow(self):
		pygame.display.set_caption('T-Rex Rush')
		# sound link : https://freesound.org/people/djgriffin/sounds/172567/
		self.main_music = pygame.mixer.Sound('./data/sound/game.wav')
		self.main_music.play(-1)
		self.load_images_and_audio()
		self.sun_load()
		self.cloud_load()
		self.ground_load()
		self.ground_draw()
		self.cactus_load()
		self.loop()

if __name__ == '__main__':
	pygame.init()
	obj = Canvas()
	obj.game_flow()
	pygame.quit()