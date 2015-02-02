from __future__ import division
import os
import sys
import pygame
from pygame.locals import *

# Various setup stuff, as before.
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

# Important functions!
def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
	
def briefImage(SCREEN, image):
	SCREEN.fill(bgcol)
	SCREEN.blit(image, (0,0))
	pygame.display.flip()
	pygame.time.wait(timeImage)
	SCREEN.fill(bgcol)
	pygame.display.flip()
	pygame.time.wait(timeBlank)

# here we have abstracted the 5 lines that write text to one function.
def showText(SCREEN, text, pos=(10,10)):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

# note that the last term to the showText() function is x and y position to which we write the text.	
showText(SCREEN, 'Welcome to our experiment!', (1, 200))
waitForKey()
showText(SCREEN, 'Press the space bar when you see the change', (1, 200))
waitForKey()

# here we will actually record the time.
# first record the initial clock time.
startTime = pygame.time.get_ticks()
keypressed = False
while(not keypressed):
	briefImage(SCREEN,image1)
	briefImage(SCREEN,image2)
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_SPACE):
			keypressed = True
			# here we record the response time as the difference between the clock at keypress, and the start clock
			responseTime = pygame.time.get_ticks() - startTime

# print the response time, and write it out to a file.
print('response time: ' + str(responseTime))
FILE.write('%d\n' % responseTime)

showText(SCREEN, 'Thank you for your participation!', (25, 200))
waitForKey()
FILE.close()
sys.exit(0)
