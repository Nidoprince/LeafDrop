import pygame
from fightGlobals import *

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
	def __init__(self, images, x, y, velocity, damage, stunTime, ammoType = None):
		Projectile.__init__(self, images, x, y, velocity)
		self.damage = damage
		self.stunTime = stunTime
		self.foe = None
		self.ammoType = ammoType
		
	def setFoe(self, foe):
		self.foe = foe
		
	def checkHit(self):
		enemy = self.foe.getHitBoxes()
		if(self.rect.collidelist(enemy)!=-1):
			if((self.foe.state.facingLeft and self.rect.center > self.foe.rect.center) or (not self.foe.state.facingLeft and self.rect.center < self.foe.rect.center)):
				self.foe.state.facingLeft = not self.foe.state.facingLeft
				self.foe.state.setHit(self.stunTime, self.damage)
			elif(self.foe.state.isBlocking):
				self.foe.state.setBlock(int(self.stunTime/2), 0, self.ammoType)
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
		self.gameOver = False
		self.foe = None
		
	#Sets who the opponent is so they can call each others methods and look at each others hit boxes	
	def setFoe(self, foe):
		self.foe = foe
		
	#Adds a new projecile to the list
	def addProjectile(self, images, x, y, velocity, damage, stun, ammoType):
		proj = DamagingProjectile(images, x+self.rect[0], y+self.rect[1], velocity, damage, stun, ammoType)
		proj.setFoe(self.foe)
		self.projectiles.add(proj)
	
	#Checks to see if their is a projectile to snag
	def checkProjectile(self):
		if(self.state.projectile):
			proj = self.state.projectile
			self.addProjectile(proj[0],proj[1],proj[2],proj[3],proj[4],proj[5],proj[6])
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
		self.defeatCheck()
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
	
	def defeatCheck(self):
		if(self.state.health == 0 and not self.gameOver):
			self.state.setDefeat()
			self.foe.state.setVictory()
			self.gameOver = True
	
	
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
					if(self.state.facingLeft  == self.foe.state.facingLeft):
						self.foe.state.setHit(20,self.state.attackDamage)
						self.state.attackLag = 0
						self.foe.state.facingLeft = not self.foe.state.facingLeft
					elif(self.foe.state.isBlocking and ((self.state.getMetaState()!="jump" and self.foe.state.getMetaState()=="crouch") or (self.state.getMetaState()!="crouch" and self.foe.state.getMetaState()=="land"))):
						self.foe.state.setBlock(10,0)
						self.state.attackLag = 15
					else:
						self.foe.state.setHit(20,self.state.attackDamage)
						self.state.attackLag = 0
					break
	
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
		self.healthRed = 150 #Health that can be restored to, and is only temporarily gone.
		self.healTimer = 0 #How long before you can start healing again.  
		self.attackDamage = 0 #How much damage the current attack will deal.
		self.ammo = []
		self.victorious = False
		
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
		
	def setProjectile(self, images, x, y, vel, damage, stun, ammoType = None):
		if(not self.facingLeft):
			r = images[0].get_rect()
			x = 100-x-r.width
			vel = (-vel[0],vel[1])
		self.projectile = [images, x, y, vel, damage, stun, ammoType]
	
	def setDefeat(self):
		self.state = "defeat"
		
	def setVictory(self):
		self.state = "victory"
		
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
		self.healTimer = 30
	
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
		
	#Starts to heal if not damaged for a second
	def passiveHeal(self):
		if(self.healTimer > 0):
			self.healTimer -= 1
		elif(self.healthRed > self.health):
			if(self.health > 0):
				self.health += 1
			self.healthRed -= 2
		elif(self.healthRed < self.health):
			self.healthRed = self.health