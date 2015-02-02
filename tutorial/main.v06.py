from __future__ import division
import os
import sys
import pygame
from pygame.locals import *

# Various setup stuff
bgcol = (128, 128, 128)
timeImage = 300
timeBlank = 200
subject = raw_input('Enter subject ID here: ')
FILE = open(os.path.join('data', subject + '.csv'), 'w')
FILE.write('Subject: %s\n' % subject)
pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,400), 32)
FONT = pygame.font.Font(None, 28)

def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
	
def showText(SCREEN, text, pos=(10,10)):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

# that whole display loop is now abstracted as a single function.
def runTrial(SCREEN, imfile1, imfile2):
	image1 = pygame.image.load(os.path.join('img', imfile1))
	image2 = pygame.image.load(os.path.join('img', imfile2))
	keypressed = False
	phase = 0
	startTime = pygame.time.get_ticks()
	while(not keypressed):
		runtime = pygame.time.get_ticks() - startTime
		modtime = runtime % (timeImage*2 + timeBlank*2)
		if(phase == 0 and modtime>0 and modtime<timeImage):
			SCREEN.fill(bgcol)
			SCREEN.blit(image1, (0,0))
			pygame.display.flip()
			phase = 1
		elif(phase == 1 and modtime>timeImage and modtime<(timeImage+timeBlank)):
			SCREEN.fill(bgcol)
			pygame.display.flip()
			phase = 2
		elif(phase == 2 and modtime>(timeImage+timeBlank) and modtime<(timeImage*2+timeBlank)):
			SCREEN.fill(bgcol)
			SCREEN.blit(image2, (0,0))
			pygame.display.flip()
			phase = 3
		elif(phase == 3 and modtime>(timeImage*2+timeBlank)):
			SCREEN.fill(bgcol)
			pygame.display.flip()
			phase = 0
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				keypressed = True
	return(runtime) # returning the runtime is equivalent to returning the response time.

showText(SCREEN, 'Welcome to our experiment!', (1, 200))
waitForKey()
showText(SCREEN, 'Press the space bar when you see the change', (1, 200))
waitForKey()

responseTime = runTrial(SCREEN, 'A.jpg', 'B.jpg')
FILE.write('%d\n' % responseTime)

showText(SCREEN, 'Thank you for your participation!', (25, 200))
waitForKey()

FILE.close()
sys.exit(0)
