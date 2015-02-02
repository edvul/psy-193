from __future__ import division
from collections import OrderedDict
import os
import sys
import random
import glob
import string
import pygame
from pygame.locals import *

DEBUG = True

# Various setup stuff
colBackground = (255, 255, 255)
colFont = (0, 0, 0)
fontSize = 24
fontFace = "Arial"
textPos = (1,1)
imgPos = (0,0)
probes = ["A", "B", "C", "D", "E", "F"]
timingTrial = {"image":6000}
recordedKeys = []
trialPath = os.path.join('.', 'Stimuli')
trialSets = next(os.walk(trialPath))[1]


# set up subject details
os.system('cls' if os.name == 'nt' else 'clear')
if(not DEBUG):
	subject = raw_input('Please enter the subject ID: ')
else:
	subject = "DEBUG"
FILE = open(os.path.join('data', subject + '.csv'), 'a')
FILE.write('Subject: %s\n' 	% subject)

pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
if(DEBUG):
	SCREEN = pygame.display.set_mode((1024,768), 16) #pygame.FULLSCREEN
else:
	SCREEN = pygame.display.set_mode((1024,768), pygame.FULLSCREEN)

FONT = pygame.font.Font(None, fontSize)


class ImageSet(object):
	def __init__(self, setPath, setName):
		self.image = pygame.image.load(os.path.join(setPath, setName, setName+'.JPG'))
		self.probe = {}
		for s in probes:
			self.probe[s] = pygame.image.load(os.path.join(setPath, setName, setName+s+'.JPG'))
		self.correct = {}
		f = open(os.path.join(setPath, setName, "CORRECT.txt"), 'r')
		for line in f.readlines():
			k,v = line.split(' ')
			self.correct[k] = v
		f.close()

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
		for k,v in trialOutput.iteritems():
			header += k + ',\t'
			recordedKeys.append(k)
			line += str(v) + ',\t'
		FILE.write(header+'\n')
	else:
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

def waitForYN():
	wait = True
	tStart = pygame.time.get_ticks()
	while wait:
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_y):
				response = "Y"
				wait = False
			elif (event.type == KEYDOWN and event.key == K_n):
				response = "N"
				wait = False
			elif (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit(False)
	return([response, pygame.time.get_ticks()-tStart])

def showText(SCREEN, text, pos=textPos, textCol=colFont):
	SCREEN.fill(colBackground)
	lines = text.split('\n')
	nlines = len(lines)
	renderedLines = list()
	for n in range(0,nlines):
		renderedLines.append(FONT.render(lines[n], 1, textCol))
	totalHeight = sum(map(lambda x: x.get_rect().height, renderedLines))
	for n in range(0,nlines):
		textpos = renderedLines[n].get_rect()
		textpos.centerx = SCREEN.get_rect().centerx
		textpos.centery = SCREEN.get_rect().centery+totalHeight*(n/nlines - 1/2)
		SCREEN.blit(renderedLines[n], textpos)
	pygame.display.flip()

def runTrial(SCREEN, imPath, imSet, timing):
	trialSet = ImageSet(imPath, imSet)
	timeTrialStart = pygame.time.get_ticks()
	
	SCREEN.fill(colBackground)
	SCREEN.blit(trialSet.image, imgPos)
	pygame.display.flip()
	pygame.time.wait(timing["image"])
	responses = {}
	responseTimes = {}
	for s in probes:
		SCREEN.fill(colBackground)
		SCREEN.blit(trialSet.probe[s], imgPos)
		pygame.display.flip()
		responses[s],responseTimes[s] = waitForYN()
	totalTime = pygame.time.get_ticks() - timeTrialStart
	trialData = {'image':imSet, 'time':totalTime}
	for s in probes:
		if(DEBUG): print(responses[s])
		if(DEBUG): print(responseTimes[s])
		if(DEBUG): print(trialSet.correct[s])
		
		trialData[s+'_response'] = responses[s]
		trialData[s+'_responseTime'] = responseTimes[s]
		trialData[s+'_correct'] = int(responses[s]==trialSet.correct[s])
	return(trialData)

showText(SCREEN, 'You will be shown a series of pictures, one at a time. \n Each picture will only be shown once for six seconds. \n After each picture, you will be shown various objects. \n You will have to answer yes or no as to whether you\'ve seen the object in the previous picture. \n Push the "Y" key if you think the object was in the previous picture, \n and push the "N" key if you think the object was not in the previous picture. \n After you have been shown 10 pictures, you will watch a short video before continuing with the final set of images. \n \n Press the SPACE bar to begin. ')
waitForKey(K_SPACE)

random.shuffle(trialSets)

first = True
if(DEBUG): print(trialSets)
for trSet in trialSets:
	trialOutput = runTrial(SCREEN, trialPath, trSet, timingTrial)
	first = writeTrial(FILE, trialOutput, first)

showText(SCREEN, 'Thank you for participating in our experiment.')
waitForKey(K_SPACE)

quit(True)
