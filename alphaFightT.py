import pygame, sys
from fightClasses import Fighter
from fightGlobals import *
from Leaf import LeafState
from Fall import FallState
			
def drawHUD(player1, player2):
	p1Status = GREEN
	p1Image = player1.state.faceImage
	p2Status = GREEN
	p2Image = player2.state.faceImage
	if(player1.state.state in ["hit","crouchHit","jumpHit"]):
		p1Status = RED
		p1Image = player1.state.faceHitImage
	if(player1.state.state in ["blocking","crouchBlocking"]):
		p1Status = BLUE
		p1Image = player1.state.faceBlockImage
	if(player2.state.state in ["hit","crouchHit","jumpHit"]):
		p2Status = RED
		p2Image = player2.state.faceHitImage
	if(player2.state.state in ["blocking","crouchBlocking"]):
		p2Status = BLUE
		p2Image = player2.state.faceBlockImage
	pygame.draw.rect(screen, BLUE, [50, 5, 150, 20])
	pygame.draw.rect(screen, BLUE, [width-200, 5, 150, 20])
	pygame.draw.rect(screen, RED, [50, 5, player1.state.healthRed, 20])
	pygame.draw.rect(screen, RED, [width-50-player2.state.healthRed, 5, player2.state.healthRed, 20])
	pygame.draw.rect(screen, GREEN, [50, 5, player1.state.health, 20])
	pygame.draw.rect(screen, GREEN, [width-50-player2.state.health, 5, player2.state.health, 20])
	pygame.draw.rect(screen, p1Status, [5, 5, 40, 45])
	screen.blit(pygame.transform.flip(p1Image, True, False),(5,5))
	pygame.draw.rect(screen, p2Status, [width-45, 5, 40, 45])
	screen.blit(p2Image,(width-45,5))
	pygame.draw.rect(screen, BLACK, [49, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [width-202, 5, 152, 20], 3)
	pygame.draw.rect(screen, BLACK, [5, 5, 40, 45], 3)
	pygame.draw.rect(screen, BLACK, [width-45, 5, 40, 45], 3)
	for x in range(len(player1.state.ammo)):
		screen.blit(player1.state.ammo[x],(50+25*x,30))
	for x in range(len(player2.state.ammo)):
		screen.blit(player2.state.ammo[x],(width-66-25*x,30))
	for x in range(5):
		pygame.draw.rect(screen, BLACK, [50+25*x, 30, 15, 15], 2)
		pygame.draw.rect(screen, BLACK, [width-66-25*x, 30, 15, 15], 2)
	
def fightLoop(play1, play2, stageIn, music):
	stage = stageIn
	player1 = play1
	player2 = play2

	player1.setFoe(player2)
	player2.setFoe(player1)

	#Toggles for animation of various hit boxes
	showCollisionBox = False
	showHitBox = False
	showHurtBox = False
	
	#Starts background music
	pygame.mixer.music.load(music)
	pygame.mixer.music.play(-1)

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

def menuLoop():
	state = "mainMenu"
	mainMenuOptions = 4
	menuOptions = mainMenuOptions
	spacePressed = False
	menuScroll = pygame.image.load("MenuScroll.bmp").convert()
	counter = 0
	menuLocation = 0
	scrollValue = 0
	menuText = pygame.font.Font('couriercode-roman.ttf', 25)
	menuText.set_bold(True)
	menuText.set_italic(True)
	versusText = menuText.render("Versus",False,RED)
	helpText = menuText.render("Help",False,RED)
	creditsText = menuText.render("Credits",False,RED)
	quitText = menuText.render("Quit",False,RED)
	menuTexts = [versusText,helpText,creditsText,quitText]
	
	subMenuText = pygame.font.Font('couriercode-roman.ttf', 20)
	subMenuText.set_bold(True)
	subMenuText.set_italic(True)
	returnText = subMenuText.render("Return",False,PURPLE)
	nextText = subMenuText.render("Next",False,PURPLE)
	backText = subMenuText.render("Back",False,PURPLE)
	helpTexts = [nextText,backText,returnText]
	
	pageText = pygame.font.Font('couriercode-roman.ttf', 15)	
	e = open("help.txt", "r")
	pages = []
	twende = True
	while(twende):
		endelea = True
		page = []
		while(endelea):
			temp = e.readline().strip()
			if(temp == "###"):
				twende = False
				endelea = False
			elif(temp == "##"):
				endelea = False
			else:
				page.append(temp)
		canvas = pygame.Surface((500,20*len(page)))
		canvas.fill(PURPLE)
		for x in range(len(page)):
			canvas.blit(pageText.render(page[x],False,BLACK),(0,20*x))
		pages.append(canvas)
	e.close()
	
	text = pygame.font.Font('couriercode-roman.ttf', 12)
	f = open("credits.txt", "r")
	creditMessage = [f.readline()]
	twende = True
	while(twende):
		temp = f.readline().strip()
		if(temp == "###"):
			twende = False
		else:
			creditMessage.append(temp)
	f.close()
	credits = [text.render(a,False,WHITE) for a in creditMessage]
	textScreen = pygame.Surface((500,15*len(credits)))
	for x in range(len(credits)):
		textScreen.blit(credits[x],(0,15*x))
	
	def menuRun(which):
		nonlocal state,spacePressed,menuOptions,menuLocation,scrollValue
		if(state == "mainMenu"):
			if(which == 0):
				spacePressed = True
			elif(which == 1):
				state = "help"
				menuOptions = 3
				menuLocation = 0
				scrollValue = 0
			elif(which == 2):
				state = "credits"
				menuOptions = 1
				menuLocation = 0
				scrollValue = 0
			elif(which == 3):
				sys.exit()
		elif(state == "help"):
			if(which == 0):
				scrollValue = (scrollValue+1)%len(pages)
			elif(which == 1):
				scrollValue = (scrollValue-1)%len(pages)
			elif(which == 2):
				state = "mainMenu"
				menuOptions = mainMenuOptions
				menuLocation = 1
		elif(state == "credits"):
			if(which == 0):
				state = "mainMenu"
				menuOptions = mainMenuOptions
				menuLocation = 2
		elif(state == "options"):
			if(which == 0):
				state = "mainMenu"
				menuOptions = mainMenuOptions
				menuLocation = 3
				
	while not spacePressed:
		clock.tick(frameRate)
		counter = (counter + 1)%1800
		counter2 = counter%600
		counter3 = counter%900
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN: #Buttons pressed
				if event.key == pygame.K_SPACE:
					spacePressed = True
				if event.key == pygame.K_DOWN:
					menuLocation = (menuLocation + 1)%menuOptions
					menuMove.play()
				if event.key == pygame.K_UP:
					menuLocation = (menuLocation - 1)%menuOptions
					menuMove.play()
				if event.key == pygame.K_COMMA:
					menuRun(menuLocation)
					menuSelect.play()
		screen.blit(menuScroll,(0,0),(counter2,2*counter3//3,600,300))
		screen.blit(menuScroll,(600-counter2,0),(0,2*counter3//3,600,300))
		if(counter>=450):
			screen.blit(menuScroll,(0,600-2*counter3//3),(counter2,0,600,300))
			screen.blit(menuScroll,(600-counter2,600-2*counter3//3),(0,0,600,300))
		if(state == "mainMenu"):
			for x in range(menuOptions):
				if(x == menuLocation):
					pygame.draw.rect(screen,GREEN,(190,70+40*x,200,35))
					screen.blit(menuTexts[x],(240,75+40*x))
				else:
					pygame.draw.rect(screen,GREEN,(200,70+40*x,200,35))
					screen.blit(menuTexts[x],(250,75+40*x))
		elif(state == "help"):
			pygame.draw.rect(screen,BLUE,(50, 30, 500, 240))
			pygame.draw.rect(screen,PURPLE,(60,40,350,220))
			screen.blit(pages[scrollValue],(70,55),(0,0,330,200))
			for x in range(menuOptions):
				if(x == menuLocation):
					pygame.draw.rect(screen,BLACK,(420,145+40*x,110,35))
					screen.blit(helpTexts[x],(435,150+40*x))
				else:
					pygame.draw.rect(screen,BLACK,(430,145+40*x,110,35))	
					screen.blit(helpTexts[x],(445,150+40*x))
		elif(state == "credits"):
			scrollValue = (scrollValue+1)%(15*len(credits))
			pygame.draw.rect(screen,BLACK,(50, 30, 500, 240))
			screen.blit(textScreen, (60, 40), (0,scrollValue,420,220))
			pygame.draw.rect(screen,BLUE,(430,225,110,35))
			screen.blit(returnText,(445,230))
		
		pygame.display.flip()

	return characterSelect()

def characterSelect():
	p1Lock = False
	p2Lock = False
	p1Pos = [0,0]
	p2Pos = [1,0]
	counter = 0
	characterSelectScroll = pygame.image.load("CharacterSelectScroll.bmp").convert()
	leafPic = pygame.image.load("Leaf/LeafFace.bmp").convert()
	leafPic.set_colorkey(RED)
	fallPic = pygame.image.load("Fall/FallFace.bmp").convert()
	fallPic.set_colorkey(PURPLE)
	lockPic = pygame.image.load("LockIcon.bmp").convert()
	lockPic.set_colorkey(BLUE)
	grid = [[[LeafState, leafPic],[False,lockPic],[False,lockPic],[False,lockPic]],[[FallState, fallPic],[False,lockPic],[False,lockPic],[False,lockPic]]]
	while(not p1Lock or not p2Lock):
		clock.tick(frameRate)
		counter = (counter + 1)%1800
		counter2 = counter%600
		counter3 = counter%900
		screen.blit(characterSelectScroll,(0,0),(counter2,2*counter3//3,600,300))
		screen.blit(characterSelectScroll,(600-counter2,0),(0,2*counter3//3,600,300))
		if(counter>=450):
			screen.blit(characterSelectScroll,(0,600-2*counter3//3),(counter2,0,600,300))
			screen.blit(characterSelectScroll,(600-counter2,600-2*counter3//3),(0,0,600,300))
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN: #Buttons pressed
				if(event.key in [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d,pygame.K_DOWN,pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT]):
					menuMove.play()
					if event.key == pygame.K_w:
						test = p1Pos[0]-1
						if(test>=0 and test<len(grid) and grid[test][p1Pos[1]][0] and not p1Lock):
							p1Pos[0] = test
					if event.key == pygame.K_s:
						test = p1Pos[0]+1
						if(test>=0 and test<len(grid) and grid[test][p1Pos[1]][0] and not p1Lock):
							p1Pos[0] = test
					if event.key == pygame.K_d:
						test = p1Pos[1]+1
						if(test>=0 and test<len(grid[0]) and grid[p1Pos[0]][test][0] and not p1Lock):
							p1Pos[1] = test
					if event.key == pygame.K_a:
						test = p1Pos[1]-1
						if(test>=0 and test<len(grid[0]) and grid[p1Pos[0]][test][0] and not p1Lock):
							p1Pos[1] = test
					if event.key == pygame.K_DOWN:
						test = p2Pos[0]+1
						if(test>=0 and test<len(grid) and grid[test][p2Pos[1]][0] and not p2Lock):
							p2Pos[0] = test
					if event.key == pygame.K_UP:
						test = p2Pos[0]-1
						if(test>=0 and test<len(grid) and grid[test][p2Pos[1]][0] and not p2Lock):
							p2Pos[0] = test
					if event.key == pygame.K_LEFT:
						test = p2Pos[1]-1
						if(test>=0 and test<len(grid[0]) and grid[p2Pos[0]][test][0] and not p2Lock):
							p2Pos[1] = test
					if event.key == pygame.K_RIGHT:
						test = p2Pos[1]+1
						if(test>=0 and test<len(grid[0]) and grid[p2Pos[0]][test][0] and not p2Lock):
							p2Pos[1] = test
				if event.key == pygame.K_COMMA:
					p2Lock = not p2Lock
					menuSelect.play()
				if event.key == pygame.K_v:
					p1Lock = not p1Lock
					menuSelect.play()
		for x in range(len(grid)):
			for y in range(len(grid[0])):
				if([x,y]==p1Pos):
					if(p1Lock):
						pygame.draw.rect(screen,BLUE,(138+y*85,68+x*95,62,67))
					else:
						pygame.draw.rect(screen,BLUE,(135+y*85,65+x*95,65,70))
				if([x,y]==p2Pos):
					if(p2Lock):
						pygame.draw.rect(screen,RED,(140+y*85,70+x*95,62,67))
					else:
						pygame.draw.rect(screen,RED,(140+y*85,70+x*95,65,70))
				pygame.draw.rect(screen,BLACK,(140+y*85,70+x*95,60,65))
				pygame.draw.rect(screen,PURPLE,(145+y*85,75+x*95,50,55))
				screen.blit(grid[x][y][1],(150+y*85,80+x*95))
		pygame.display.flip()
		
	character1 = grid[p1Pos[0]][p1Pos[1]][0]
	character2 = grid[p2Pos[0]][p2Pos[1]][0]
	player1 = Fighter(character1(False),100,170) # Makes fighter1
	player2 = Fighter(character2(True),400,170) # Makes fighter2
	return stageSelect(player1,player2)

def stageSelect(player1,player2):
	cursorPos = [0,0]
	notReady = True
	counter = 0
	stageSelectScroll = pygame.image.load("StageSelectScroll.bmp").convert()
	forestPreview = pygame.image.load("ForestStagePreview.bmp").convert()
	unknownPreview = pygame.image.load("UnknownPreview.bmp").convert()
	grid = [[[forestPreview, "ForestStage.bmp", "ForestSong.ogg"],[unknownPreview,False,False],[unknownPreview,False,False]],[[unknownPreview,False,False],[unknownPreview,False,False],[unknownPreview,False,False]]]
	while notReady:
		clock.tick(frameRate)
		counter = (counter + 1)%1800
		counter2 = counter%600
		counter3 = counter%900
		screen.blit(stageSelectScroll,(0,0),(counter2,2*counter3//3,600,300))
		screen.blit(stageSelectScroll,(600-counter2,0),(0,2*counter3//3,600,300))
		if(counter>=450):
			screen.blit(stageSelectScroll,(0,600-2*counter3//3),(counter2,0,600,300))
			screen.blit(stageSelectScroll,(600-counter2,600-2*counter3//3),(0,0,600,300))
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN: #Buttons pressed
				if(event.key in [pygame.K_DOWN,pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT]):
					menuMove.play()
					if event.key == pygame.K_DOWN:
						test = cursorPos[0]+1
						if(test>=0 and test<len(grid) and grid[test][cursorPos[1]][1]):
							cursorPos[0] = test
					if event.key == pygame.K_UP:
						test = cursorPos[0]-1
						if(test>=0 and test<len(grid) and grid[test][cursorPos[1]][1]):
							cursorPos[0] = test
					if event.key == pygame.K_LEFT:
						test = cursorPos[1]-1
						if(test>=0 and test<len(grid[0]) and grid[cursorPos[0]][test][1]):
							cursorPos[1] = test
					if event.key == pygame.K_RIGHT:
						test = cursorPos[1]+1
						if(test>=0 and test<len(grid[0]) and grid[cursorPos[0]][test][1]):
							cursorPos[1] = test
				if event.key == pygame.K_COMMA:
					notReady = False
					menuSelect.play()
		for x in range(len(grid)):
			for y in range(len(grid[0])):
				if([x,y]==cursorPos):
					pygame.draw.rect(screen,BLUE,(45+y*180,65+x*100,160,85))
				screen.blit(grid[x][y][0],(50+y*180,70+x*100))
		pygame.display.flip()
	stage = pygame.image.load(grid[cursorPos[0]][cursorPos[1]][1]).convert() #Sets background image
	backgroundMusic = grid[cursorPos[0]][cursorPos[1]][2]
	return player1, player2, stage, backgroundMusic
	
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
text = pygame.font.Font(None, 20)

#Initialization stuff
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
menuSelect = pygame.mixer.Sound("MenuChoose.ogg")
menuSelect.set_volume(0.4)
menuMove = pygame.mixer.Sound("MenuMove.ogg")
menuMove.set_volume(0.4)

while 1:
	pygame.mixer.music.load("MenuSong.ogg")
	pygame.mixer.music.play(-1)
	pygame.mixer.music.set_volume(0.7)
	leaf, clone, forestStage, backgroundMusic = menuLoop()
	pygame.mixer.music.fadeout(500)
	fightLoop(leaf, clone, forestStage, backgroundMusic)
	pygame.mixer.music.fadeout(500)