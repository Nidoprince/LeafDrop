import pygame, sys
from fightClasses import Fighter
from fightGlobals import *
from Leaf import LeafState
from Fall import FallState
			
def drawHUD(player1, player2):
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
	pygame.draw.rect(screen, RED, [50, 5, player1.state.healthRed, 20])
	pygame.draw.rect(screen, RED, [width-50-player2.state.healthRed, 5, player2.state.healthRed, 20])
	pygame.draw.rect(screen, GREEN, [50, 5, player1.state.health, 20])
	pygame.draw.rect(screen, GREEN, [width-50-player2.state.health, 5, player2.state.health, 20])
	pygame.draw.rect(screen, p1Status, [5, 5, 40, 45])
	pygame.draw.rect(screen, p2Status, [width-45, 5, 40, 45])
	pygame.draw.rect(screen, BLACK, [49, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [width-202, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [5, 5, 40, 45], 3)
	pygame.draw.rect(screen, BLACK, [width-45, 5, 40, 45], 3)
	for x in range(len(player1.state.ammo)):
		screen.blit(player1.state.ammo[x],(50+25*x,30))
	for x in range(len(player2.state.ammo)):
		screen.blit(player2.state.ammo[x],(width-66-25*x,30))
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
	
def fightLoop(play1, play2, stageIn):
	stage = stageIn
	player1 = play1
	player2 = play2

	player1.setFoe(player2)
	player2.setFoe(player1)

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
				if event.key == pygame.K_SPACE:
					if(player1.gameOver or player2.gameOver):
						return True
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
		drawHUD(player1, player2)
		if(player1.gameOver or player2.gameOver):
			if(not 'continueText' in locals()):
				continueText = text.render("Game Over.  Press Space to Restart",False,BLACK)
			screen.blit(continueText, (200, 100))
		pygame.display.flip()	

pygame.init()
text = pygame.font.Font(None, 20)

#Initialization stuff
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
forestStage = pygame.image.load("ForestStage.bmp").convert() #Sets background image
while 1:
	leaf = Fighter(LeafState(False),100,170) # Makes fighter1
	clone = Fighter(FallState(True),400,170) # Makes fighter2
	fightLoop(leaf, clone, forestStage)