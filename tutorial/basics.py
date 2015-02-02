import random

subject = raw_input('What is the subject ID? ')
print('Subject ID: ' + subject)
filename = subject + '.txt'
filedir = 'data'
filepath = filedir + '/' + filename
FILE = open(filepath, 'w')
FILE.write('Subject ID: ' + subject + '\n')

FILE.write('trial\tN1\tN2\tCorrect\tResponse\n')

i = 1
while i<10:
	print('trial ' + str(i))
	int1 = random.randint(10,50)
	int2 = random.randint(10,50)
	correct = int1 + int2
	response = raw_input('What is ' + str(int1) + '+' + str(int2) + '? ')
	print('You said: ' + response + '; answer was:' + str(correct))
	FILE.write(str(i) + '\t' + str(int1) + '\t' + str(int2) + '\t' + str(correct) + '\t' + response + '\n')
	i = i+1

FILE.close()



def waitForClick():
	wait = True
	while wait:
		for event in pygame.event.get():
			if (event.type == MOUSEBUTTONDOWN):
				return(event.pos)
			if (event.type == KEYDOWN and event.key == K_ESCAPE):
				quit()
	
