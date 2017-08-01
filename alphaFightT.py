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
		self.foe = None
		
	def setFoe(self, foe):
		self.foe = foe
		
	def update(self, keypress):
		self.state.next(keypress)
		self.image = self.state.getImage()
		self.hitbox = self.state.getHit()
		self.hurtbox = self.state.getHurt()
		self.stopbox = self.state.getStopBox()
		moveTest = self.canMove()
		if(moveTest[0]):
			self.rect = self.rect.move(self.state.getMovement())
			if(self.state.getMovement()!=(0,0)):
				self.state.stopped = False
		else:
			self.state.stopped = True
			self.rect[0]=moveTest[1][0]
			self.rect[1]=moveTest[1][1]
	
	def getStopBox(self):
		return pygame.Rect(self.rect[0]+self.stopbox[0],self.rect[1]+self.stopbox[1],self.stopbox[2],self.stopbox[3])
		
	def getHitBox(self):
		return pygame.Rect(0,0,0,0)
		
	def getHurtBox(self):
		return pygame.Rect(0,0,0,0)
	
	def canMove(self):
		me = self.getStopBox().move(self.state.getMovement())
		you = self.foe.getStopBox()
		testRec = self.rect.move(self.state.getMovement())
		x = testRec[0]
		y = testRec[1]
		if(self.state.getMovement()==(0,0)):
			me = pygame.Rect(me[0]-2,me[1],me[2]+4,me[3])
		if(me.colliderect(you)):
			if(me.centerx>you.centerx):
				x = you.right-(me.left-x)
			else:
				x = you.left-me.width-(me.left-x)
			
			return (False, (x,y))
		else:
			return self.canMoveWalls()
	def canMoveWalls(self):
		testRec = self.rect.move(self.state.getMovement())
		x = testRec[0]
		y = testRec[1]
		if(testRec[0]<-45):
			x = -45
		elif(testRec[0]>width-55):
			x = width-55
		if(testRec[1]>170):
			y = 170
		elif(testRec[1]<-40):
			y = -40
		if(x != testRec[0] or y != testRec[1]):
			return (False,(x,y))
		return (True,None)
		
class FightState():
	def __init__(self,fileLoc,color,left):
		self.currentImage = pygame.image.load(fileLoc+".bmp").convert()
		self.currentImage.set_colorkey(color)
		self.setBoxes(self.readBoxFile(fileLoc+".txt"))
		self.facingLeft = left
		self.stopped = False
		self.move = (0,0)
		#self.stopBox = None
		#self.hurtBoxes = []
		#self.hitBoxes = []
		
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
		if(self.facingLeft):
			return self.stopBox
		else:
			return pygame.Rect(100-self.stopBox[0]-self.stopBox[2],self.stopBox[1],self.stopBox[2],self.stopBox[3])
	def getMovement(self):
		return self.move
		
	def strToRect(self, x):
		textArray = x.split(" ")
		numArray = [int(a) for a in textArray]
		return pygame.Rect(numArray[0],numArray[1],numArray[2]-numArray[0],numArray[3]-numArray[1])
		
	def readBoxFile(self,filename):
		f = open(filename, "r")
		stpBox = f.readline().strip()
		stopBoxT = self.strToRect(stpBox)
		twende = True
		hurtBoxT = []
		while(twende):
			holder = f.readline().strip()
			if(holder == "###"):
				twende = False
			else:
				hurtBoxT.append(self.strToRect(holder))
		twende = True
		hitBoxT = []
		while(twende):
			holder = f.readline().strip()
			if(holder == "###"):
				twende = False
			else:
				hitBoxT.append(self.strToRect(holder))
		f.close()
		return (stopBoxT,hurtBoxT,hitBoxT)
		
	def setBoxes(self, boxes):
		self.stopBox = boxes[0]
		self.hurtBoxes = boxes[1]
		self.hitBoxes = boxes[2]
		
	def getBoxes(self):
		return (self.stopBox, self.hurtBoxes, self.hitBoxes)
			
		

class LeafState(FightState):
	def __init__(self,left):
		FightState.__init__(self,"LeafBreath/LeafBrthFrm1",RED,left)
		self.state = "idle"
		self.holdingU = False
		self.holdingD = False
		self.holdingL = False
		self.holdingR = False
		self.holdingP = False
		self.holdingK = False
		self.move = (0,0)
		self.adjust = (0,0)
		self.idleImage = self.currentImage.copy()
		self.idleBoxes = self.getBoxes()
		self.attack1Image = [0,0,0,0,0]
		self.attack2Image = [0,0]
		self.cAttack1Image = [0,0,0,0,0]
		self.cAttack2Image = [0,0]
		self.stepImage = [0,0,0,0]
		self.breathImage = [0,0,0]
		self.jumpImage = [0,0]
		self.jAttack1Image = [0,0,0,0]
		self.jAttack2Image = [0,0]
		self.attack1Boxes = [0,0,0,0,0]
		self.attack2Boxes = [0,0]
		self.cAttack1Boxes = [0,0,0,0,0]
		self.cAttack2Boxes = [0,0]
		self.stepBoxes = [0,0,0,0]
		self.breathBoxes = [0,0,0]
		self.jumpBoxes = [0,0]
		self.jAttack1Boxes = [0,0,0,0]
		self.jAttack2Boxes = [0,0]
		self.frame = 0
		self.frame2 = 0
		self.jumpV = 0
		self.orth = 0
		self.crouchImage = pygame.image.load("LeafCrouch.bmp").convert()
		self.crouchImage.set_colorkey(RED)
		self.crouchBoxes = self.readBoxFile("LeafCrouch.txt")
		for i in range(0,5):
			self.attack1Image[i] = pygame.image.load("LeafAttack1/LeafAtk1Frm"+str(i+1)+".bmp").convert()
			self.attack1Image[i].set_colorkey(RED)
			self.attack1Boxes[i] = self.readBoxFile("LeafAttack1/LeafAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.attack2Image[i] = pygame.image.load("LeafAttack2/LeafAtk2Frm"+str(i+1)+".bmp").convert()
			self.attack2Image[i].set_colorkey(RED)
			self.attack2Boxes[i] = self.readBoxFile("LeafAttack2/LeafAtk2Frm"+str(i+1)+".txt")
		for i in range(0,5):
			self.cAttack1Image[i] = pygame.image.load("LeafCrouchAttack1/LeafCrchAtk1Frm"+str(i+1)+".bmp").convert()
			self.cAttack1Image[i].set_colorkey(RED)
			self.cAttack1Boxes[i] = self.readBoxFile("LeafCrouchAttack1/LeafCrchAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.cAttack2Image[i] = pygame.image.load("LeafCrouchAttack2/LeafCrchAtk2Frm"+str(i+1)+".bmp").convert()
			self.cAttack2Image[i].set_colorkey(RED)
			self.cAttack2Boxes[i] = self.readBoxFile("LeafCrouchAttack2/LeafCrchAtk2Frm"+str(i+1)+".txt")
		for i in range(0,4):
			self.stepImage[i] = pygame.image.load("LeafStep/LeafStpFrm"+str(i+1)+".bmp").convert()
			self.stepImage[i].set_colorkey(RED)
			self.stepBoxes[i] = self.readBoxFile("LeafStep/LeafStpFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.breathImage[i] = pygame.image.load("LeafBreath/LeafBrthFrm"+str(i+1)+".bmp").convert()
			self.breathImage[i].set_colorkey(RED)
			self.breathBoxes[i] = self.readBoxFile("LeafBreath/LeafBrthFrm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jumpImage[i] = pygame.image.load("LeafJump/LeafJmpFrm"+str(i+1)+".bmp").convert()
			self.jumpImage[i].set_colorkey(RED)
			self.jumpBoxes[i] = self.readBoxFile("LeafJump/LeafJmpFrm"+str(i+1)+".txt")
		for i in range(0,4):
			self.jAttack1Image[i] = pygame.image.load("LeafJumpAttack1/LeafJmpAtk1Frm"+str(i+1)+".bmp").convert()
			self.jAttack1Image[i].set_colorkey(RED)
			self.jAttack1Boxes[i] = self.readBoxFile("LeafJumpAttack1/LeafJmpAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jAttack2Image[i] = pygame.image.load("LeafJumpAttack2/LeafJmpAtk2Frm"+str(i+1)+".bmp").convert()
			self.jAttack2Image[i].set_colorkey(RED)
			self.jAttack2Boxes[i] = self.readBoxFile("LeafJumpAttack2/LeafJmpAtk2Frm"+str(i+1)+".txt")
		
	
	def next(self, keypress):
		self.adjust = (0,0)
		if("leftD" in keypress):self.holdingL=True
		if("leftU" in keypress):
			self.holdingL=False
			if(self.state=="leftForw"):
				self.adjust = (-(walkSpeed*self.frame/6),0)
			elif(self.state=="rightBack" and not self.stopped):
				self.adjust = (walkSpeed*self.frame/6,0)
		if("rightD" in keypress):self.holdingR=True
		if("rightU" in keypress):
			self.holdingR=False
			if(self.state=="rightForw"):
				self.adjust = (walkSpeed*self.frame/6,0)
			elif(self.state=="leftBack" and not self.stopped):
				self.adjust = (-walkSpeed*self.frame/6,0)
		if("downD" in keypress):self.holdingD=True
		if("downU" in keypress):self.holdingD=False
		if(self.state == "punch1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame == 6):
				self.currentImage = self.attack1Image[4]
				self.setBoxes(self.attack1Boxes[4])
			elif(self.frame == 5):
				self.currentImage = self.attack1Image[3]
				self.setBoxes(self.attack1Boxes[3])
			elif(self.frame == 4):
				self.currentImage = self.attack1Image[2]
				self.setBoxes(self.attack1Boxes[2])
			elif(self.frame == 2):
				self.currentImage = self.attack1Image[1]
				self.setBoxes(self.attack1Boxes[1])
		elif(self.state == "kick1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame == 3):
				self.currentImage = self.attack2Image[1]
				self.setBoxes(self.attack2Boxes[1])
		elif(self.state == "cPunch1"):
			self.frame += 1
			if(self.frame == 10):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			elif(self.frame == 5):
				self.currentImage = self.cAttack1Image[4]
				self.setBoxes(self.cAttack1Boxes[4])
			elif(self.frame == 4):
				self.currentImage = self.cAttack1Image[3]
				self.setBoxes(self.cAttack1Boxes[3])
			elif(self.frame == 3):
				self.currentImage = self.cAttack1Image[2]
				self.setBoxes(self.cAttack1Boxes[2])
			elif(self.frame == 2):
				self.currentImage = self.cAttack1Image[1]
				self.setBoxes(self.cAttack1Boxes[1])
		elif(self.state == "cKick1"):
			self.frame += 1
			if(self.frame == 15):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			elif(self.frame == 2):
				self.currentImage = self.cAttack2Image[1]
				self.setBoxes(self.cAttack2Boxes[1])
		elif(self.state in["jumping","jPunch1","jKick1"]):
			self.nextJump(keypress)
		elif(self.state in ["idle", "crouch", "leftForw", "leftBack", "rightForw", "rightBack"]):
			if("punchD" in keypress):
				if(self.state == "crouch"):
					self.state = "cPunch1"
					self.currentImage = self.cAttack1Image[1]
					self.setBoxes(self.cAttack1Boxes[1])
				else:
					self.state = "punch1"
					self.currentImage = self.attack1Image[1]
					self.setBoxes(self.attack1Boxes[1])
				self.frame = 0
				self.move = (0,0)
			elif("upD" in keypress):
				self.state = "jumping"
				self.frame = 0
				self.move = (0,0)
				self.jumpV = 16.5
			elif("kickD" in keypress):
				if(self.state == "crouch"):
					self.state = "cKick1"
					self.currentImage = self.cAttack2Image[0]
					self.setBoxes(self.cAttack2Boxes[0])
				else:
					self.state = "kick1"
					self.currentImage = self.attack2Image[0]
					self.setBoxes(self.attack2Boxes[0])
				self.frame = 0
				self.move = (0,0)
			elif(self.holdingD):
				self.state = "crouch"
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
				self.move = (0,0)
			elif(self.holdingL and not self.holdingR):
				if(self.state == "idle"):
					self.frame = 0
				if(not self.facingLeft):
					self.state = "rightBack"
				else:
					self.state = "leftForw"
			elif(self.holdingR and not self.holdingL):
				if(self.state == "idle"):
					self.frame = 0
				if(self.facingLeft):
					self.state = "leftBack"
				else:
					self.state = "rightForw"
			else:
				self.state = "idle"
				self.move = (0,0)
			
			if(self.state == "idle"):
				self.frame = (self.frame + 1)%40
				if(self.frame in [25,26,27,37,38,39]):
					self.currentImage = self.breathImage[1]
					self.setBoxes(self.breathBoxes[1])
				elif(self.frame in range(28,37)):
					self.currentImage = self.breathImage[2]
					self.setBoxes(self.breathBoxes[2])
				else:
					self.currentImage = self.breathImage[0]
					self.setBoxes(self.breathBoxes[0])
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
					self.frame = 5
					moveFrame = True
				elif(self.frame == 6):
					self.frame = 0
					moveFrame = True
				if(self.frame in [0]):
					self.currentImage = self.stepImage[0]
					self.setBoxes(self.stepBoxes[0])
				elif(self.frame in [1]):
					self.currentImage = self.stepImage[1]
					self.setBoxes(self.stepBoxes[1])
				elif(self.frame in [2,3]):
					self.currentImage = self.stepImage[2]
					self.setBoxes(self.stepBoxes[2])
				elif(self.frame in [4,5]):
					self.currentImage = self.stepImage[3]
					self.setBoxes(self.stepBoxes[3])
				if(moveFrame):
					if(self.state in ["leftForw","rightBack"]):
						self.move = (-1*walkSpeed,0)
					else:
						self.move = (walkSpeed,0)
				else:
					self.move = (0,0)
			self.move = (self.move[0] + self.adjust[0],self.move[1]+self.adjust[1])
					
	def nextJump(self, keypress):
		self.frame += 1
		if(self.frame >= 28):
			self.state = "idle"
			self.frame = 0
		elif(self.frame<5 or self.frame>=26):
			self.currentImage = self.jumpImage[0]
			self.setBoxes(self.jumpBoxes[0])
			self.move = (0,0)
			self.orth = 0
			self.state = "jumping"
			self.frame2 = 0
		else:
			if(self.state == "jumping"):
				self.currentImage = self.jumpImage[1]
				self.setBoxes(self.jumpBoxes[1])
			elif(self.state == "jPunch1"):
				self.frame2+=1
				if(self.frame2 == 10):
					self.state = "jumping"
				elif(self.frame2 == 6):
					self.currentImage = self.jAttack1Image[3]
					self.setBoxes(self.jAttack1Boxes[3])
				elif(self.frame2 == 5):
					self.currentImage = self.jAttack1Image[2]
					self.setBoxes(self.jAttack1Boxes[2])
				elif(self.frame2 == 3):
					self.currentImage = self.jAttack1Image[1]
					self.setBoxes(self.jAttack1Boxes[1])
				elif(self.frame2 == 1):
					self.currentImage = self.jAttack1Image[0]
					self.setBoxes(self.jAttack1Boxes[0])
			elif(self.state == "jKick1"):
				self.frame2+=1
				if(self.frame2==20):
					self.state = "jumping"
				elif(self.frame == 1):
					self.currentImage = self.jAttack2Image[0]
					self.setBoxes(self.jAttack2Boxes[0])
				else:
					self.currentImage = self.jAttack2Image[1]
					self.setBoxes(self.jAttack2Boxes[1])
			self.jumpV -= 1.5
			if("punchD" in keypress and self.state == "jumping"):
				self.state = "jPunch1"
				self.frame2 = 0
			elif("kickD" in keypress and self.state == "jumping"):
				self.state = "jKick1"
				self.frame2 = 0
			elif(self.holdingR and not self.holdingL):
				self.orth = 3.5
			elif(self.holdingL and not self.holdingR):
				self.orth = -3.5
			else:
				self.orth = 0
			self.move = (self.orth,-self.jumpV)
			
		
		

size = width, height = 600, 300
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW =(255, 255,   0)

walkSpeed = 14

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#pygame.key.set_repeat(500, 20)
forestStage = pygame.image.load("ForestStage.bmp").convert()
stage = forestStage
leaf = Fighter(LeafState(True),500,170)
clone = Fighter(LeafState(False),300,170)
player1 = leaf
player2 = clone

player1.setFoe(player2)
player2.setFoe(player1)

showCollisionBox = False
showHitBox = False
showHurtBox = False

while 1:
	clock.tick(frameRate)
	keypressA = []
	keypressB = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				keypressB.append("leftD")
			if event.key == pygame.K_RIGHT:
				keypressB.append("rightD")
			if event.key == pygame.K_UP:
				keypressB.append("upD")
			if event.key == pygame.K_COMMA:
				keypressB.append("punchD")
			if event.key == pygame.K_PERIOD:
				keypressB.append("kickD")
			if event.key == pygame.K_DOWN:
				keypressB.append("downD")
			if event.key == pygame.K_a:
				keypressA.append("leftD")
			if event.key == pygame.K_d:
				keypressA.append("rightD")
			if event.key == pygame.K_w:
				keypressA.append("upD")
			if event.key == pygame.K_v:
				keypressA.append("punchD")
			if event.key == pygame.K_b:
				keypressA.append("kickD")
			if event.key == pygame.K_s:
				keypressA.append("downD")
			if event.key == pygame.K_i:
				showCollisionBox = not showCollisionBox
			if event.key == pygame.K_o:
				showHitBox = not showHitBox
			if event.key == pygame.K_p:
				showHurtBox = not showHurtBox
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				keypressB.append("leftU")
			if event.key == pygame.K_RIGHT:
				keypressB.append("rightU")
			if event.key == pygame.K_UP:
				keypressB.append("upU")
			if event.key == pygame.K_COMMA:
				keypressB.append("punchU")
			if event.key == pygame.K_PERIOD:
				keypressB.append("kickU")
			if event.key == pygame.K_DOWN:
				keypressB.append("downU")
			if event.key == pygame.K_a:
				keypressA.append("leftU")
			if event.key == pygame.K_d:
				keypressA.append("rightU")
			if event.key == pygame.K_w:
				keypressA.append("upU")
			if event.key == pygame.K_v:
				keypressA.append("punchU")
			if event.key == pygame.K_b:
				keypressA.append("kickU")
			if event.key == pygame.K_s:
				keypressA.append("downU")
			
	
	player1.update(keypressA)
	player2.update(keypressB)
	
	if(player1.rect[0]<player2.rect[0]-10 and player1.state.facingLeft):
		player1.state.setFacing(False)
		player1.rect = player1.rect.move(5,0)
		player2.state.setFacing(True)
		player2.rect = player2.rect.move(-5,0)
	elif(player1.rect[0]-10>player2.rect[0] and player2.state.facingLeft):
		player1.state.setFacing(True)
		player1.rect = player1.rect.move(-5,0)
		player2.state.setFacing(False)
		player2.rect = player2.rect.move(5,0)
		
	screen.blit(stage, (0,0))
	screen.blit(player1.image,player1.rect)
	screen.blit(player2.image,player2.rect)
	if(showCollisionBox):
		s = pygame.Surface((600,400))
		s.set_alpha(128)
		s.fill(YELLOW)
		screen.blit(s,player1.getStopBox(),player1.getStopBox())
		screen.blit(s,player2.getStopBox(),player2.getStopBox())
	if(showHitBox):
		pygame.draw.rect(screen, GREEN, player1.getHitBox())
		pygame.draw.rect(screen, GREEN, player2.getHitBox())
	if(showHurtBox):
		pygame.draw.rect(screen, RED, player1.getHurtBox())
		pygame.draw.rect(screen, RED, player2.getHurtBox())
	pygame.display.flip()