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
image1 = pygame.image.load(os.path.join('img', 'A.jpg'))
image2 = pygame.image.load(os.path.join('img', 'B.jpg'))

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
	
# let's produce somewhat more helpful instructions.
showText(SCREEN, 'Welcome to our experiment!', (1, 200))
waitForKey()
showText(SCREEN, 'Press the space bar when you see the change', (1, 200))
waitForKey()

# in the previous loop, we could only record a response time every 2*(timeImage+timeBlank) msec
# this was because we only checked for an input after a whole display sequence had completed.
# in contrast, we will now rewrite this whole loop to monitor the keypress constantly, and we
# will confer with our timer to decide whether the contents of the display should be updated.

# we haven't yet pressed a key
keypressed = False
# define the start time
startTime = pygame.time.get_ticks()
# we will use this to figure out which phase of the display sequence we are in.
# the whole display sequence is Image1 display, blank, Image 2 display, blank
# this whole sequence will last timeImage + timeBlank + timeImage + timeBlank
# .... or 2*timeImage + 2*timeBlank
sequenceLength = 2*timeImage + 2*timeBlank

# here is how we will define the various 'phases' of the display sequence
# phase 1: image 1 on screen 			[t=0 to t=timeImage]
# phase 2: blank phase after image 1 (before image 2)	[t=timeImage to t=(timeImage+timeBlank)]
# phase 3: image 2 on screen  [t=(timeImage+timeBlank) to t=(timeImage+timeBlank+timeImage)]
# phase 0: blank phase after image 2, before image 1. [t=(timeImage+timeBlank+timeImage) to t=(timeImage+timeBlank+timeImage+timeBlank)]
# 	however, because time is modular (we repeat the cycle) at t=(timeImage+timeBlank+timeImage+timeBlank), t resets to 0.

# we are starting in phase 0
phase = 0

while(not keypressed):
	# define runtime as the time elpased since startTime
	runtime = pygame.time.get_ticks() - startTime
	# modTime is the remainder of runtime and the full cycle length.
	# this will allow us to figure out which 'phase' of the image display cycle we are in.
	modtime = runtime % sequenceLength

	# if we are in phase 0, and the time is right, display image1, and move to phase=1
	if(phase == 0 and modtime>0 and modtime<timeImage):
		SCREEN.fill(bgcol)
		SCREEN.blit(image1, (0,0))
		pygame.display.flip()
		phase = 1
	# if we are in phase=1, and the time is right, display blank, and move to phase=2
	elif(phase == 1 and modtime>timeImage and modtime<(timeImage+timeBlank)):
		SCREEN.fill(bgcol)
		pygame.display.flip()
		phase = 2
	# if we are in phase=2, and the time is right, display image 2 and move to phase=3
	elif(phase == 2 and modtime>(timeImage+timeBlank) and modtime<(timeImage*2+timeBlank)):
		SCREEN.fill(bgcol)
		SCREEN.blit(image2, (0,0))
		pygame.display.flip()
		phase = 3
	# if we are in phase=3, and the time is right, display blank, and move to phase=0
	elif(phase == 3 and modtime>(timeImage*2+timeBlank)):
		SCREEN.fill(bgcol)
		pygame.display.flip()
		phase = 0
	# monitor for space bar press every cycle.
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_SPACE):
			keypressed = True
# once we have left the display loop, it means the key was pressed, and we can record the response time.
responseTime = pygame.time.get_ticks() - startTime


print('response time: ' + str(responseTime))
FILE.write('%d\n' % responseTime)

showText(SCREEN, 'Thank you for your participation!', (25, 200))
waitForKey()
FILE.close()
sys.exit(0)
