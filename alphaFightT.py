import pygame

frameRate = 30

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
	def __init__(self,imageLoc,color,left):
		self.currentImage = pygame.image.load(imageLoc).convert()
		self.currentImage.set_colorkey(color)
		self.facingLeft = left
		
	def getImage(self):
		if(self.facingLeft):
			return self.currentImage
		else:
			return pygame.transform.flip(self.currentImage, True, False)
	
	def setFacing(self,isLeft):
		self.facingLeft = isLeft
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
	def __init__(self,left):
		FightState.__init__(self,"LeafBreath/LeafBrthFrm1.bmp",RED,left)
		self.state = "idle"
		self.move = (0,0)
		self.idleImage = self.currentImage.copy()
		self.attack1Image = [0,0,0,0,0]
		self.attack2Image = [0,0]
		self.cAttack1Image = [0,0,0,0,0]
		self.cAttack2Image = [0,0]
		self.stepImage = [0,0,0,0]
		self.breathImage = [0,0,0]
		self.jumpImage = [0,0]
		self.jAttack1Image = [0,0,0,0]
		self.jAttack2Image = [0,0]
		self.frame = 0
		self.frame2 = 0
		self.jumpV = 0
		self.orth = 0
		self.crouchImage = pygame.image.load("LeafCrouch.bmp").convert()
		self.crouchImage.set_colorkey(RED)
		for i in range(0,5):
			self.attack1Image[i] = pygame.image.load("LeafAttack1/LeafAtk1Frm"+str(i+1)+".bmp").convert()
			self.attack1Image[i].set_colorkey(RED)
		for i in range(0,2):
			self.attack2Image[i] = pygame.image.load("LeafAttack2/LeafAtk2Frm"+str(i+1)+".bmp").convert()
			self.attack2Image[i].set_colorkey(RED)
		for i in range(0,5):
			self.cAttack1Image[i] = pygame.image.load("LeafCrouchAttack1/LeafCrchAtk1Frm"+str(i+1)+".bmp").convert()
			self.cAttack1Image[i].set_colorkey(RED)
		for i in range(0,2):
			self.cAttack2Image[i] = pygame.image.load("LeafCrouchAttack2/LeafCrchAtk2Frm"+str(i+1)+".bmp").convert()
			self.cAttack2Image[i].set_colorkey(RED)
		for i in range(0,4):
			self.stepImage[i] = pygame.image.load("LeafStep/LeafStpFrm"+str(i+1)+".bmp").convert()
			self.stepImage[i].set_colorkey(RED)
		for i in range(0,3):
			self.breathImage[i] = pygame.image.load("LeafBreath/LeafBrthFrm"+str(i+1)+".bmp").convert()
			self.breathImage[i].set_colorkey(RED)
		for i in range(0,2):
			self.jumpImage[i] = pygame.image.load("LeafJump/LeafJmpFrm"+str(i+1)+".bmp").convert()
			self.jumpImage[i].set_colorkey(RED)
		for i in range(0,4):
			self.jAttack1Image[i] = pygame.image.load("LeafJumpAttack1/LeafJmpAtk1Frm"+str(i+1)+".bmp").convert()
			self.jAttack1Image[i].set_colorkey(RED)
		for i in range(0,2):
			self.jAttack2Image[i] = pygame.image.load("LeafJumpAttack2/LeafJmpAtk2Frm"+str(i+1)+".bmp").convert()
			self.jAttack2Image[i].set_colorkey(RED)
		
	
	def next(self, keypress):
		if(self.state == "punch1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
			elif(self.frame == 6):
				self.currentImage = self.attack1Image[4]
			elif(self.frame == 5):
				self.currentImage = self.attack1Image[3]
			elif(self.frame == 4):
				self.currentImage = self.attack1Image[2]
			elif(self.frame == 2):
				self.currentImage = self.attack1Image[1]
		elif(self.state == "kick1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
			elif(self.frame == 3):
				self.currentImage = self.attack2Image[1]
		elif(self.state == "cPunch1"):
			self.frame += 1
			if(self.frame == 10):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
			elif(self.frame == 5):
				self.currentImage = self.cAttack1Image[4]
			elif(self.frame == 4):
				self.currentImage = self.cAttack1Image[3]
			elif(self.frame == 3):
				self.currentImage = self.cAttack1Image[2]
			elif(self.frame == 2):
				self.currentImage = self.cAttack1Image[1]
		elif(self.state == "cKick1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
			elif(self.frame == 2):
				self.currentImage = self.cAttack2Image[1]
		elif(self.state in["jumping","jPunch1","jKick1"]):
			self.nextJump(keypress)
		elif(self.state in ["idle", "crouch", "leftForw", "leftBack", "rightForw", "rightBack"]):
			if(keypress == pygame.K_COMMA):
				if(self.state == "crouch"):
					self.state = "cPunch1"
					self.currentImage = self.cAttack1Image[1]
				else:
					self.state = "punch1"
					self.currentImage = self.attack1Image[1]
				self.frame = 0
				self.move = (0,0)
			elif(keypress == pygame.K_UP):
				self.state = "jumping"
				self.frame = 0
				self.move = (0,0)
				self.jumpV = 11
			elif(keypress == pygame.K_PERIOD):
				if(self.state == "crouch"):
					self.state = "cKick1"
					self.currentImage = self.cAttack2Image[0]
				else:
					self.state = "kick1"
					self.currentImage = self.attack2Image[0]
				self.frame = 0
				self.move = (0,0)
			elif(keypress == pygame.K_DOWN):
				self.state = "crouch"
				self.currentImage = self.crouchImage
				self.move = (0,0)
			elif(keypress == pygame.K_LEFT):
				if(self.state == "idle"):
					self.frame = 0
				if(not self.facingLeft):
					self.state = "rightBack"
				else:
					self.state = "leftForw"
			elif(keypress == pygame.K_RIGHT):
				if(self.state == "idle"):
					self.frame = 0
				if(self.facingLeft):
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
			elif(self.state in ["punch1","kick1","cPunch1","cKick1"]):
				True
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
				if(self.frame in [0,1,2]):
					self.currentImage = self.stepImage[0]
				elif(self.frame in [4,3]):
					self.currentImage = self.stepImage[1]
				elif(self.frame in [5,6,7]):
					self.currentImage = self.stepImage[2]
				elif(self.frame in [8,9,10]):
					self.currentImage = self.stepImage[3]
				if(moveFrame):
					if(self.state in ["leftForw","rightBack"]):
						self.move = (-1*walkSpeed,0)
					else:
						self.move = (walkSpeed,0)
				else:
					self.move = (0,0)
					
	def nextJump(self, keypress):
		self.frame += 1
		if(self.frame >= 28):
			self.state = "idle"
			self.frame = 0
		elif(self.frame<5 or self.frame>=26):
			self.currentImage = self.jumpImage[0]
			self.move = (0,0)
			self.orth = 0
			self.state = "jumping"
			self.frame2 = 0
		else:
			if(self.state == "jumping"):
				self.currentImage = self.jumpImage[1]
			elif(self.state == "jPunch1"):
				self.frame2+=1
				if(self.frame2 == 10):
					self.state = "jumping"
				elif(self.frame2 == 6):
					self.currentImage = self.jAttack1Image[3]
				elif(self.frame2 == 5):
					self.currentImage = self.jAttack1Image[2]
				elif(self.frame2 == 3):
					self.currentImage = self.jAttack1Image[1]
				elif(self.frame2 == 1):
					self.currentImage = self.jAttack1Image[0]
			elif(self.state == "jKick1"):
				self.frame2+=1
				if(self.frame2==20):
					self.state = "jumping"
				elif(self.frame == 1):
					self.currentImage = self.jAttack2Image[0]
				else:
					self.currentImage = self.jAttack2Image[1]
			self.jumpV -= 1
			if(keypress == pygame.K_COMMA and self.state == "jumping"):
				self.state = "jPunch1"
				self.frame2 = 0
			elif(keypress == pygame.K_PERIOD and self.state == "jumping"):
				self.state = "jKick1"
				self.frame2 = 0
			elif(keypress == pygame.K_RIGHT):
				self.orth = 2
			elif(keypress == pygame.K_LEFT):
				self.orth = -2
			elif(keypress == pygame.K_DOWN):
				self.orth = 0
			self.move = (self.orth,-self.jumpV)
			
			
				
	def getMovement(self):
		return self.move
		
		

size = width, height = 600, 300
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

walkSpeed = 14

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 20)
forestStage = pygame.image.load("ForestStage.bmp").convert()
stage = forestStage
leaf = Fighter(LeafState(True),500,170)
clone = Fighter(FightState("LeafBreath/LeafBrthFrm1.bmp",RED,False),300,170)
player1 = leaf
player2 = clone

while 1:
	clock.tick(frameRate)
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
			if event.key == pygame.K_PERIOD:
				keypress = event.key
			if event.key == pygame.K_DOWN:
				keypress = event.key
	
	player1.update(keypress)
	player2.update(keypress)
	
	if(player1.rect[0]<player2.rect[0]):
		player1.state.setFacing(False)
		player2.state.setFacing(True)
	else:
		player1.state.setFacing(True)
		player2.state.setFacing(False)
		
	screen.blit(stage, (0,0))
	screen.blit(player1.image,player1.rect)
	screen.blit(player2.image,player2.rect)
	pygame.display.flip()