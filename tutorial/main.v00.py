# these specify which libraries we will use
from __future__ import division
import os
import sys

# Get subject ID (name?)
subject = raw_input('Enter subject ID here: ')
print('Subject ID is: ', subject)

# use subject name to define a filename, and then a path to a file
filename = subject + '.csv'
print('filename: ', filename)
filepath = os.path.join('data', filename)
print('filepath: ', filepath)

# open file for writing.
FILE = open(filepath, 'w')

# write a line to a file.
FILE.write('Subject: %s\n' % subject)

print('thank you for your participation!')

# close the file and exit.
FILE.close()
sys.exit(0)
