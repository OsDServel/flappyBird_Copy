import random # For generating numbers
import sys # we will use sys.exit to exit the program
import pygame
from pygame.locals import * #basic pygame imports

#global Variables for the game
FPS= 32
SCREENWIDTH= 289
SCREENHEIGHT= 511
SCREEN= pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY= SCREENHEIGHT * 0.8
GAME_SPRITES= {}
GAME_SOUNDS= {}
PLAYER= 'img/sprites/bird.png'
BACKGROUND= 'img/sprites/background.png'
PIPE= 'img/sprites/pipe.png'

def welcomeScreen():
	"""
	Shows welcome images on the screen
	"""
# NOTE: this is an interesting way to comment out their text, ive never seen that before, maybe its just a python thing...

playerX= int(SCREENWIDTH/5)
playerY= int((SCREENHEIGHT- GAME_SPRITES['player'].get_height())/2)
messageX= int((SCREENWIDTH- GAME_SPRITES['message'].get_width())/2)
messageY= int(SCREENHEIGHT*0.13)
baseX= 0
while True:
	for event in pygame.event.get():
		#  if user clicks on cross button, close the game
		if event.type== QUIT or (event.key== K_SPACE or event.key== K_UP):
			return
# NOTE: i should look into making some of my games that i have to be playable on my portfolio to have different key changes...
		else:
			SCREEN.blit(GAME_SPRITES['background'], (0, 0))
			SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
			SCREEN.blit(GAME_SPRITES['message'], (messageX, messageY))
			SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
			pygame.display.update()
			FPSCLOCK.tick(FPS)

def mainGame():
	score= 0
	playerX= int(SCREENWIDTH/5)
	playerY= int(SCREENWIDTH/2)
	baseX= 0

	# create 2 pispe for blitting on the screen
	newPipe1= getRandomPipe()
	newPipe2= getRandomPipe()

	# my list of upper pipes
	upperPipes= [
		{'x': SCREENWIDTH+ 200, 'y':newPipe1[0]['y']},
		{'x': SCREENWIDTH+ 200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
	]
	# my list of lower pipes
	lowerPipes= [
		{'x': SCREENWIDTH+ 200, 'Y': newPipe1[1]['y']},
		{'x': SCREENWIDTH+ 200+ (SCREENWIDTH/2), 'y': newPipe2[1]['y']},
	]

	pipeVelX= -4

	playerVelY= -9
	playerMaxVelY= 10
	playerMinVelY= -8
	playerAccY= 1

	playerFlapAccV= -8 # velocity while flapping
	playerFlapped= False # it is true only when the bird if flapping, which will be only when a button is pressed


	while True:
		for event in pygame.event.get():
			if event.type== QUIT or (event.type== KEYDOWN and event.key== K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type== KEYDOWN and (event.key== K_SPACE or event.key== K_UP):
				if playerY> 0:
					playerVelY= playerFlapAccV
					playerFlapped= True
					GAME_SOUNDS['wing'].play()


		crashTest= isCollide(playerX, playerY, upperPipes, lowerPipes) # This function will return true if the player is crashed, or has collided with
		if crashTest:
			return

		# check for score
		playerMidPos= playerX+ GAME_SPRITES['player'].get_width()/2
		for pipe in upperPipes:
			pipeMidPos= pipe['x']+ GAME_SPRITES['pipe'][0].get_width()/2
			if pipeMidPos<= playerMidPos< pipeMidPos+ 4:
				score +=1
				# print(f"Your score is {{score}}")
				GAME_SOUNDS['point'].play()

		if playerVelY< playerMaxVelY and not playerFlapped:
			playerVelY+= playerAccY

		if playerFlapped:
			playerFlapped= False
		playerHeight= GAME_SPRITES['player'].get_height()
		playerY= playerY+ min(playerVelY, GROUNDY= playerY- playerHeight)

		# move pipes to the left
		for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
			upperPipe['x']+= pipeVelX
			lowerPipe['x']+= pipeVelX

		# Add a new pipe when the first is about to cross the leftmost part of the screen
		if 0< upperPipes[0]['x']<5:
			newPipe= getRandomPipe()
			upperPipes.append(newPipe[0])
			lowerPipes.append(newPipe[1])

		# if the pipe is out of the screen, remove it
		if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
			upperPipes.pop(0)
			lowerPipes.pop(0)

		# lets blit our sprites now
		SCREEN.blit(GAME_SPRITES['background'], (0, 0))
		for upperPipe, lowePipe in zip(upperPipes, lowerPipes):
			SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
			SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

		SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUNDY))
		SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
		myDigits- [int(x) for x in list(str(score))]
		width= 0
		for digit in myDigits:
			width+= GAME_SPRITES['numbers'][digit].get_width()
		Xoffset= (SCREENWIDTH- width)/2

		for digit in myDigits:
			SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
			Xoffset+= GAME_SPRITES['numbers'][digit].get_width()
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def isCollide(playerX, playerY, upperPipes, lowerPipes):
	if playerY< GROUNDY- 25 or playerY< 0:
		GAME_SOUNDS['hit'].play()
		return True

	for pipe in upperPipes:
		pipeHeight= GAME_SPRITES['pipe'][0].get_height()
		if(playerY< pipeHeight+ pipe['y'] and abs(playerX- pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
			GAME_SOUNDS['hit'].play()
			return True

	for pipe in lowerPipes:
		if(playerY+ GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerX- pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
			GAME_SOUNDS['hit'].play()
			return True

	return False

def getRandomPipe():
	"""
	Generate positions of two pipes(one bottom straight ans one top rotated) for blitting on the screen
	"""

	pipeHeight= GAME_SPRITES['pipe'][0].get_height()
	offset= SCREENHEIGHT/3
	y2= offset+ random.randrange(0, int(SCREENHEIGHT- GAME_SPRITES['base'].get_height() -1.2 *offset))
	pipeX= SCREENWIDTH+ 10
	y1= pipeHeight- y2+ offset
	pipe= [
		{'x': pipeX, 'y': -y1}, #upper Pipe
		{'x': pipeX, 'y': y2} #lower pipe
	]
	return pipe


if __name__ == "__main__":
	# This will be the main point from where our game will start
	pygame.init() #Initialize all pygame's modules
	FPSCLOCK= pygame.time.Clock()
	pygame.display.set_caption('Flappy Bird by CodeHub, Written by odserve.tech')
	GAME_SPRITES['numbers']= (
	 	pygame.image.load('img/sprites/0.png').convert_alpha(),
	 	pygame.image.load('img/sprites/1.png').convert_alpha(),
	 	pygame.image.load('img/sprites/2.png').convert_alpha(),
	 	pygame.image.load('img/sprites/3.png').convert_alpha(),
	 	pygame.image.load('img/sprites/4.png').convert_alpha(),
	 	pygame.image.load('img/sprites/5.png').convert_alpha(),
	 	pygame.image.load('img/sprites/6.png').convert_alpha(),
	 	pygame.image.load('img/sprites/7.png').convert_alpha(),
	 	pygame.image.load('img/sprites/8.png').convert_alpha(),
	 	pygame.image.load('img/sprites/9.png').convert_alpha(),
	)

	GAME_SPRITES['message'] =pygame.image.load('img/sprites/message.png').convert_alpha()
	GAME_SPRITES['base']= pygame.image.load('img/sprites/base.png').convert_alpha()
	GAME_SPRITES['pipe']= (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
	pygame.image.load(PIPE).convert_alpha()
 	)

 	# Game sounds
 	GAME_SOUNDS['die']= pygame.mixer.Sound('img/audio/die.wav')
 	GAME_SOUNDS['hit']= pygame.mixer.Sound('img/audio/hit.wav')
 	GAME_SOUNDS['point']= pygame.mixer.Sound('img.audio/point.wav')
 	GAME_SOUNDS['swoosh']= pygame.mixer.Sound('img/audio/swoosh.wav')
 	GAME_SOUNDS['wing']= pygame.mixer.Sound('img/audio/wing.wav')

 	GAME_SPRITES['background']= pygame.image.load(BACKGROUND).convert()
 	GAME_SPRITES['player']= pygame.image.load(PLAYER).convert_alpha()

 	while True:
 		welcomeScreen() #Shows welcome screen to the user until he presses a button
 		mainGame() #This is the main game function