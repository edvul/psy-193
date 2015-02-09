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
recordedKeys = []
stimPath = os.path.join('.', 'Stimuli')
allimages = list(map(lambda x: "MoodyImage%02d"%x, range(1,2)))
textCol = (0,0,0)
first = True

timing = {"list":40*1000, "blank":3*1000, "break":5*1000, "image.on":5*1000, "timeout":10*1000}
if(DEBUG): timing = {"list":3*1000, "blank":0.5*1000, "break":0.5*1000, "image.on":5*1000, "timeout":10*1000}


# set up subject details
os.system('cls' if os.name == 'nt' else 'clear')
subject = input('Please enter the subject ID: ')
FILE = open(os.path.join('data', subject + '_mooney.csv'), 'a')
FILE.write('Subject: %s\n' 	% subject)

FILEMEM = open(os.path.join('data', subject + '_memory.csv'), 'a')
FILEMEM.write('Subject: %s\n' 	% subject)
FILEMEM.write('%s\t%s\t%s\t%s\n' 	% ('repetition', 'responseTime', 'anyresponse', ','.join(map(lambda x: 'response_'+str(x), range(1,26)))))

demofile = open(os.path.join('data', 'subjectsdemo.txt'), 'a')
demofile.write(str(subject))
demofile.write(', %s' 		% input('Enter Name' ).strip())
demofile.write(', %s' 		% input('Enter Age' ).strip())
demofile.write(', %s\n' 	% input('Enter Gender').strip())
demofile.close()

pygame.init()
pygame.mixer.init()
pygame.event.set_grab(1)
if(DEBUG):
	SCREEN = pygame.display.set_mode((1024,768), pygame.FULLSCREEN) #pygame.FULLSCREEN
else:
	SCREEN = pygame.display.set_mode((1024,768), pygame.FULLSCREEN)

FONT = pygame.font.Font(None, fontSize)

FONT2 = pygame.font.Font(None, fontSize+10)

def quit(complete):
	FILE.close()
	FILEMEM.close()
	if(complete == False):
		print("Experiment quit before completion (likely due to escape key)")
	else:
		print("Experiment quit successfully")
	sys.exit(0)

def showList(SCREEN, words):
	random.shuffle(words)
	cx = SCREEN.get_rect().centerx
	cy = SCREEN.get_rect().centery
	wx = SCREEN.get_rect().width
	wy = SCREEN.get_rect().height
	SCREEN.fill(colBackground)
	for i in range(0,5):
		ccx = cx+wx/6*(i-2)
		for j in range(0,5):
			ccy = cy+wy/12*(j-2)
			curtext = FONT.render(words[i*5+j], 1, textCol)
			textpos = curtext.get_rect()
			textpos.centerx = ccx
			textpos.centery = ccy
			SCREEN.blit(curtext, textpos)
	pygame.display.flip()

def reportList(SCREEN):
	cx = SCREEN.get_rect().centerx
	cy = SCREEN.get_rect().centery
	wx = SCREEN.get_rect().width
	wy = SCREEN.get_rect().height
	responses = ['']*25
	curword = 0
	finished = False
	nextIcon = FONT.render("NEXT", 1, (0, 96, 0))
	nextRect = nextIcon.get_rect()
	nextRect.centerx = cx
	nextRect.top = 0
	startTime = pygame.time.get_ticks()
	while(not finished):
		SCREEN.fill(colBackground)
		for i in range(0,5):
			ccx = cx+wx/6*(i-2)
			for j in range(0,5):
				ccy = cy+wy/12*(j-2)
				ci = i*5+j
				show = responses[ci]
				if ci == curword: show += "_"
				curtext = FONT.render(show, 1, textCol)
				textpos = curtext.get_rect()
				textpos.centerx = ccx
				textpos.centery = ccy
				SCREEN.blit(curtext, textpos)
		SCREEN.blit(nextIcon, nextRect)
		pygame.display.flip()
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				clickPos = event.pos
				x,y = clickPos
				if(DEBUG): print("click! (%d <= %d <= %d) and (%d <= %d <= %d)?\n"%(nextRect.left, x, nextRect.right, nextRect.top, y, nextRect.bottom))
				if (nextRect.left <= x <= nextRect.right) and (nextRect.top <= y <= nextRect.bottom):
					finished = True
			if (event.type == KEYDOWN and event.key == K_BACKSPACE):
				responses[curword] = responses[curword][:-1]
			if (event.type == KEYDOWN and event.key == K_RETURN):
				curword = (curword+1 if curword<23 else curword)
			if (event.type == KEYDOWN and (event.unicode in string.ascii_lowercase or event.unicode in string.ascii_uppercase)):
				responses[curword] += event.unicode
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit(False)
	totalTime = pygame.time.get_ticks()-startTime
	return(responses, totalTime)

def readList(filename):
	listfile = open(os.path.join(stimPath, filename), 'r')
	return([x.strip() for x in listfile.readlines()])

def writeTrial(FILE, trialOutput, first):
	header = ''
	line = ''
	if first:
		first = False
		global recordedKeys
		for k in trialOutput.keys():
			header += k + ',\t'
			recordedKeys.append(k)
			line += str(trialOutput[k]) + ',\t'
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
	totalHeight = sum(list(map(lambda x: x.get_rect().height, renderedLines)))
	for n in range(0,nlines):
		textpos = renderedLines[n].get_rect()
		textpos.centerx = SCREEN.get_rect().centerx
		textpos.centery = SCREEN.get_rect().centery+totalHeight*(n/nlines - 1/2)
		SCREEN.blit(renderedLines[n], textpos)
	pygame.display.flip()

def waitQuit(duration):
	stopped = False
	expired = False
	startTime = pygame.time.get_ticks()
	while(not stopped and not expired):
		runtime = pygame.time.get_ticks() - startTime
		if runtime>duration:
			expired = True
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				stopped = True
				quit(False)

def runTrial(SCREEN, imPath, imName, timing):
	image = pygame.image.load(os.path.join(imPath, imName+'.jpg'))
	timeTrialStart = pygame.time.get_ticks()
	finished = False
	display = True
	timeout = False
	response = ''
	while(not finished and not timeout):
		SCREEN.fill(colBackground)
		curtime = pygame.time.get_ticks()-timeTrialStart
		if(curtime > timing['image.on']): display = False
		if(curtime > timing['timeout']): timeout = True
		if(display): SCREEN.blit(image, imgPos)
		curtext = FONT2.render(response+'_', 1, (255,0,0))
		textpos = curtext.get_rect()
		textpos.centerx = SCREEN.get_rect().centerx
		textpos.bottom = SCREEN.get_rect().bottom
		SCREEN.blit(curtext, textpos)
		pygame.display.flip()
		for event in pygame.event.get():
			if (event.type == KEYDOWN and event.key == K_BACKSPACE):
				response = response[:-1]
			if (event.type == KEYDOWN and event.key == K_RETURN and len(response)>0):
				finished = True
			if (event.type == KEYDOWN and (event.unicode in string.ascii_lowercase or event.unicode in string.ascii_uppercase)):
				response += event.unicode
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit(False)
	return({'image':imName, 'response':response, 'responseTime':curtime, 'timeout':int(timeout)})

words = readList(listfile)

showText(SCREEN, 'Part 1: In the following portion of the study, you will be presented a list of 25 words. \n Please study them in the time allotted. \n You will have 40 seconds to view the word list. \n Try to remember as many of them as you can.  \n Your performance in this task will increase your ability to parse the ambiguous images presented in Part 2. \n Please press <Enter > to move on to the list of words.')
waitForKey(K_RETURN)
showList(SCREEN, words)
waitQuit(timing['list'])
showText(SCREEN, '')
waitQuit(timing['blank'])

showText(SCREEN, 'In the following screen please attempt to type out as many of the words as you can remember. \n You can type them in any order, just list as many as you can. \n Please take as long as you feel that you need. \n Press <Next> when you feel that you are finished. \n \n Press <Enter> to continue.')
waitForKey(K_RETURN)
responses,responseTime = reportList(SCREEN)
anyresponse = int(any(list(map(lambda x: len(x)>0, responses))))
FILEMEM.write('%d,%d,%d,%s\n' 	% (1, responseTime, anyresponse, ','.join(responses)))


showText(SCREEN, 'You will now be presented the same list of 25 words again. \n Please study them again in the time allotted. \n \n Press <Enter > to continue.')
waitForKey(K_RETURN)
showList(SCREEN, words)
waitQuit(timing['list'])

showText(SCREEN, 'Now please attempt to recall as many words as you can in the following screen, in any order. \n Be sure to also include words that you listed last time. \n Once again, please take as a long as you need. \n Press <Next> when you feel that you are finished. \n \n Press <Enter > to continue.')
waitForKey(K_RETURN)
responses,responseTime = reportList(SCREEN)
anyresponse = int(any(list(map(lambda x: len(x)>0, responses))))
FILEMEM.write('%d,%d,%d,%s\n' 	% (2, responseTime, anyresponse, ','.join(responses)))

showText(SCREEN, 'Like before, please attempt to recall the list of words. \n This time, the list will not be displayed to you. \nOnce again, take as long as you need. \nPress <Next> when you feel that you are finished. \n \n Press <Enter > to continue')
waitForKey(K_RETURN)
responses,responseTime = reportList(SCREEN)
anyresponse = int(any(list(map(lambda x: len(x)>0, responses))))
FILEMEM.write('%d,%d,%d,%s\n' 	% (3, responseTime, anyresponse, ','.join(responses)))

showText(SCREEN, 'Thank you. \n \n Part 1 of the study is now complete. \n \n Please press <Enter > to move on to Part 2.')
waitForKey(K_RETURN)

showText(SCREEN, '')
waitQuit(timing['break'])

showText(SCREEN, 'In the following slides you will see some images that may appear, at first, to be ambiguous. \n These are what are known as Mooney images.  \n Mooney images are two-tone derivations of natural images \n made by thresholding photographs under asymmetrical lighting conditions. \n Although some information about the photographed subject will be degraded, please identify the image presented onscreen.  \n Write your response in the space provided. \n Press <Enter> when you have finished writing your response. \n If you are unable to identify the image, type "none"  and press <Enter> to move to the next image.\n \n You will have 5 seconds to view each image, though you may provide your response at any time.\n \n Press <Enter> to begin trial.')
waitForKey(K_RETURN)

showText(SCREEN, 'To acquaint you with what these images look like we will begin with a practice trial.\n \n Please identify the image and provide your response.\n \n Press <Enter> when done to move to the next image.')
waitForKey(K_RETURN)

trialOutput = runTrial(SCREEN, stimPath, 'practice', timing)
first = writeTrial(FILE, trialOutput, first)


showText(SCREEN, 'We will now begin the experiment.\n \n press <Enter> to begin.')
waitForKey(K_RETURN)

for imageName in allimages:
	trialOutput = runTrial(SCREEN, stimPath, imageName, timing)
	first = writeTrial(FILE, trialOutput, first)
	
showText(SCREEN, 'Thank you for your participation.')
waitForKey(K_RETURN)

quit(True)