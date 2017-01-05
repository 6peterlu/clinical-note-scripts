'''
Clinical Note Preprocessor

Current features:
1. All numbers replaced with word version of number(i.e. 3 -> three)
2. Strips all new lines
3. Strips extra whitespace
4. All sentence boundaries converted to carats
5. Numbers with more than one digit removed

Features in development:
1. Turn dates into recognizable ML tokens
2. Convert input format to command line arguments
3. Abstract processing into method

Created by Peter Lu (peterlu6@stanford.edu)
Last modified: 13 September 2016
'''

#from num2words import num2words #package needed for number to word conversion (no longer necessary)

import re #package needed for regular expression search for digits
import sys #read command line arguments

def get_word_representation_of_digit(num):
	if num == 0:
		return "zero";
	elif num == 1:
		return "one";
	elif num == 2:
		return "two";
	elif num == 3:
		return "three";
	elif num == 4:
		return "four";
	elif num == 5:
		return "five";
	elif num == 6:
		return "six";
	elif num == 7:
		return "seven";
	elif num == 8:
		return "eight";
	elif num == 9:
		return "nine";
	else:
		return "word representation error with the number " + str(num);

#line by line modification
def clean_line(line):
	numberarray = re.findall('\\d+', line);#gets array of numbers found in string
	cleaned = "";
	curindex = 0; #tracks how much of the original string has been copied over so far
	for num in numberarray:
		startindex = line.find(num);
		endindex = startindex + len(num);#getting start and end index of each number found in string
		cleaned = cleaned + line[curindex:startindex];
		if num < 10 and num >= 0: #only adding in number if its a one digit number
			cleaned = cleaned + num2words(int(num));
		curindex = endindex;
	if curindex < len(line) - 1: #checking if any additional text is left after the last number
		cleaned = cleaned + line[curindex:len(line)];

	cleaned = cleaned.replace('. ', '^');                  #replacing all periods with carat symbols
	cleaned = cleaned.replace('.\n', '^');                 
	cleaned = cleaned.replace('\n', ' ');                  #replacing all new lines with spaces
	cleaned = cleaned.replace(',', ' ');                   #replacing all commas with spaces
	cleaned = cleaned.replace('/', ' ');                   #replacing all slashes with spaces
	cleaned = cleaned.replace('-', ' ');                   #replacing all dashes with spaces
	cleaned = cleaned.replace(':', ' ');                   #replacing all colons with spaces
	cleaned = cleaned.lower();                             #changing all characters to lowercase
	cleaned = re.sub('[;()"%\'\.]', '', cleaned);              #removing all special characters
	return cleaned;

def preprocess(infile, outfile):
	newfiledata = ''
	for line in infile:
		newfiledata = newfiledata + clean_line(line); #writing cleaned text to output string
	newfiledata = ' '.join(newfiledata.split());
	newfiledata = newfiledata.replace('^ ', '^');
	outfile.write(newfiledata);

def main():
	num_arguments = len(sys.argv)
	infilename = sys.argv[1];
	outfilename = sys.argv[2];
	date = sys.argv[3];
	exclude_list = [];
	for i in range(4, num_arguments):
		exclude_list.append(sys.argv[i])
	infile = open(infilename, 'r');
	outfile = open(outfilename, 'w');

	preprocess(infile, outfile);

	infile.close();
	outfile.close();

	print "\nDone! Cleaned text is in " + outfilename;

main()