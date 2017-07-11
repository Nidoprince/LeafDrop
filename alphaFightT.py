import pygame

class Fighter(pygame.sprite.Sprite):
	def __init__(self, fightState, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.state = fightState
		self.image = self.state.getImage()
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x,y)
		self.hitbox = self.state.getHit()
		self.hurtbox = self.state.getHurt()
		self.stopbox = self.state.getStopBox()
	
	def update(self, keypress):
		self.state.next(keypress)
		self.image = self.state.getImage()
		self.hitbox = self.state.getHit()
		self.hurtbox = self.state.getHurt()
		self.stopbox = self.state.getStopBox()
		self.rect = self.rect.move(self.state.getMovement())
		
class FightState():
	def __init__(self,imageLoc):
		self.currentImage = pygame.image.load(imageLoc).convert()
		self.currentImage.set_colorkey(WHITE)
		
	def getImage(self):
		return self.currentImage
	
	def next(self, keypress):
		return
	def getHit(self):
		return
	def getHurt(self):
		return
	def getStopBox(self):
		return
	def getMovement(self):
		return (0,0)

class LeafState(FightState):
	def __init__(self):
		FightState.__init__(self,"LeafBreath/LeafBrthFrm1.bmp")
		self.state = "idle"
		self.move = (0,0)
		self.facingLeft = True
		self.idleImage = self.currentImage.copy()
		self.attack1Image = [0,0,0,0,0,0]
		self.stepImage = [0,0,0,0]
		self.breathImage = [0,0,0]
		self.frame = 0
		self.crouchImage = pygame.image.load("LeafCrouch.bmp").convert()
		self.crouchImage.set_colorkey(WHITE)
		for i in range(1,6):
			self.attack1Image[i] = pygame.image.load("LeafAttack1/LeafAtk1Frm"+str(i)+".bmp").convert()
			self.attack1Image[i].set_colorkey(WHITE)
		for i in range(0,4):
			self.stepImage[i] = pygame.image.load("LeafStep/LeafStpFrm"+str(i+1)+".bmp").convert()
			self.stepImage[i].set_colorkey(WHITE)
		for i in range(0,3):
			self.breathImage[i] = pygame.image.load("LeafBreath/LeafBrthFrm"+str(i+1)+".bmp").convert()
			self.breathImage[i].set_colorkey(WHITE)
		
	
	def next(self, keypress):
		if(self.state == "punch1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
			elif(self.frame == 6):
				self.currentImage = self.attack1Image[5]
			elif(self.frame == 5):
				self.currentImage = self.attack1Image[4]
			elif(self.frame == 4):
				self.currentImage = self.attack1Image[3]
			elif(self.frame == 2):
				self.currentImage = self.attack1Image[2]
		elif(self.state in ["idle", "crouch", "leftForw", "leftBack", "rightForw", "rightBack"]):
			if(keypress == pygame.K_COMMA):
				self.state = "punch1"
				self.frame = 0
				self.currentImage = self.attack1Image[1]
				self.move = (0,0)
			elif(keypress == pygame.K_UP):
				self.state = "idle"
				self.currentImage = self.idleImage
				self.move = (0,0)
				self.facingLeft = not self.facingLeft
			elif(keypress == pygame.K_DOWN):
				self.state = "crouch"
				self.currentImage = self.crouchImage
				self.move = (0,0)
			elif(keypress == pygame.K_LEFT):
				if(self.state == "idle"):
					self.state = "leftForw"
					self.frame = 0
				elif(not self.facingLeft):
					self.state = "rightBack"
				else:
					self.state = "leftForw"
			elif(keypress == pygame.K_RIGHT):
				if(self.state == "idle"):
					self.state = "rightForw"
					self.frame = 0
				elif(self.facingLeft):
					self.state = "leftBack"
				else:
					self.state = "rightForw"
			
			if(self.state == "idle"):
				self.frame = (self.frame + 1)%40
				if(self.frame in [25,26,27,37,38,39]):
					self.currentImage = self.breathImage[1]
				elif(self.frame in range(28,37)):
					self.currentImage = self.breathImage[2]
				else:
					self.currentImage = self.breathImage[0]
			elif(self.state == "crouch"):
				self.frame = 0
			else:
				if(self.state in ["leftForw", "rightForw"]):
					self.frame += 1
				elif(self.state in ["leftBack", "rightBack"]):
					self.frame -= 1
				moveFrame = False
				if(self.frame == -1):
					self.frame = 10
					moveFrame = True
				elif(self.frame == 11):
					self.frame = 0
					moveFrame = True
				if(self.frame in [0,1,2,10]):
					self.currentImage = self.stepImage[0]
				elif(self.frame in [4,3]):
					self.currentImage = self.stepImage[1]
				elif(self.frame in [5,6]):
					self.currentImage = self.stepImage[2]
				elif(self.frame in [7,8,9]):
					self.currentImage = self.stepImage[3]
				if(moveFrame):
					if(self.state in ["leftForw","rightBack"]):
						self.move = (-16,0)
					else:
						self.move = (16,0)
				else:
					self.move = (0,0)
				
			
				
	def getMovement(self):
		return self.move
		
	def getImage(self):
		if(self.facingLeft):
			return self.currentImage
		else:
			return pygame.transform.flip(self.currentImage, True, False)
				
		

size = width, height = 600, 300
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 20)
forestStage = pygame.image.load("ForestStage.bmp").convert()
stage = forestStage
leaf = Fighter(LeafState(),500,170)

while 1:
	clock.tick(30)
	keypress = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				keypress = event.key
			if event.key == pygame.K_RIGHT:
				keypress = event.key
			if event.key == pygame.K_UP:
				keypress = event.key
			if event.key == pygame.K_COMMA:
				keypress = event.key
			if event.key == pygame.K_DOWN:
				keypress = event.key
	
	leaf.update(keypress)
		
	screen.blit(stage, (0,0))
	screen.blit(leaf.image,leaf.rect)
	pygame.display.flip()