from __future__ import division
from collections import OrderedDict
import os
import sys
import random
import glob
import string
import pygame
from pygame.locals import *

DEBUG = False

# Various setup stuff
colBackground = (255, 255, 255)
colFont = (0, 0, 0)
fontSize = 24
fontFace = "Arial"
textPos = (1,1)
imgPos = (0,0)
timingPractice1 = {"image":1000, "blank":100, "expired":60*60*1000}
timingPractice2 = {"image":560, "blank":100, "expired":60*60*1000}
timingTrial = {"image":560, "blank":100, "expired":60*1000}
recordedKeys = ['image', 'time', 'clickAttempts', 'allClicks']

# set up subject details
os.system('cls' if os.name == 'nt' else 'clear')
if(not DEBUG):
	subject = input('Please enter the subject ID: ')
else:
	subject = "DEBUG"
FILE = open(os.path.join('data', subject + '.csv'), 'a')
FILE.write('Subject: %s\n' 	% subject)

if(not DEBUG):
	FILE.write('\tage: %s\n' 	% input('What is your age? [enter an integer]' ).strip())
	FILE.write('\tgender: %s\n' % input('What is your gender?' ).strip())
	FILE.write('\trace: %s\n' 	% input('What is your race? (write "Decline to answer" if you prefer not to answer) ').strip())
	FILE.write('\tvision: %s\n' 	% input('Do you have normal/corrected-to-normal vision? [Y/N] ').strip())
	FILE.write('\teducation: %s\n' % input('What is your education? ').strip())
	FILE.write('\tmajor: %s\n' % input('What is your major? ').strip())


pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
if(DEBUG):
	SCREEN = pygame.display.set_mode((1024,768), 16) #pygame.FULLSCREEN
else:
	SCREEN = pygame.display.set_mode((1024,768), pygame.FULLSCREEN)
FONT = pygame.font.Font(None, fontSize)
textFBbad = FONT.render('C', 1, (160,0,0))
textFBgood = FONT.render('Right!', 1, (0,160,0))

trialPath = os.path.join('.', 'Stimuli', 'Experiment')
trialSets = next(os.walk(trialPath))[1]
practicePath = os.path.join('.', 'Stimuli', 'Practice')
practiceSets = next(os.walk(practicePath))[1]

# Print: "Thank you for volunteering to participate in our experiment. Please press the spacebar to continue.""
# Wait for spacebar press.

class ImageSet(object):
	def __init__(self, setPath, setName):
		self.imageA = pygame.image.load(os.path.join(setPath, setName, setName+'A.JPG'))
		self.imageB = pygame.image.load(os.path.join(setPath, setName, setName+'B.JPG'))
		fileA = open(os.path.join(setPath, setName, setName+'A.txt'), 'r')
		self.A1 = list(map(int, fileA.readline().strip().split(',')))
		self.A2 = list(map(int, fileA.readline().strip().split(',')))
		fileA.close()
		fileB = open(os.path.join(setPath, setName, setName+'B.txt'), 'r')
		self.B1 = list(map(int, fileB.readline().strip().split(',')))   
		self.B2 = list(map(int, fileB.readline().strip().split(',')))
		fileB.close()
	def CoordsIn(self, x, y, C1, C2):
		inside = ((C1[0] <= x <= C2[0]) & (C1[1] <= y <= C2[1]))
		if(DEBUG): print("(%d <= %d <= %d & %d <= %d <= %d) = %d"%(C1[0], x, C2[0], C1[1], y, C2[1], inside))
		return(inside)
	def CoordsInA(self, x, y):
		return(self.CoordsIn(x, y, self.A1, self.A2))
	def CoordsInB(self, x, y):
		return(self.CoordsIn(x, y, self.B1, self.B2))

def quit(complete):
	FILE.close()
	if(complete == False):
		print("Experiment quit before completion (likely due to escape key)")
	else:
		print("Experiment quit successfully")
	sys.exit(0)

def writeTrial(FILE, trialOutput, first):
	header = ''
	line = ''
	if first:
		first = False
		global recordedKeys
		for k in recordedKeys:
			header += k + ',\t'
		FILE.write(header+'\n')
	for k in recordedKeys:
		line += str(trialOutput[k]) + ',\t'
	FILE.write(line+'\n')
	return(first)


def waitForKey(target_key):
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == target_key):
				wait = False
			elif (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit(False)

def showText(SCREEN, text, pos=textPos, textCol=colFont):
	SCREEN.fill(colBackground)
	lines = text.split('\n')
	renderedLines = list()
	for n in range(0,len(lines)):
		renderedLines.append(FONT.render(lines[n], 1, textCol))
	totalHeight = sum(map(lambda x: x.get_rect().height, renderedLines))
	for n in range(0,len(lines)):
		textpos = renderedLines[n].get_rect()
		textpos.centerx = SCREEN.get_rect().centerx
		textpos.centery = SCREEN.get_rect().centery-totalHeight+n*textpos.height
		SCREEN.blit(renderedLines[n], textpos)
	pygame.display.flip()

def showImages(SCREEN, imPath, imSet, timing):
	trialSet = ImageSet(imPath, imSet)
	SCREEN.fill(colBackground)
	SCREEN.blit(trialSet.imageA, imgPos)
	if(DEBUG): 
		transRect = pygame.Surface((trialSet.A2[0]-trialSet.A1[0], trialSet.A2[0]-trialSet.A1[0]))
		transRect.set_alpha(128)
		transRect.fill((255,0,0))
		SCREEN.blit(transRect, (trialSet.A1[0], trialSet.A1[1]))
	pygame.display.flip()
	pygame.time.wait(timing["image"])

	SCREEN.fill(colBackground)
	pygame.display.flip()
	pygame.time.wait(timing["blank"])

	SCREEN.fill(colBackground)
	SCREEN.blit(trialSet.imageB, imgPos)
	if(DEBUG):
		transRect = pygame.Surface((trialSet.B2[0]-trialSet.B1[0], trialSet.B2[0]-trialSet.B1[0]))
		transRect.set_alpha(128)
		transRect.fill((255,0,0))
		SCREEN.blit(transRect, (trialSet.B1[0], trialSet.B1[1]))
	pygame.display.flip()
	pygame.time.wait(timing["image"])

	SCREEN.fill(colBackground)
	pygame.display.flip()
	pygame.time.wait(1000)

def runTrial(SCREEN, imPath, imSet, timing):
	allClicks = ''
	trialSet = ImageSet(imPath, imSet)
	iterations = 0
	attempts = 0
	detected = False
	phase = 0
	targetClicked = False
	timeExpired = False
	timeTrialStart = pygame.time.get_ticks()
	while(not targetClicked and not timeExpired):
		runtime = pygame.time.get_ticks() - timeTrialStart
		if(runtime > timing["expired"]): timeExpired = True
		modtime = runtime % (timing["image"]*2 + timing["blank"]*2)
		if(phase == 0 and modtime>0 and modtime<timing["image"]):
			SCREEN.fill(colBackground)
			SCREEN.blit(trialSet.imageA, imgPos)
			if(DEBUG): 
				transRect = pygame.Surface((trialSet.A2[0]-trialSet.A1[0], trialSet.A2[0]-trialSet.A1[0]))
				transRect.set_alpha(128)
				transRect.fill((255,0,0))
				SCREEN.blit(transRect, (trialSet.A1[0], trialSet.A1[1]))
			pygame.display.flip()
			phase = 1
		elif(phase == 1 and modtime>timing["image"] and modtime<(timing["image"]+timing["blank"])):
			SCREEN.fill(colBackground)
			pygame.display.flip()
			phase = 2
		elif(phase == 2 and modtime>(timing["image"]+timing["blank"]) and modtime<(timing["image"]*2+timing["blank"])):
			SCREEN.fill(colBackground)
			SCREEN.blit(trialSet.imageB, imgPos)
			if(DEBUG):
				transRect = pygame.Surface((trialSet.B2[0]-trialSet.B1[0], trialSet.B2[0]-trialSet.B1[0]))
				transRect.set_alpha(128)
				transRect.fill((255,0,0))
				SCREEN.blit(transRect, (trialSet.B1[0], trialSet.B1[1]))
			pygame.display.flip()
			phase = 3
		elif(phase == 3 and modtime>(timing["image"]*2+timing["blank"])):
			SCREEN.fill(colBackground)
			pygame.display.flip()
			phase = 0
			iterations += 1
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = event.pos
				x,y = clickPos
				allClicks += "(%d,%d) " % (x,y)
				attempts += 1
				if(DEBUG): print("click! (%d,%d)\n"%(x,y))
				if(((phase == 1 or phase == 2) and trialSet.CoordsInA(x,y)) or ((phase == 3 or phase == 0) and trialSet.CoordsInB(x,y))):
					targetClicked = True
				else:
					# do nothing
					attempts += 1
					targetClicked = False
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	totalTrialTime = pygame.time.get_ticks() - timeTrialStart
	if(targetClicked): 
		showText(SCREEN, 'Correct! \n \nPress space to continue.', textCol=(11,97,11))
		waitForKey(K_SPACE)
	if(timeExpired):
		showText(SCREEN, 'Unfortunately, you did not detect the change quickly enough. \n \n Please press space to continue.', textCol=(204,26,26))
		waitForKey(K_SPACE)
	return({'image':imSet, 'time':runtime, 'clickAttempts':attempts, 'allClicks':allClicks})

showText(SCREEN, 'Thank you for volunteering to participate in our experiment. \n \n Please press the spacebar to continue.')
waitForKey(K_SPACE)
showText(SCREEN, 'In this experiment you will be viewing sets of alternating images, and your task will be to identify the change in the scene. \nPossible risks include eyestrain and boredom. \nYour compensation will be the joy of helping students collect data for their research project. \n \n If you consent to these conditions, please press the spacebar to continue.')
waitForKey(K_SPACE)

random.shuffle(trialSets)

first = True
if(DEBUG): print(practiceSets)
showText(SCREEN, 'We will now start a trial session for you to practice what you will be doing in the experiment. \nYou will see two alternating images, separated by a flash. \n \nPress space to continue.')
waitForKey(K_SPACE)
showImages(SCREEN, practicePath, practiceSets[0], timingPractice1)
showText(SCREEN, 'Your task is to click in the middle of the area in either picture where you identified the change. \n \n Press space to continue')
waitForKey(K_SPACE)
trialOutput = runTrial(SCREEN, practicePath, practiceSets[0], timingPractice1)
first = writeTrial(FILE, trialOutput, first)

showText(SCREEN, 'Congratulations! \nYou have successfully found the change. \nIn the actual experiment, display times will be shorter, so we will now practice under those conditions. \n \n Press space to continue')
waitForKey(K_SPACE)
trialOutput = runTrial(SCREEN, practicePath, practiceSets[1], timingPractice2)
first = writeTrial(FILE, trialOutput, first)
showText(SCREEN, 'Congratulations! \nYou have successfully found the change. \n \n Note that in the actual experiment, you will need to find the change within a certain amount of time.\n \n If you have any questions at this point, please ask the experimenter. \n \nPress space to continue.')
waitForKey(K_SPACE)


showText(SCREEN, 'You will now begin the experimental portion of this session. \n \n Please press space to continue.')
waitForKey(K_SPACE)
	
if(DEBUG): print(trialSets)
n = 0
for trSet in trialSets:
	if(n == 10):
		showText(SCREEN, 'You have reached the halfway mark of the experiment. \n \n You can choose to take a break or you can proceed through the rest of the experiment by pressing the spacebar')
		waitForKey(K_SPACE)
	trialOutput = runTrial(SCREEN, trialPath, trSet, timingTrial)
	first = writeTrial(FILE, trialOutput, first)
	n += 1


showText(SCREEN, 'Thank you for your participation! \n \n The purpose of this experiment was to determine whether people are more attentive to certain types of change. \n \n Please contact the experimenter.')
waitForKey(K_ESCAPE)

quit(True)