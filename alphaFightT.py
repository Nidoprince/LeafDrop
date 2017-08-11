import pygame, sys

frameRate = 30

#Meta class for projectiles
class Projectile(pygame.sprite.Sprite):
	def __init__(self, images, x, y, velocity):
		pygame.sprite.Sprite.__init__(self)
		self.image = images[0]
		self.animations = images
		self.frame = 0
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x,y)
		self.vel = velocity
		
	def update(self):
		self.frame = (self.frame+1)%len(self.animations)
		self.image = self.animations[self.frame]
		self.rect = self.rect.move(self.vel)
		self.checkHit()
		self.checkBorder()
		
	def checkHit(self):
		True
		
	def checkBorder(self):
		if(self.rect.right < 0 or self.rect.left > width or self.rect.top > height or self.rect.bottom < 0):
			self.kill()


class DamagingProjectile(Projectile):
	def __init__(self, images, x, y, velocity, damage, stunTime):
		Projectile.__init__(self, images, x, y, velocity)
		self.damage = damage
		self.stunTime = stunTime
		self.foe = None
		
	def setFoe(self, foe):
		self.foe = foe
		
	def checkHit(self):
		enemy = self.foe.getHitBoxes()
		if(self.rect.collidelist(enemy)!=-1):
			if(self.foe.state.isBlocking):
				self.foe.state.setBlock(int(self.stunTime/2), 0)
			else:
				self.foe.state.setHit(self.stunTime, self.damage)
			self.kill()
			
	def destroy(self):
		self.kill()
		

#Basic class of the combatants in the game.  Contains functions dealing with a given character's interaction with 
#the opposing fighter, and the stage around them.
class Fighter(pygame.sprite.Sprite):
	def __init__(self, fightState, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.state = fightState
		self.image = self.state.getImage()
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x,y)
		self.stopbox = self.state.getStopBox()
		self.projectiles = pygame.sprite.Group()
		self.foe = None
		
	#Sets who the opponent is so they can call each others methods and look at each others hit boxes	
	def setFoe(self, foe):
		self.foe = foe
		
	#Adds a new projecile to the list
	def addProjectile(self, images, x, y, velocity, damage, stun):
		proj = DamagingProjectile(images, x+self.rect[0], y+self.rect[1], velocity, damage, stun)
		proj.setFoe(self.foe)
		self.projectiles.add(proj)
	
	#Checks to see if their is a projectile to snag
	def checkProjectile(self):
		if(self.state.projectile):
			proj = self.state.projectile
			self.addProjectile(proj[0],proj[1],proj[2],proj[3],proj[4],proj[5])
			self.state.clearProjectile()
		
	#Called every frame to update whats happening.  Calls the State update method which does most of the heavy lifting.
	#Deals with movement and collision detection and stuff.
	def update(self, keypress):
		self.state.next(keypress)
		self.image = self.state.getImage()
		self.stopbox = self.state.getStopBox()
		moveTest = self.canMove()
		self.checkHit()
		self.checkProjectile()
		self.projectiles.update()
		pygame.sprite.groupcollide(self.projectiles,self.foe.projectiles,True,True)
		if(moveTest[0]):
			self.rect = self.rect.move(self.state.getMovement())
			if(self.state.getMovement()!=(0,0)):
				self.state.stopped = False
				#Turns player to face enemy if they are facing the wrong way and move towards them.
				if(self.state.facingLeft and self.state.getMovement()[0] > 0 and self.rect[0]<self.foe.rect[0]-10):
					self.state.facingLeft = False
					self.rect = self.rect.move(5,0)
				elif(not self.state.facingLeft and self.state.getMovement()[0] < 0 and self.rect[0]-10>self.foe.rect[0]):
					self.state.facingLeft = True
					self.rect = self.rect.move(-5,0)
		else:
			self.state.stopped = True
			self.rect[0]=moveTest[1][0]
			self.rect[1]=moveTest[1][1]
	
	def getStopBox(self):
		return pygame.Rect(self.rect[0]+self.stopbox[0],self.rect[1]+self.stopbox[1],self.stopbox[2],self.stopbox[3])
		
	def getHitBoxes(self):
		return [pygame.Rect(self.rect[0]+a[0],self.rect[1]+a[1],a[2],a[3]) for a in self.state.getHitBoxes()]
		
	def getHurtBoxes(self):
		return [pygame.Rect(self.rect[0]+a[0],self.rect[1]+a[1],a[2],a[3]) for a in self.state.getHurtBoxes()]
	
	#Checks to see if any of its hurt boxes intersect with the enemies hit boxes
	#If so, it calls setHit on the enemy, making them react to the damage.
	def checkHit(self):
		if(self.state.isHurting):
			enemy = self.foe.getHitBoxes()
			enemyProj = self.foe.projectiles
			me = self.getHurtBoxes()
			for x in enemyProj:
				if(x.rect.collidelist(me)!=-1):
					x.destroy()
			for x in me:
				if(x.collidelist(enemy)!=-1):
					self.state.stopHurting()
					if(self.foe.state.isBlocking and ((self.state.getMetaState()!="jump" and self.foe.state.getMetaState()=="crouch") or (self.state.getMetaState()!="crouch" and self.foe.state.getMetaState()=="land"))):
						self.foe.state.setBlock(10,0)
						self.state.attackLag = 15
					else:
						self.foe.state.setHit(20,0)
						self.state.attackLag = 0
	
	#Returns all the rects of all the projects
	def getProjRect(self):
		out = []
		for x in self.projectiles:
			out.append(x.rect)
		return out
		
	#Checks to see if movement is possible or if you are walking into a wall or enemy.
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
	
	#subfunction of above, this part deals with walls in particular
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

#Super class for the internal state of a fighter.  This deals with sprites, attack animations, hit boxes,
#and all the internals of the fighter that are not explicitly connected to the other character or the map.		
class FightState():
	def __init__(self,fileLoc,color,left):
		#Loads intial image and box data for character from file
		self.currentImage = pygame.image.load(fileLoc+".bmp").convert()
		self.currentImage.set_colorkey(color)
		self.setBoxes(self.readBoxFile(fileLoc+".txt"))
		self.facingLeft = left #Determines which direction character is facing
		self.stopped = False #Flag used when stopped by walls or other characters to prevent some jittering motions
		self.move = (0,0) #Movement distance sent to the Fighter class each frame.
		self.punchTimer = 0 #Determines how long stunned by an attack
		self.state = "idle" #Tells what the character is in the process of doing.  The most important variable in the class.
		self.isHurting = False #Turns on and off hurt boxes.
		self.attackLag = 0 #Adds or subtracts time attack delays before you can move again
		self.isBlocking = False #Tells if you are blocking
		self.comboMem = [] #Remembers your last few commands for the purposes of special attacks.
		self.projectile = None #Holds any projectiles the character might fire
		self.health = 150 #Current Health
		
	def getImage(self):
		if(self.facingLeft):
			return self.currentImage
		else:
			return pygame.transform.flip(self.currentImage, True, False)
	
	def setFacing(self,isLeft):
		self.facingLeft = isLeft
		
	def next(self, keypress):
		return
		
	def getHitBoxes(self):
		if(self.facingLeft):
			return self.hitBoxes
		else:
			return [pygame.Rect(100-a[0]-a[2],a[1],a[2],a[3]) for a in self.hitBoxes]
			
	def getHurtBoxes(self):
		if(self.facingLeft):
			return self.hurtBoxes
		else:
			return [pygame.Rect(100-a[0]-a[2],a[1],a[2],a[3]) for a in self.hurtBoxes]
		
	def getStopBox(self):
		if(self.facingLeft):
			return self.stopBox
		else:
			return pygame.Rect(100-self.stopBox[0]-self.stopBox[2],self.stopBox[1],self.stopBox[2],self.stopBox[3])

	def getMovement(self):
		return self.move
	
	def clearProjectile(self):
		self.projectile = None
		
	def setProjectile(self, images, x, y, vel, damage, stun):
		if(not self.facingLeft):
			r = images[0].get_rect()
			x = 100-x-r.width
			vel = (-vel[0],vel[1])
		self.projectile = [images, x, y, vel, damage, stun]
	
	#Dummy function for a land/crouch/jump check
	def getMetaState(self):
		return "land"
	
	#Really shouldnt be in here, but this turns a string of the coordinates of the diagonal corners of a rectangle
	#into a Rect object
	def strToRect(self, x):
		textArray = x.split(" ")
		numArray = [int(a) for a in textArray]
		return pygame.Rect(numArray[0],numArray[1],numArray[2]-numArray[0],numArray[3]-numArray[1])
		
	#Reads a text file associated with each frame of animation that contains the stop, hit, and hurt boxes for that
	#frame
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
	
	#called when hit by enemies attack.  Sets length of time you are in the "hit" state
	def setHit(self, punchTime, damage):
		self.state = "hit"
		self.frame = 0
		self.punchTimer = punchTime
	
	#called when hit by enemies while blocking.  
	def setBlock(self, punchTime, damage):
		self.state = "blocking"
		self.frame = 0
		self.punchTimer = punchTime
	
	#Used to turn off hurtboxes in an attack once it has hit something.
	def stopHurting(self):
		self.isHurting = False
		
	#Sets some variables needed when starting an attack.
	def attack(self):
		self.isHurting = True
		self.attackLag = 0
		
	#Adds new commands to combo memory while forgetting very old ones
	def moveRemember(self, newCommands):
		self.comboMem = self.comboMem + newCommands
		self.comboMem = self.comboMem[-10:]
		
			
		
#The subClass of the FightState specifically for the character Leaf.  This controls his animations, his frames,
#how he reacts to user input, everything.
class LeafState(FightState):
	#Sets all the variables.  Probably pretty bloated.  
	def __init__(self,left):
		FightState.__init__(self,"LeafBreath/LeafBrthFrm1",RED,left)
		
		#Used to tell if a particular keyboard key is currently held down or not.
		self.holdingU = False
		self.holdingD = False
		self.holdingL = False
		self.holdingR = False
		self.holdingP = False
		self.holdingK = False
		
		self.adjust = (0,0) #If movement is interupted during a walk cycle, this adjusts the character an appropriate fractional distance of a step.
		self.frame = 0 #Keeps track of how far into each task one is.
		self.frame2 = 0 #Keeps track of how far into a second task one is if two are happening concurrently.  
		self.jumpV = 0 #The vertical velocity of a jump
		self.orth = 0 #How far a character is moving left or right while jumping
		self.walkSpeed = 14 #Determines how many pixels each step covers
		
		#Initializes all the lists for different animations' images
		self.hitImage = [0,0]
		self.attack1Image = [0,0,0,0,0]
		self.attack2Image = [0,0]
		self.cAttack1Image = [0,0,0,0,0]
		self.cAttack2Image = [0,0]
		self.stepImage = [0,0,0,0]
		self.breathImage = [0,0,0]
		self.jumpImage = [0,0]
		self.jAttack1Image = [0,0,0,0]
		self.jAttack2Image = [0,0]
		self.sAttack1Image = [0,0,0]
		#Initializes all the lists for differnet animations' boxes
		self.hitBox = [0,0] #Uses a slightly different naming format than all the rest because of the previously existing "hitBoxes" variable.
		self.attack1Boxes = [0,0,0,0,0]
		self.attack2Boxes = [0,0]
		self.cAttack1Boxes = [0,0,0,0,0]
		self.cAttack2Boxes = [0,0]
		self.stepBoxes = [0,0,0,0]
		self.breathBoxes = [0,0,0]
		self.jumpBoxes = [0,0]
		self.jAttack1Boxes = [0,0,0,0]
		self.jAttack2Boxes = [0,0]
		self.sAttack1Boxes = [0,0,0]
		#Initialize projectile images
		self.tankenImage = [0,0,0]
		
		#Sets all the single frame animation variables for sprites and hitboxes
		self.idleImage = self.currentImage.copy() 
		self.idleBoxes = self.getBoxes()
		self.crouchImage = pygame.image.load("LeafCrouch.bmp").convert()
		self.crouchImage.set_colorkey(RED)
		self.crouchBoxes = self.readBoxFile("LeafCrouch.txt")
		self.crouchHitImage = pygame.image.load("LeafCrouchHit.bmp").convert()
		self.crouchHitImage.set_colorkey(RED)
		self.crouchHitBoxes = self.readBoxFile("LeafCrouchHit.txt")
		self.blockHiImage = pygame.image.load("LeafBlock.bmp").convert()
		self.blockHiImage.set_colorkey(RED)
		self.blockHiBoxes = self.readBoxFile("LeafBlock.txt")
		self.blockLowImage = pygame.image.load("LeafCrouchBlock.bmp").convert()
		self.blockLowImage.set_colorkey(RED)
		self.blockLowBoxes = self.readBoxFile("LeafCrouchBlock.txt")
		
		
		#And here is all the multiframe animation data setting
		for i in range(0,2):
			self.hitImage[i] = pygame.image.load("LeafHit/LeafHitFrm"+str(i+1)+".bmp").convert()
			self.hitImage[i].set_colorkey(RED)
			self.hitBox[i] = self.readBoxFile("LeafHit/LeafHitFrm"+str(i+1)+".txt")
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
		for i in range(0,3):
			self.sAttack1Image[i] = pygame.image.load("LeafSpecial1/LeafHtkFrm"+str(i+1)+".bmp").convert()
			self.sAttack1Image[i].set_colorkey(RED)
			self.sAttack1Boxes[i] = self.readBoxFile("LeafSpecial1/LeafHtkFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.tankenImage[i] = pygame.image.load("HaNoTanken/HntknFrm"+str(i+1)+".bmp").convert()
			self.tankenImage[i].set_colorkey(RED)
		
	#The super bloated mega method. This runs each frame to update everything and its brother, depending on state, and keyboard input.
	def next(self, keypress):
	
		self.moveRemember(keypress)
		self.isBlocking = False
	
		#Deals with keyboard input that cares about being held down as opposed to just pressed.  
		#Also deals with adjustment nessessary if step animations interupted, because it normally only
		#adjusts the location after each full step cycle.  
		self.adjust = (0,0)
		if("leftD" in keypress):self.holdingL=True
		if("leftU" in keypress):
			self.holdingL=False
			if(self.state=="leftForw"):
				self.adjust = (-(self.walkSpeed*self.frame/6),0)
			elif(self.state=="rightBack" and not self.stopped):
				self.adjust = (self.walkSpeed*self.frame/6,0)
		if("rightD" in keypress):self.holdingR=True
		if("rightU" in keypress):
			self.holdingR=False
			if(self.state=="rightForw"):
				self.adjust = (self.walkSpeed*self.frame/6,0)
			elif(self.state=="leftBack" and not self.stopped):
				self.adjust = (-self.walkSpeed*self.frame/6,0)
		if("downD" in keypress):self.holdingD=True
		if("downU" in keypress):self.holdingD=False
		
		if(self.state == "hit"): #Animation when struck
			self.frame += 1
			if(self.frame == self.punchTimer):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame <= 2):
				self.currentImage = self.hitImage[0]
				self.setBoxes(self.hitBox[0])
			else:
				self.currentImage = self.hitImage[1]
				self.setBoxes(self.hitBox[1])
		elif(self.state == "blocking"): #Animation when blocking
			self.frame += 1
			if(self.frame == self.punchTimer):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			else:
				self.currentImage = self.blockHiImage
				self.setBoxes(self.blockHiBoxes)
		elif(self.state == "crouchHit"): #Animation when struck while crouching
			self.frame += 1
			if(self.frame == self.punchTimer):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			else:
				self.currentImage = self.crouchHitImage
				self.setBoxes(self.crouchHitBoxes)
		elif(self.state == "crouchBlocking"): #Animation when blocking while crouching
			self.frame += 1
			if(self.frame == self.punchTimer):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			else:
				self.currentImage = self.blockLowImage
				self.setBoxes(self.blockLowBoxes)
		elif(self.state == "sAttack1"): #Animation for the Ha no Tanken Speical Attack
			self.frame += 1
			if(self.frame == 15):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame == 6):
				self.currentImage = self.sAttack1Image[2]
				self.setBoxes(self.sAttack1Boxes[2])
				self.setProjectile(self.tankenImage,30,35,(-7,0),20,15)
			elif(self.frame == 3):
				self.currentImage = self.sAttack1Image[1]
				self.setBoxes(self.sAttack1Boxes[1])
		elif(self.state == "punch1"): #Animation when performing basic sword attack while standing
			self.frame += 1
			if(self.frame == 15+self.attackLag):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame == 7):
				self.isHurting = False
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
		elif(self.state == "kick1"):  #Animation for basic kick while standing
			self.frame += 1
			if(self.frame == 15+self.attackLag):
				self.state = "idle"
				self.frame = 0
				self.currentImage = self.idleImage
				self.setBoxes(self.idleBoxes)
			elif(self.frame == 5):
				self.isHurting = False
			elif(self.frame == 3):
				self.currentImage = self.attack2Image[1]
				self.setBoxes(self.attack2Boxes[1])
		elif(self.state == "cPunch1"):  #Animation for basic sword strike while crouching
			self.frame += 1
			if(self.frame == 10+self.attackLag):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			elif(self.frame == 6):
				self.isHurting = False
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
		elif(self.state == "cKick1"): #Animation for basic kick while crouching
			self.frame += 1
			if(self.frame == 5+self.attackLag):
				self.state = "crouch"
				self.frame = 0
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
			elif(self.frame == 4):
				self.isHurting = False
			elif(self.frame == 2):
				self.currentImage = self.cAttack2Image[1]
				self.setBoxes(self.cAttack2Boxes[1])
		elif(self.state in["jumping","jPunch1","jKick1","jumpHit"]): #Jumps to special jumping function.  Haha
			self.nextJump(keypress)
		elif(self.state in ["idle", "crouch", "leftForw", "leftBack", "rightForw", "rightBack"]): #Logic for passive states that you can initiate attacks from.
			if("punchD" in keypress): #Starts basic sword swing.
				if(self.specialCheckStart()): #Tests for special attacks
					True
				elif(self.state == "crouch"): #When crouched
					self.state = "cPunch1"
					self.currentImage = self.cAttack1Image[1]
					self.setBoxes(self.cAttack1Boxes[1])
				else: #When standing
					self.state = "punch1"
					self.currentImage = self.attack1Image[1]
					self.setBoxes(self.attack1Boxes[1])
				self.frame = 0
				self.move = (0,0)
				self.attack()
			elif("upD" in keypress): #Starts jumping
				self.state = "jumping"
				self.frame = 0
				self.move = (0,0)
				self.jumpV = 16.5 #This tells us how fast we are jumping upward.  Currently very specific number needed or you won't land on the ground, but will instead fly.
			elif("kickD" in keypress): 
				if(self.state == "crouch"): #Start kicking while crouched
					self.state = "cKick1"
					self.currentImage = self.cAttack2Image[0]
					self.setBoxes(self.cAttack2Boxes[0])
				else: #Start kicking while standing
					self.state = "kick1"
					self.currentImage = self.attack2Image[0]
					self.setBoxes(self.attack2Boxes[0])
				self.frame = 0
				self.move = (0,0)
				self.attack()
			elif(self.holdingD): #Start or continue crouching
				self.state = "crouch"
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
				self.move = (0,0)
				if((self.facingLeft and self.holdingR) or (not self.facingLeft and self.holdingL)):
					self.isBlocking = True
			elif(self.holdingL and not self.holdingR): #Start or continue walking left
				if(self.state == "idle"):
					self.frame = 0
				if(not self.facingLeft):
					self.state = "rightBack"
					self.isBlocking = True
				else:
					self.state = "leftForw"
			elif(self.holdingR and not self.holdingL): #Start or continue walking right
				if(self.state == "idle"):
					self.frame = 0
				if(self.facingLeft):
					self.state = "leftBack"
					self.isBlocking = True
				else:
					self.state = "rightForw"
			else: #Start or continue standing still
				self.state = "idle"
				self.move = (0,0)
			
			if(self.state == "idle"): #Breathing animation for when standing still
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
			elif(self.state == "crouch"): #Do nothing if crouching
				self.frame = 0
			elif(self.state in ["punch1","kick1","cPunch1","cKick1"]): #Do even more nothing if currently attacking
				True
			else: #Deal with walking animation. Generic for walking forward or backwards.
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
				if(moveFrame): #Actually move about when at the end of a step animation
					if(self.state in ["leftForw","rightBack"]):
						self.move = (-1*self.walkSpeed,0)
					else:
						self.move = (self.walkSpeed,0)
				else:
					self.move = (0,0)
			self.move = (self.move[0] + self.adjust[0],self.move[1]+self.adjust[1])
		
	#Checks for special attacks able to be performed and initiates them if possible
	def specialCheckStart(self):
		combo = False
		if(self.facingLeft):
			if(self.comboMem[-4:] == ["downD","leftD","downU","punchD"]):
				combo = "hanotanken"
		else:
			if(self.comboMem[-4:] == ["downD","rightD","downU","punchD"]):
				combo = "hanotanken"
		
		if(combo == "hanotanken"):
			self.state = "sAttack1"
			self.currentImage = self.sAttack1Image[0]
			self.currentBoxes = self.sAttack1Boxes[0]
		
		return combo
	
	
	#Sets appropriate state and conditions when struck by enemy.
	def setHit(self, punchTime, damage):
		if(self.getMetaState() == "land"):
			self.state = "hit"
			self.frame = 0
		elif(self.getMetaState() == "crouch"):
			self.state = "crouchHit"
			self.frame = 0
		else:
			self.state = "jumpHit"
			self.frame2 = 0
		self.punchTimer = punchTime
		self.move = (0,0)
		self.isHurting = False
		self.health = self.health - damage
		if(self.health<0):
			self.health = 0
		
	#Sets appropriate state and conditions when struck by enemy.
	def setBlock(self, punchTime, damage):
		if(self.getMetaState() == "land"):
			self.state = "blocking"
			self.frame = 0
		elif(self.getMetaState() == "crouch"):
			self.state = "crouchBlocking"
			self.frame = 0
		self.punchTimer = punchTime
		self.move = (0,0)
		self.isHurting = False
		
	#Tells if jumping, standing, or crouching
	def getMetaState(self):
		if(self.state in ["crouch","cPunch1","cKick1","crouchHit","crouchBlocking"]):
			return "crouch"
		elif(self.state in ["jumping","jumpHit","jKick1","jPunch1"]):
			return "jump"
		else:
			return "land"
	
	#Deals with animations when in the process of jumping
	def nextJump(self, keypress):
		self.frame += 1
		if(self.frame >= 28): #Deals with landing
			if(self.state=="jumpHit"):
				self.state = "hit"
				self.frame = self.frame2
			else:
				self.state = "idle"
				self.frame = 0
		elif(self.frame<5 or self.frame>=26): #Deals with first starting or ending a jump
			if(self.state=="jumpHit"):
				self.state = "hit"
				self.frame = self.frame2
			else:
				self.currentImage = self.jumpImage[0]
				self.setBoxes(self.jumpBoxes[0])
				self.state = "jumping"
			self.frame2 = 0
			self.move = (0,0)
			self.orth = 0
		else: #Deals with the actual "in the air" part of jumping
			if(self.state == "jumpHit"):
				self.frame2+=1
				if(self.frame2 == self.punchTimer):
					self.state = "jumping"
					self.currentImage = self.jumpImage[1]
					self.setBoxes(self.jumpBoxes[1])
				else:
					self.currentImage = self.hitImage[0]
					self.setBoxes(self.hitBox[0])
			elif(self.state == "jumping"): #When just jumping
				self.currentImage = self.jumpImage[1]
				self.setBoxes(self.jumpBoxes[1])
			elif(self.state == "jPunch1"): #When swinging a sword while jumping
				self.frame2+=1
				if(self.frame2 == 10+self.attackLag):
					self.state = "jumping"
				elif(self.frame2 == 7):
					self.isHurting = False
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
			elif(self.state == "jKick1"): #When kicking while jumping
				self.frame2+=1
				if(self.frame2==20+self.attackLag):
					self.state = "jumping"
				elif(self.frame == 1):
					self.currentImage = self.jAttack2Image[0]
					self.setBoxes(self.jAttack2Boxes[0])
				else:
					self.currentImage = self.jAttack2Image[1]
					self.setBoxes(self.jAttack2Boxes[1])
			self.jumpV -= 1.5 #Accelerate down
			if("punchD" in keypress and self.state == "jumping"): #Start sword swinging
				self.state = "jPunch1"
				self.frame2 = 0
				self.attack()
			elif("kickD" in keypress and self.state == "jumping"): #Start kicking
				self.state = "jKick1"
				self.frame2 = 0
				self.attack()
			elif(self.state == "jumpHit"): #Can't move while struck
				self.orth = 0
			elif(self.holdingR and not self.holdingL): #Go Right young Meowth
				self.orth = 3.5
			elif(self.holdingL and not self.holdingR): #Go Left young Meowth
				self.orth = -3.5
			else: #Don't move
				self.orth = 0
			self.move = (self.orth,-self.jumpV)

#Used to keep track of health from 1 second ago.  
class OldHealth():
	def __init__(self):
		self.p1Health = [100]
		self.p2Health = [100]
	def iterate(self):
		self.p1Health.append(player1.state.health)
		self.p1Health = self.p1Health[-30:]
		self.p2Health.append(player2.state.health)
		self.p2Health = self.p2Health[-30:]
		return [self.p1Health[0],self.p2Health[0]]
		
def drawHUD():
	healths = oldHealths.iterate()
	p1Status = GREEN
	p2Status = GREEN
	if(player1.state.state in ["hit","crouchHit","jumpHit"]):
		p1Status = RED
	if(player1.state.state in ["blocking","crouchBlocking"]):
		p1Status = BLUE
	if(player2.state.state in ["hit","crouchHit","jumpHit"]):
		p2Status = RED
	if(player2.state.state in ["blocking","crouchBlocking"]):
		p2Status = BLUE
	pygame.draw.rect(screen, BLUE, [50, 5, 150, 20])
	pygame.draw.rect(screen, BLUE, [width-200, 5, 150, 20])
	pygame.draw.rect(screen, RED, [50, 5, healths[0], 20])
	pygame.draw.rect(screen, RED, [width-50-healths[1], 5, healths[1], 20])
	pygame.draw.rect(screen, GREEN, [50, 5, player1.state.health, 20])
	pygame.draw.rect(screen, GREEN, [width-50-player2.state.health, 5, player2.state.health, 20])
	pygame.draw.rect(screen, p1Status, [5, 5, 40, 45])
	pygame.draw.rect(screen, p2Status, [width-45, 5, 40, 45])
	pygame.draw.rect(screen, BLACK, [49, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [width-202, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [5, 5, 40, 45], 3)
	pygame.draw.rect(screen, BLACK, [width-45, 5, 40, 45], 3)
	pygame.draw.rect(screen, BLACK, [50, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [75, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [100, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [125, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [150, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [width-66, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [width-91, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [width-116, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [width-141, 30, 15, 15], 2)
	pygame.draw.rect(screen, BLACK, [width-166, 30, 15, 15], 2)
	
	
		

size = width, height = 600, 300 #Determines the size of the screen.
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW =(255, 255,   0)

#Initialization stuff
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
forestStage = pygame.image.load("ForestStage.bmp").convert() #Sets background image
stage = forestStage
leaf = Fighter(LeafState(False),200,170) # Makes fighter1
clone = Fighter(LeafState(True),400,170) # Makes fighter2
player1 = leaf
player2 = clone

player1.setFoe(player2)
player2.setFoe(player1)
oldHealths = OldHealth() #Keeps track of healths from a second ago

#Toggles for animation of various hit boxes
showCollisionBox = False
showHitBox = False
showHurtBox = False

while 1: #Main game loop
	clock.tick(frameRate) #Makes sure it runs at appropriate frame rate
	keypressA = [] #Holder for player 1's input
	keypressB = [] #Holder for player 2's input
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN: #Buttons pressed
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
		if event.type == pygame.KEYUP: #Buttons released
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
			
	#Run the logic for the two characters
	player1.update(keypressA) 
	player2.update(keypressB)
	
	#Draw stuff on the screen	
	screen.blit(stage, (0,0))
	screen.blit(player1.image,player1.rect)
	screen.blit(player2.image,player2.rect)
	for x in player1.projectiles:
		screen.blit(x.image,x.rect)
	for y in player2.projectiles:
		screen.blit(y.image,y.rect)
	if(showCollisionBox):
		s = pygame.Surface((600,400))
		s.set_alpha(128)
		s.fill(YELLOW)
		screen.blit(s,player1.getStopBox(),player1.getStopBox())
		screen.blit(s,player2.getStopBox(),player2.getStopBox())
	if(showHitBox):
		s = pygame.Surface((600,400))
		s.set_alpha(128)
		s.fill(GREEN)
		for a in player1.getHitBoxes():
			screen.blit(s,a,a)
		for a in player2.getHitBoxes():
			screen.blit(s,a,a)
	if(showHurtBox):
		s = pygame.Surface((600,400))
		s.set_alpha(128)
		s.fill(RED)
		for a in player1.getHurtBoxes():
			screen.blit(s,a,a)
		for a in player2.getHurtBoxes():
			screen.blit(s,a,a)
	drawHUD()
	pygame.display.flip()