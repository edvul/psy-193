from __future__ import division
import os
import sys

# new libraries we are using to create graphical input.
import pygame
from pygame.locals import *

# this is the stuff we did on main.v00.py
subject = raw_input('Enter subject ID here: ')
print('Subject ID is: ', subject)
filename = subject + '.csv'
filepath = os.path.join('data', filename)
FILE = open(filepath, 'w')
FILE.write('Subject: %s\n' % subject)

# new stuff.
# initialize graphical display, sound, and event (input) monitor
pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
# create a window.
SCREEN = pygame.display.set_mode((800,600), 32) #, pygame.FULLSCREEN
# set up font for window.
FONT = pygame.font.Font(None, 28)

# will window with some color (RGB [0 255])
SCREEN.fill((86, 130, 160))
# make a bitmap from text using the "FONT object"
textimg = FONT.render('Hello World', 1, (0,0,0))
# write the text bitmap to our window.
SCREEN.blit(textimg, (10, 10))
# update the display
pygame.display.flip()

# wait for space bar.
wait = True
while wait:
	for event in pygame.event.get():
		if (event.type == KEYDOWN and event.key == K_SPACE):
			wait = False

print('thank you for your participation!')
FILE.close()
sys.exit(0)
