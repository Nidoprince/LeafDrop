import pygame

class Fighter(pygame.sprite.Sprite):
	def __init__(self, fightState, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.state = fightState
		self.image = self.state.getImage()
		self.rect = self.image.get_rect()
		self.hitbox = self.state.getHit()
		self.hurtbox = self.state.getHurt()
		self.stopbox = self.state.getStopBox()
	
	def update(self, keypress):
		self.state.next(keypress)
		self.image = self.state.getImage()
		self.hitbox = self.state.getHit()
		self.hurtbox = self.state.getHurt()
		self.stopbox = self.state.getStopBox()
		self.rect.move(self.state.getMovement())
		
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
		FightState.__init__(self,"Leaf1.bmp")
		self.state = "idle"
		self.move = (0,0)
		self.facingLeft = True
		self.idleImage = self.currentImage.copy()
		self.attack1Image = []
		for i in range(1,6):
			self.attack1Image[i] = pygame.image.load("LeafAttack1/LeafAtk1Frm"+i+".bmp").convert()
			self.attack1Image[i].set_colorkey(WHITE)
	
	def next(self, keypress):
		if(self.state == "punch1"):
			self.frame += 1
			if(self.frame == 10):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
			elif(self.frame == 6):
				self.currentImage = self.attack1[5]
			elif(self.frame == 5):
				self.currentImage = self.attack1[4]
			elif(self.frame == 4):
				self.currentImage = self.attack1[3]
			elif(self.frame == 2):
				self.currentImage = self.attack1[2]
		elif(self.state == "idle"):
			if(keypress == pygame.K_COMMA):
				self.state = "punch1"
				self.frame = 0
				self.currentImage = self.attack1[1]
				self.move = (0,0)
			elif(keypress == pygame.K_LEFT):
				self.move = (-4,0)
				if(not self.facingLeft):
					self.facingLeft = True
			elif(keypress == pygame.K_RIGHT):
				self.move = (4,0)
				if(self.facingLeft):
					self.facingLeft = False
			elif(keypress == pygame.K_UP):
				self.move = (0,0)
	def getMovement(self):
		return self.move
				
		

size = width, height = 600, 300
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.key.set_repeat(500, 20)

leaf = pygame.image.load("Leaf1.bmp").convert()
leaf.set_colorkey(WHITE)
leaf = pygame.transform.scale2x(leaf)
leafPos = [400, 100]
leafMove = [0,0]
leafFaceLeft = True

while 1:
	clock.tick(30)
	leafMove = (0,0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				leafMove = (-3, 0)
				if not leafFaceLeft:
					leaf = pygame.transform.flip(leaf, True, False)
					leafFaceLeft = True
			if event.key == pygame.K_RIGHT:
				leafMove = (3, 0)
				if leafFaceLeft:
					leaf = pygame.transform.flip(leaf, True, False)
					leafFaceLeft = False
	
	leafPos[0] += leafMove[0]
	leafPos[1] += leafMove[1]
		
	screen.fill(GREEN)
	screen.blit(leaf,leafPos)
	pygame.display.flip()