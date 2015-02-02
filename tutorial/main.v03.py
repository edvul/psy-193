from __future__ import division
import os
import sys
import pygame
from pygame.locals import *

# now we are going to generalize what we did before a little bit

# save the time used for a display, and the background color, as variables
bgcol = (128, 128, 128)
timeImage = 300
timeBlank = 200

# define a function that waits for someone to press spacebar.
def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False

# define a function that draws an image for timeImage msec, and hten shows a blank screen for timeBlank msec
def briefImage(SCREEN, image):
	SCREEN.fill(bgcol)
	SCREEN.blit(image, (0,0))
	pygame.display.flip()
	pygame.time.wait(timeImage)
	SCREEN.fill(bgcol)
	pygame.display.flip()
	pygame.time.wait(timeBlank)

# a compressed version of the file and input operations we had before	
subject = raw_input('Enter subject ID here: ')
FILE = open(os.path.join('data', subject + '.csv'), 'w')
FILE.write('Subject: %s\n' % subject)

# a compressed version of pygame initialization and image loading we had before.
pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,400), 32)
FONT = pygame.font.Font(None, 28)
image1 = pygame.image.load(os.path.join('img', 'A.jpg'))
image2 = pygame.image.load(os.path.join('img', 'B.jpg'))

# show welcome text, wait for space bar
SCREEN.fill(bgcol)
textimg = FONT.render('Hello World', 1, (0,0,0))
SCREEN.blit(textimg, (10, 10))
pygame.display.flip()

waitForKey()

# now we are going to alternate between the two images until a space bar is pressed.
keypressed = False
while(not keypressed):
	briefImage(SCREEN,image1)
	briefImage(SCREEN,image2)
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_SPACE):
			keypressed = True

# now we write the "thank you" to the graphical window and wait for a space bar
SCREEN.fill(bgcol)
textimg = FONT.render('Thank you for your participation', 1, (0,0,0))
SCREEN.blit(textimg, (10, 10))
pygame.display.flip()
waitForKey()

FILE.close()
sys.exit(0)
