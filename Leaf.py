from fightClasses import FightState
import pygame
from fightGlobals import *

#The subClass of the FightState specifically for the character Leaf.  This controls his animations, his frames,
#how he reacts to user input, everything.
class LeafState(FightState):
	#Sets all the variables.  Probably pretty bloated.  
	def __init__(self,left):
		FightState.__init__(self,"Leaf/LeafBreath/LeafBrthFrm1",RED,left)
		
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
		self.ammoFired = None #Determines type of ammo used
		
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
		self.victory1Image = [0,0,0,0]
		self.defeat1Image = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
		
		self.loadImages()
	
	#Loads the image files in
	def loadImages(self):
		#Sets all the single frame animation variables for sprites and hitboxes
		self.idleImage = self.currentImage.copy() 
		self.idleBoxes = self.getBoxes()
		self.crouchImage = pygame.image.load("Leaf/LeafCrouch.bmp").convert()
		self.crouchImage.set_colorkey(RED)
		self.crouchBoxes = self.readBoxFile("Leaf/LeafCrouch.txt")
		self.crouchHitImage = pygame.image.load("Leaf/LeafCrouchHit.bmp").convert()
		self.crouchHitImage.set_colorkey(RED)
		self.crouchHitBoxes = self.readBoxFile("Leaf/LeafCrouchHit.txt")
		self.blockHiImage = pygame.image.load("Leaf/LeafBlock.bmp").convert()
		self.blockHiImage.set_colorkey(RED)
		self.blockHiBoxes = self.readBoxFile("Leaf/LeafBlock.txt")
		self.blockLowImage = pygame.image.load("Leaf/LeafCrouchBlock.bmp").convert()
		self.blockLowImage.set_colorkey(RED)
		self.blockLowBoxes = self.readBoxFile("Leaf/LeafCrouchBlock.txt")
		self.ammoImage = pygame.image.load("Leaf/LeafAmmo.bmp").convert()
		self.ammoImage.set_colorkey(RED)
		for x in range(3): self.ammo.append(self.ammoImage)
		self.faceImage = pygame.image.load("Leaf/LeafFace.bmp")
		self.faceImage.set_colorkey(RED)
		self.faceHitImage = pygame.image.load("Leaf/LeafFaceHit.bmp")
		self.faceHitImage.set_colorkey(RED)
		self.faceBlockImage = pygame.image.load("Leaf/LeafFaceBlock.bmp")
		self.faceBlockImage.set_colorkey(RED)
		
		#And here is all the multiframe animation data setting
		for i in range(0,2):
			self.hitImage[i] = pygame.image.load("Leaf/LeafHit/LeafHitFrm"+str(i+1)+".bmp").convert()
			self.hitImage[i].set_colorkey(RED)
			self.hitBox[i] = self.readBoxFile("Leaf/LeafHit/LeafHitFrm"+str(i+1)+".txt")
		for i in range(0,5):
			self.attack1Image[i] = pygame.image.load("Leaf/LeafAttack1/LeafAtk1Frm"+str(i+1)+".bmp").convert()
			self.attack1Image[i].set_colorkey(RED)
			self.attack1Boxes[i] = self.readBoxFile("Leaf/LeafAttack1/LeafAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.attack2Image[i] = pygame.image.load("Leaf/LeafAttack2/LeafAtk2Frm"+str(i+1)+".bmp").convert()
			self.attack2Image[i].set_colorkey(RED)
			self.attack2Boxes[i] = self.readBoxFile("Leaf/LeafAttack2/LeafAtk2Frm"+str(i+1)+".txt")
		for i in range(0,5):
			self.cAttack1Image[i] = pygame.image.load("Leaf/LeafCrouchAttack1/LeafCrchAtk1Frm"+str(i+1)+".bmp").convert()
			self.cAttack1Image[i].set_colorkey(RED)
			self.cAttack1Boxes[i] = self.readBoxFile("Leaf/LeafCrouchAttack1/LeafCrchAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.cAttack2Image[i] = pygame.image.load("Leaf/LeafCrouchAttack2/LeafCrchAtk2Frm"+str(i+1)+".bmp").convert()
			self.cAttack2Image[i].set_colorkey(RED)
			self.cAttack2Boxes[i] = self.readBoxFile("Leaf/LeafCrouchAttack2/LeafCrchAtk2Frm"+str(i+1)+".txt")
		for i in range(0,4):
			self.stepImage[i] = pygame.image.load("Leaf/LeafStep/LeafStpFrm"+str(i+1)+".bmp").convert()
			self.stepImage[i].set_colorkey(RED)
			self.stepBoxes[i] = self.readBoxFile("Leaf/LeafStep/LeafStpFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.breathImage[i] = pygame.image.load("Leaf/LeafBreath/LeafBrthFrm"+str(i+1)+".bmp").convert()
			self.breathImage[i].set_colorkey(RED)
			self.breathBoxes[i] = self.readBoxFile("Leaf/LeafBreath/LeafBrthFrm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jumpImage[i] = pygame.image.load("Leaf/LeafJump/LeafJmpFrm"+str(i+1)+".bmp").convert()
			self.jumpImage[i].set_colorkey(RED)
			self.jumpBoxes[i] = self.readBoxFile("Leaf/LeafJump/LeafJmpFrm"+str(i+1)+".txt")
		for i in range(0,4):
			self.jAttack1Image[i] = pygame.image.load("Leaf/LeafJumpAttack1/LeafJmpAtk1Frm"+str(i+1)+".bmp").convert()
			self.jAttack1Image[i].set_colorkey(RED)
			self.jAttack1Boxes[i] = self.readBoxFile("Leaf/LeafJumpAttack1/LeafJmpAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jAttack2Image[i] = pygame.image.load("Leaf/LeafJumpAttack2/LeafJmpAtk2Frm"+str(i+1)+".bmp").convert()
			self.jAttack2Image[i].set_colorkey(RED)
			self.jAttack2Boxes[i] = self.readBoxFile("Leaf/LeafJumpAttack2/LeafJmpAtk2Frm"+str(i+1)+".txt")
		for i in range(0,3):
			self.sAttack1Image[i] = pygame.image.load("Leaf/LeafSpecial1/LeafHtkFrm"+str(i+1)+".bmp").convert()
			self.sAttack1Image[i].set_colorkey(RED)
			self.sAttack1Boxes[i] = self.readBoxFile("Leaf/LeafSpecial1/LeafHtkFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.tankenImage[i] = pygame.image.load("Leaf/HaNoTanken/HntknFrm"+str(i+1)+".bmp").convert()
			self.tankenImage[i].set_colorkey(RED)
		for i in range(0,4):
			self.victory1Image[i] = pygame.image.load("Leaf/LeafVictory1/LeafVctFrm"+str(i+1)+".bmp").convert()
			self.victory1Image[i].set_colorkey(RED)
		for i in range(0,20):
			self.defeat1Image[i] = pygame.image.load("Leaf/LeafDefeat1/LeafDefeatFrm"+str(i+1)+".bmp").convert()
			self.defeat1Image[i].set_colorkey(RED)
		
		
	#The super bloated mega method. This runs each frame to update everything and its brother, depending on state, and keyboard input.
	def next(self, keypress):
	
		self.moveRemember(keypress)
		self.isBlocking = False
		self.passiveHeal()
		#Deals with keyboard input that cares about being held down as opposed to just pressed.  
		#Also deals with adjustment nessessary if step animations interupted, because it normally only
		#adjusts the location after each full step cycle.  
		self.adjust = (0,0)
		self.move = (0,0)
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
		
		
		if(self.state == "defeat"): #Animation when losing
			self.frame += 0.3
			if(self.frame > 30):
				self.currentImage = self.defeat1Image[19]
			elif(self.frame > 18):
				self.currentImage = self.defeat1Image[18]
			else:
				self.currentImage = self.defeat1Image[int(self.frame) - 1]
		elif(self.state == "victory"): #Animation when winning
			self.frame += 1
			if(self.frame >10):
				self.currentImage = self.victory1Image[3]
			elif(self.frame >6):
				self.currentImage = self.victory1Image[2]
			elif(self.frame > 3):
				self.currentImage = self.victory1Image[1]
			elif(self.frame > 1):
				self.currentImage = self.victory1Image[0]
			else:
				self.currentImage = self.victory1Image[0]
				self.move = (0,-20)
		elif(self.state == "hit"): #Animation when struck
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
				if(self.victorious):
					self.state = "victory"
			elif(self.frame == 6):
				self.currentImage = self.sAttack1Image[2]
				self.setBoxes(self.sAttack1Boxes[2])
				self.setProjectile(self.tankenImage,30,35,(-7,0),20,15,self.ammoFired)
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
				if(self.victorious):
					self.state = "victory"
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
				if(self.victorious):
					self.state = "victory"
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
				if(self.victorious):
					self.state = "victory"
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
				if(self.victorious):
					self.state = "victory"
			elif(self.frame == 4):
				self.isHurting = False
			elif(self.frame == 2):
				self.currentImage = self.cAttack2Image[1]
				self.setBoxes(self.cAttack2Boxes[1])
		elif(self.getMetaState() == "jump"): #Jumps to special jumping function.  Haha
			self.nextJump(keypress)
		elif(self.state in ["idle", "crouch", "leftForw", "leftBack", "rightForw", "rightBack"]): #Logic for passive states that you can initiate attacks from.
			if("punchD" in keypress): #Starts basic sword swing.
				if(self.specialCheckStart()): #Tests for special attacks
					True
				elif(self.state == "crouch"): #When crouched
					self.state = "cPunch1"
					self.currentImage = self.cAttack1Image[0]
					self.setBoxes(self.cAttack1Boxes[0])
					self.attackDamage = 25
				else: #When standing
					self.state = "punch1"
					self.currentImage = self.attack1Image[0]
					self.setBoxes(self.attack1Boxes[0])
					self.attackDamage = 30
				self.frame = 0
				self.attack()
			elif("upD" in keypress): #Starts jumping
				self.state = "jumping"
				self.frame = 0
				self.jumpV = 16.5 #This tells us how fast we are jumping upward.  Currently very specific number needed or you won't land on the ground, but will instead fly.
			elif("kickD" in keypress): 
				if(self.state == "crouch"): #Start kicking while crouched
					self.state = "cKick1"
					self.currentImage = self.cAttack2Image[0]
					self.setBoxes(self.cAttack2Boxes[0])
					self.attackDamage = 15
				else: #Start kicking while standing
					self.state = "kick1"
					self.currentImage = self.attack2Image[0]
					self.setBoxes(self.attack2Boxes[0])
					self.attackDamage = 20
				self.frame = 0
				self.attack()
			elif(self.holdingD): #Start or continue crouching
				self.state = "crouch"
				self.currentImage = self.crouchImage
				self.setBoxes(self.crouchBoxes)
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
			if(len(self.ammo)>0):
				self.state = "sAttack1"
				self.currentImage = self.sAttack1Image[0]
				self.currentBoxes = self.sAttack1Boxes[0]
				self.ammoFired = self.ammo[0]
				self.ammo = self.ammo[1:]
			else:
				combo = False
		
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
		self.isHurting = False
		self.healTimer = 30
		self.health = self.health - damage
		if(self.health<0):
			self.health = 0
		if(len(self.ammo)<2):
			self.ammo.append(self.ammoImage)
		
	#Sets appropriate state and conditions when struck by enemy.
	def setBlock(self, punchTime, damage, ammoGrabbed = None):
		if(self.getMetaState() == "land"):
			self.state = "blocking"
			self.frame = 0
		elif(self.getMetaState() == "crouch"):
			self.state = "crouchBlocking"
			self.frame = 0
		self.punchTimer = punchTime
		self.isHurting = False
		if(ammoGrabbed and len(self.ammo)<5):
			self.ammo.append(ammoGrabbed)
		
	#Tells if jumping, standing, or crouching
	def getMetaState(self):
		if(self.state in ["crouch","cPunch1","cKick1","crouchHit","crouchBlocking"]):
			return "crouch"
		elif(self.state in ["jumping","jumpHit","jKick1","jPunch1","jumpDefeat"]):
			return "jump"
		else:
			return "land"
	
	#Checks if currently attacking
	def isAttacking(self):
		return self.state in ["punch1","kick1","jPunch1","jKick1","cPunch1","cKick1","sAttack1"]
	
	def setDefeat(self):
		if(self.getMetaState() == "jump"):
			self.state = "jumpDefeat"
			self.frame2 = 0
		else:
			self.state = "defeat"
			self.frame = 0
		
	def setVictory(self):
		self.victorious = True
		if(not self.isAttacking()):
			self.state = "victory"
			self.frame = 0
		
	
	#Deals with animations when in the process of jumping
	def nextJump(self, keypress):
		self.frame += 1
		if(self.frame >= 28): #Deals with landing
			if(self.state=="jumpHit"):
				self.state = "hit"
				self.frame = self.frame2
			elif(self.state=="jumpDefeat"):
				self.state = "defeat"
				self.frame = self.frame2
			elif(self.victorious):
				self.state = "victory"
				self.frame = 0
			else:
				self.state = "idle"
				self.frame = 0
		elif(self.frame<5 or self.frame>=26): #Deals with first starting or ending a jump
			if(self.state=="jumpHit"):
				self.state = "hit"
				self.frame = self.frame2
			elif(self.state=="jumpDefeat"):
				self.state = "defeat"
				self.frame = self.frame2
			else:
				self.currentImage = self.jumpImage[0]
				self.setBoxes(self.jumpBoxes[0])
				self.state = "jumping"
			self.frame2 = 0
			self.orth = 0
		else: #Deals with the actual "in the air" part of jumping
			if(self.state == "jumpDefeat"):
				self.frame2 += 0.3
				if(self.frame2 > 30):
					self.currentImage = self.defeat1Image[19]
				elif(self.frame2 > 18):
					self.currentImage = self.defeat1Image[18]
				else:
					self.currentImage = self.defeat1Image[int(self.frame2) - 1]
			elif(self.state == "jumpHit"):
				self.frame2 += 1
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
				self.attackDamage = 20
			elif("kickD" in keypress and self.state == "jumping"): #Start kicking
				self.state = "jKick1"
				self.frame2 = 0
				self.attack()
				self.attackDamage = 25
			elif(self.state in ["jumpHit", "jumpDefeat"]): #Can't move while struck
				self.orth = 0
			elif(self.holdingR and not self.holdingL): #Go Right young Meowth
				self.orth = 3.5
			elif(self.holdingL and not self.holdingR): #Go Left young Meowth
				self.orth = -3.5
			else: #Don't move
				self.orth = 0
			self.move = (self.orth,-self.jumpV)