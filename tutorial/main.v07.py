# we now move to more of an experiment.  we will try to record the response time and accuracy
# for different image comparisons.
from __future__ import division
import os
import sys
import random
import pygame
from pygame.locals import *

# Various setup stuff
bgcol = (128, 128, 128)
timeImage = 300
timeBlank = 200
subject = raw_input('Enter subject ID here: ')
FILE = open(os.path.join('data', subject + '.txt'), 'w')
FILE.write('Subject: %s\n' % subject)
pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,400), 32)
FONT = pygame.font.Font(None, 28)

# now we will have four different images.
images = ['im000.jpg', 'im001.jpg', 'im002.jpg', 'im003.jpg']
# four images give us 6 unique pairs.
pairs = [[images[1], images[2]], 
		 [images[1], images[3]], 
		 [images[1], images[4]], 
		 [images[2], images[3]], 
		 [images[2], images[4]], 
		 [images[3], images[4]]]

# let's make a quit() function, so we can quit whenever we want.
def quit():
	FILE.close()
	sys.exit(0)

# now, let's also give us an option to quit.  if we press space while waiting, we will continue
# if we press escape while waiting, we will quit.
def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()

# same as before.
def showText(SCREEN, text, pos=(10,10)):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

def runTrial(SCREEN, imfile1, imfile2):
	image1 = pygame.image.load(os.path.join('imgA', imfile))
	image2 = pygame.image.load(os.path.join('imgB', imfile))
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
			# now, let's allow a number of responses:
			# up arrow: indicating that images are different
			# down arrow; indicating that images are the same
			# escape: quit.
			if (event.type == KEYDOWN and event.key == K_UP):
				keypressed = True
				response = 1
			if (event.type == KEYDOWN and event.key == K_UP):
				keypressed = True
				response = 0
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	return([runtime, response]) # now we return both the response time, and the response.


showText(SCREEN, 'Welcome to our experiment!', (1, 200))
waitForKey()
showText(SCREEN, 'Press up to indicate images are different, down to indicate that they are the same', (1, 200))
waitForKey()

random.shuffle(images)

for imfile in images:
	showText(SCREEN, 'Press space for the next trial!', (30, 200))
	waitForKey()
	responseTime = runTrial(SCREEN, imfile)
	FILE.write('%s\t%d\n' % (imfile, responseTime))

showText(SCREEN, 'Thank you for your participation!', (25, 200))
waitForKey()

quit()
