from __future__ import division
import os
import sys
import pygame
from pygame.locals import *

# from main.v00
subject = raw_input('Enter subject ID here: ')
filename = subject + '.csv'
filepath = os.path.join('data', filename)
FILE = open(filepath, 'w')
FILE.write('Subject: %s\n' % subject)

# from main.v01
pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((800,600), 32) #, pygame.FULLSCREEN
FONT = pygame.font.Font(None, 28)
SCREEN.fill((86, 130, 160))
textimg = FONT.render('Hello World', 1, (0,0,0))
SCREEN.blit(textimg, (10, 10))
pygame.display.flip()
wait = True
while wait:
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_SPACE):
			wait = False

# new stuff
# load two images from jpg files in ./img/
image1 = pygame.image.load(os.path.join('img', 'A.jpg'))
image2 = pygame.image.load(os.path.join('img', 'B.jpg'))

# draw a blank screen, put image1 on it, update.
SCREEN.fill((86, 130, 160))
SCREEN.blit(image1, (50,50))
pygame.display.flip()

# wait for 300 msec
pygame.time.wait(300)

# draw a blank screen
SCREEN.fill((86, 130, 160))
pygame.display.flip()

# wait 200 msec
pygame.time.wait(200)

# draw screen containing image2
SCREEN.fill((86, 130, 160))
SCREEN.blit(image2, (50,50))
pygame.display.flip()

# wait 300 msec
pygame.time.wait(300)

# draw blank screen
SCREEN.fill((86, 130, 160))
pygame.display.flip()

print('thank you for your participation!')
FILE.close()
sys.exit(0)
