from __future__ import division
import os
import sys
import random
import glob
import string
import math
import pygame
from pygame.locals import *

# Various setup stuff
subject = raw_input('Enter subject ID here: ')
SEARCHFILE = open(os.path.join('data', subject + '-search.txt'), 'w')
GROUPFILE = open(os.path.join('data', subject + '-group.txt'), 'w')

pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
SCREEN = pygame.display.set_mode((600,420), 16)
FONT = pygame.font.Font(None, 28)

textInstructionSearch = FONT.render('Click on the target!', 1, (0,0,96))
textInstructionGroup = FONT.render('Press a number from 0 (no grouping) to 9 (lots of grouping)', \
									1, (0,0,96))
gridX = 12
gridY = 8
offset = (0,20)
bgcol = (255, 255, 255)
textPos = (1,1)
imSize = (50,50)
ntrials = 3

# assuming images are coded as 01-A.png etc.
imgsets = ['01', '02', '03', '04', '05']
# number of set sizes per image set should be constant for all imgs
setsize = [[4, 16], [4, 25], [4, 36], [4, 49], [4, 64]]
# encode patterns...
patterns = glob.glob(os.path.join('patterns', '*.txt'))
pattern = []
i = 0
for filename in patterns:
	f = open(filename, 'r')
	pattern.append([])
	for line in f:
		pattern[i].append(line.strip())
	f.close()
	i += 1
def quit():
	GROUPFILE.close()
	SEARCHFILE.close()
	sys.exit(0)

def gridPos(grididx):
	xpos = (grididx%gridX)*imSize[0]+offset[0]
	ypos = math.floor(grididx/gridX)*imSize[1]+offset[1]
	return((xpos,ypos))

def showText(SCREEN, text, pos=textPos):
	SCREEN.fill(bgcol)
	textimg = FONT.render(text, 1, (0,0,0))
	SCREEN.blit(textimg, pos)
	pygame.display.flip()

def waitForKey():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_SPACE):
				wait = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()

def runSearchTrial(imgstem, sizen):
	imA = pygame.image.load(os.path.join('img', imgstem+'-A.png'))
	imB = pygame.image.load(os.path.join('img', imgstem+'-B.png'))
	usegrid = range(0,gridX*gridY)
	random.shuffle(usegrid)

	showText(SCREEN, 'Next trial, look for the target below.  Press SPACE to start.')
	SCREEN.blit(imA, (275, 175))
	pygame.display.flip()
	waitForKey()

	SCREEN.fill(bgcol)
	targetloc = gridPos(usegrid[0])
	SCREEN.blit(imA, gridPos(usegrid[0]))
	for i in range(1, sizen):
		SCREEN.blit(imB, gridPos(usegrid[i]))
	SCREEN.blit(textInstructionSearch, textPos)
	pygame.display.flip()

	searchStart = pygame.time.get_ticks()
	clicks = 0
	targetClicked = False
	while(not targetClicked):
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = event.pos
				clicks += 1
				if(clickPos[0] > targetloc[0] and clickPos[0] < (targetloc[0] + imSize[0]) and \
					clickPos[1] > targetloc[1] and clickPos[1] < (targetloc[1] + imSize[1])):
					targetClicked = True
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	searchTime = pygame.time.get_ticks() - searchStart
	return({'RT': searchTime, 'clicks': clicks})
	
def runSearchExpt():
	# randomize trial seq.  ntrials per imageset x setsize
	trialseq = range(0,len(imgsets)*len(setsize[0])*ntrials)
	sets = map(lambda n: int(n%len(imgsets)), trialseq)
	sizes = map(lambda n: int(math.floor(n/len(imgsets))%2), trialseq)
	random.shuffle(trialseq)

	showText(SCREEN, 'In this phase you will need to find a target among distracters', textPos)
	waitForKey()
	
	for trialn in range(0,len(trialseq)):
		setidx = sets[trialseq[trialn]]
		szidx = sizes[trialseq[trialn]]
	
		imgstem = imgsets[setidx]
		sizen = setsize[setidx][szidx]

		output = runSearchTrial(imgstem, sizen)
	
		trial = {'trial': trialn, 'set-size': sizen, 'images':imgstem, 'RT':output['RT'], \
				'clicks':output['clicks']}
		header = ''
		line = ''
		for k,v in trial.iteritems():
			header += k + '\t'
			line += str(v) + '\t'
		if trialn==0:
			first = False
			SEARCHFILE.write(header+'\n')
		SEARCHFILE.write(line+'\n')

def runGroupTrial(imgstem, pidx):
	imA = pygame.image.load(os.path.join('img', imgstem+'-A.png'))
	imB = pygame.image.load(os.path.join('img', imgstem+'-B.png'))

	showText(SCREEN, 'Press SPACE to start next trial.')
	waitForKey()

	SCREEN.fill(bgcol)
	for i in range(0,gridY):
		for j in range(0,gridX):
			pos = (j*imSize[0]+offset[0], i*imSize[1]+offset[1])
			if(pattern[pidx][i][j] == 'O'):
				SCREEN.blit(imA, pos)
			else:
				SCREEN.blit(imB, pos)
	SCREEN.blit(textInstructionGroup, textPos)
	pygame.display.flip()

	startTime = pygame.time.get_ticks()
	madeResponse = False
	while(not madeResponse):
		for event in pygame.event.get():
			if (event.type == KEYDOWN):
				if(event.unicode in map(str, range(0,10))):
					response = int(event.unicode)
					madeResponse = True
				elif(event.key == K_ESCAPE):
					quit()
	RT = pygame.time.get_ticks() - startTime
	return({'response':response, 'RT': RT})

def runGroupExpt():
	# randomize trial seq.  1 trial per imageset x pattern
	trialseq = range(0,len(imgsets)*len(pattern))
	sets = map(lambda n: int(n%len(imgsets)), trialseq)
	pats = map(lambda n: int(math.floor(n/len(imgsets))), trialseq)
	random.shuffle(trialseq)
	
	showText(SCREEN, 'In this phase describe grouping strength with a number', textPos)
	waitForKey()
	
	for trialn in range(0,len(trialseq)):
		setidx = sets[trialseq[trialn]]
		patidx = pats[trialseq[trialn]]
	
		imgstem = imgsets[setidx]
		output = runGroupTrial(imgstem, patidx)
	
		trial = {'trial': trialn, 'images':imgstem, 'RT':output['RT'], \
				'response':output['response']}
		header = ''
		line = ''
		for k,v in trial.iteritems():
			header += k + '\t'
			line += str(v) + '\t'
		if trialn==0:
			first = False
			GROUPFILE.write(header+'\n')
		GROUPFILE.write(line+'\n')

runGroupExpt()
runSearchExpt()

showText(SCREEN, 'Thank you for your participation!', textPos)
waitForKey()
	
quit()
