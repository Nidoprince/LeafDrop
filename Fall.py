from Leaf import LeafState
import pygame
from fightGlobals import *

class FallState(LeafState):
	def __init__(self,left):
		LeafState.__init__(self,left)
	
	def loadImages(self):
		#Sets all the single frame animation variables for sprites and hitboxes
		self.crouchImage = pygame.image.load("Fall/FallCrouch.bmp").convert()
		self.crouchImage.set_colorkey(PURPLE)
		self.crouchBoxes = self.readBoxFile("Fall/FallCrouch.txt")
		self.crouchHitImage = pygame.image.load("Fall/FallCrouchHit.bmp").convert()
		self.crouchHitImage.set_colorkey(PURPLE)
		self.crouchHitBoxes = self.readBoxFile("Fall/FallCrouchHit.txt")
		self.blockHiImage = pygame.image.load("Fall/FallBlock.bmp").convert()
		self.blockHiImage.set_colorkey(PURPLE)
		self.blockHiBoxes = self.readBoxFile("Fall/FallBlock.txt")
		self.blockLowImage = pygame.image.load("Fall/FallCrouchBlock.bmp").convert()
		self.blockLowImage.set_colorkey(PURPLE)
		self.blockLowBoxes = self.readBoxFile("Fall/FallCrouchBlock.txt")
		
		
		#And here is all the multiframe animation data setting
		for i in range(0,2):
			self.hitImage[i] = pygame.image.load("Fall/FallHit/FallHitFrm"+str(i+1)+".bmp").convert()
			self.hitImage[i].set_colorkey(PURPLE)
			self.hitBox[i] = self.readBoxFile("Fall/FallHit/FallHitFrm"+str(i+1)+".txt")
		for i in range(0,5):
			self.attack1Image[i] = pygame.image.load("Fall/FallAttack1/FallAtk1Frm"+str(i+1)+".bmp").convert()
			self.attack1Image[i].set_colorkey(PURPLE)
			self.attack1Boxes[i] = self.readBoxFile("Fall/FallAttack1/FallAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.attack2Image[i] = pygame.image.load("Fall/FallAttack2/FallAtk2Frm"+str(i+1)+".bmp").convert()
			self.attack2Image[i].set_colorkey(PURPLE)
			self.attack2Boxes[i] = self.readBoxFile("Fall/FallAttack2/FallAtk2Frm"+str(i+1)+".txt")
		for i in range(0,5):
			self.cAttack1Image[i] = pygame.image.load("Fall/FallCrouchAttack1/FallCrchAtk1Frm"+str(i+1)+".bmp").convert()
			self.cAttack1Image[i].set_colorkey(PURPLE)
			self.cAttack1Boxes[i] = self.readBoxFile("Fall/FallCrouchAttack1/FallCrchAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.cAttack2Image[i] = pygame.image.load("Fall/FallCrouchAttack2/FallCrchAtk2Frm"+str(i+1)+".bmp").convert()
			self.cAttack2Image[i].set_colorkey(PURPLE)
			self.cAttack2Boxes[i] = self.readBoxFile("Fall/FallCrouchAttack2/FallCrchAtk2Frm"+str(i+1)+".txt")
		for i in range(0,4):
			self.stepImage[i] = pygame.image.load("Fall/FallStep/FallStpFrm"+str(i+1)+".bmp").convert()
			self.stepImage[i].set_colorkey(PURPLE)
			self.stepBoxes[i] = self.readBoxFile("Fall/FallStep/FallStpFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.breathImage[i] = pygame.image.load("Fall/FallBreath/FallBrthFrm"+str(i+1)+".bmp").convert()
			self.breathImage[i].set_colorkey(PURPLE)
			self.breathBoxes[i] = self.readBoxFile("Fall/FallBreath/FallBrthFrm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jumpImage[i] = pygame.image.load("Fall/FallJump/FallJmpFrm"+str(i+1)+".bmp").convert()
			self.jumpImage[i].set_colorkey(PURPLE)
			self.jumpBoxes[i] = self.readBoxFile("Fall/FallJump/FallJmpFrm"+str(i+1)+".txt")
		for i in range(0,4):
			self.jAttack1Image[i] = pygame.image.load("Fall/FallJumpAttack1/FallJmpAtk1Frm"+str(i+1)+".bmp").convert()
			self.jAttack1Image[i].set_colorkey(PURPLE)
			self.jAttack1Boxes[i] = self.readBoxFile("Fall/FallJumpAttack1/FallJmpAtk1Frm"+str(i+1)+".txt")
		for i in range(0,2):
			self.jAttack2Image[i] = pygame.image.load("Fall/FallJumpAttack2/FallJmpAtk2Frm"+str(i+1)+".bmp").convert()
			self.jAttack2Image[i].set_colorkey(PURPLE)
			self.jAttack2Boxes[i] = self.readBoxFile("Fall/FallJumpAttack2/FallJmpAtk2Frm"+str(i+1)+".txt")
		for i in range(0,3):
			self.sAttack1Image[i] = pygame.image.load("Fall/FallSpecial1/FallHtkFrm"+str(i+1)+".bmp").convert()
			self.sAttack1Image[i].set_colorkey(PURPLE)
			self.sAttack1Boxes[i] = self.readBoxFile("Fall/FallSpecial1/FallHtkFrm"+str(i+1)+".txt")
		for i in range(0,3):
			self.tankenImage[i] = pygame.image.load("Fall/HaNoTanken/HntknFrm"+str(i+1)+".bmp").convert()
			self.tankenImage[i].set_colorkey(PURPLE)
		for i in range(0,4):
			self.victory1Image[i] = pygame.image.load("Fall/FallVictory1/FallVctFrm"+str(i+1)+".bmp").convert()
			self.victory1Image[i].set_colorkey(PURPLE)
		for i in range(0,20):
			self.defeat1Image[i] = pygame.image.load("Fall/FallDefeat1/FallDefeatFrm"+str(i+1)+".bmp").convert()
			self.defeat1Image[i].set_colorkey(PURPLE)
		
		self.idleImage = self.breathImage[0] 
		self.idleBoxes = self.breathBoxes[0]	
		for x in range(3): self.ammo.append(self.tankenImage[0])
