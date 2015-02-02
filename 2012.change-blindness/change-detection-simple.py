from __future__ import division
import os
import sys
import random
import glob
import string
import pygame
from pygame.locals import *
subject = raw_input('Enter subject ID here: ')

pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,420), 16)
FONT = pygame.font.Font(None, 28)

#  few paramters
DEBUG = False
bgcol = (255, 255, 255)
textPos = (1,1)
imgPos = (0,20)
timeImage = 300
timeBlank = 200
FILE = open(os.path.join('data', subject + '.txt'), 'w')
imDirA = 'imgA'
imDirB = 'imgB'
textSpace = FONT.render('Click on the location of the change!', 1, (0,0,96))

images = glob.glob(os.path.join(imDirA, '*.jpg'))
imageNames = map(lambda fn: string.split(string.split(fn, os.sep)[1], '.')[0], images)

def quit():
	FILE.close()
	sys.exit(0)
def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
def readBox(imfile):
	boxfile = open(os.path.join('boxes', imfile+'.txt'), 'r')
	box = [[],[]]
	box[0] = map(int, string.split(boxfile.readline().strip(), ','))
	box[1] = map(int, string.split(boxfile.readline().strip(), ','))
	boxfile.close()
	return(box)
def drawBox(clickFrame):
	pygame.draw.rect(SCREEN, (255,0,0), (clickFrame[0][0]+imgPos[0], \
			clickFrame[0][1]+imgPos[1],clickFrame[1][0]-clickFrame[0][0], \
			clickFrame[1][1]-clickFrame[0][1]), 3)
def waitForClick():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = event.pos
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	clickPos = [clickPos[0]-imgPos[0], clickPos[1]-imgPos[1]]
	return(clickPos)
def showText(SCREEN, text, pos=textPos):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

def runTrial(SCREEN, imfile):
	image1 = pygame.image.load(os.path.join(imDirA, imfile+'.jpg'))
	image2 = pygame.image.load(os.path.join(imDirB, imfile+'.jpg'))
	clickFrame = readBox(imfile)
	iterations = attempts = phase = 0
	detected = False
	timeTrialStart = pygame.time.get_ticks()
	while(not detected):
		runtime = pygame.time.get_ticks() - timeTrialStart
		modtime = runtime % (timeImage*2 + timeBlank*2)
		if(phase == 0 and modtime>0 and modtime<timeImage):
			SCREEN.fill(bgcol)
			SCREEN.blit(image1, imgPos)
			SCREEN.blit(textSpace, textPos)
			if(DEBUG): drawBox(clickFrame)
			pygame.display.flip()
			phase = 1
		elif(phase == 1 and modtime>timeImage and modtime<(timeImage+timeBlank)):
			SCREEN.fill(bgcol)
			SCREEN.blit(textSpace, textPos)
			if(DEBUG): drawBox(clickFrame)
			pygame.display.flip()
			phase = 2
		elif(phase == 2 and modtime>(timeImage+timeBlank) and modtime<(timeImage*2+timeBlank)):
			SCREEN.fill(bgcol)
			SCREEN.blit(image2, imgPos)
			SCREEN.blit(textSpace, textPos)
			if(DEBUG): drawBox(clickFrame)
			pygame.display.flip()
			phase = 3
		elif(phase == 3 and modtime>(timeImage*2+timeBlank)):
			SCREEN.fill(bgcol)
			SCREEN.blit(textSpace, textPos)
			if(DEBUG): drawBox(clickFrame)
			pygame.display.flip()
			phase = 0
			iterations += 1
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = [event.pos[0]-imgPos[0], event.pos[1]-imgPos[1]]
				attempts += 1
				if(clickPos[0] > clickFrame[0][0] and clickPos[0] < clickFrame[1][0] and \
					clickPos[1] > clickFrame[0][1] and clickPos[1] < clickFrame[1][1]):
					detected = True
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	textFBgood = FONT.render('Right!  Your time: ' + str(runtime/1000) + ' sec', 1, (0,60,0))
	SCREEN.fill(bgcol)
	SCREEN.blit(textFBgood, textPos)
	if(DEBUG): drawBox(clickFrame)
	pygame.display.flip()
	pygame.time.wait(1000)
	return({'image': imfile, 'trialTime': runtime, 'loopTime': runtime, \
			'iterations': iterations, 'attempts':attempts})

showText(SCREEN, 'Welcome to our experiment!', textPos)
waitForKey()
showText(SCREEN, 'Click on the change when you see it', textPos)
waitForKey()
random.shuffle(images)

first = True
for imfile in imageNames:
	showText(SCREEN, 'Press space for the next trial!', textPos)
	waitForKey()
	trialOutput = runTrial(SCREEN, imfile)
	header = ''
	line = ''
	for k,v in trialOutput.iteritems():
		header += k + '\t'
		line += str(v) + '\t'
	if first:
		first = False
		FILE.write(header+'\n')
	FILE.write(line+'\n')

showText(SCREEN, 'Thank you for your participation!', textPos)
waitForKey()

quit()
