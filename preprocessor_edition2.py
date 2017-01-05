'''
Clinical note preprocessor.

Created by Peter Lu (peterlu6@stanford.edu)

Usage: python preprocessor.py inputfile.txt outputfile.txt date excludelist1 excludelist2 ...

Features added:
1. change all text to lowercase
2. remove all numbers except single digits
3. remove all special characters

TODO:
1. remove all matches to exclude list
2. mark dates by time before input date
'''
import re #regexes
import sys #command line arguments

def concatenate_into_string(infile):
	total_text = ""
	for line in infile:
		line = line.replace('\n', ' ')
		total_text += line
	return total_text

def get_word_for_digit(digit):
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

def preprocess(inputstr):
	output = inputstr.lower()
	output = re.sub(r"\d\d+", "", output)
	output = re.sub(r'[;()"%\'\.\/\:\?\-]', '', output)
	return output

def write_to_file(outputstr, outfile):
	outfile.write(outputstr)

def main():
	num_arguments = len(sys.argv)
	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	date = sys.argv[3]
	exclude_list = []
	for i in range(4, num_arguments):
		exclude_list.append(sys.argv[i])

	infile = open(infilename, 'r')
	inputstr = concatenate_into_string(infile)
	infile.close()

	outputstr = preprocess(inputstr)
	outfile = open(outfilename, 'w')
	write_to_file(outputstr, outfile)
	outfile.close()

	print "\nDone! Cleaned text is in " + outfilename

main()