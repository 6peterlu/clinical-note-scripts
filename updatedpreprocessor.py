'''
Clinical note preprocessor.

Created by Peter Lu (peterlu6@stanford.edu)

Features added:

TODO:
1. change all text to lowercase *
2. concatenate into single string *
3. remove all numbers except single digits (test this)
4. remove all matches to exclude list
5. mark dates by time before input date
'''
import re #regexes
import sys #command line arguments

def concatenate_into_string(infile):
	total_text = ""
	for line in file:
		line = line.replace('\n', ' ')
		total_text += line
	return line

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

def preprocess(input):
	output = input.lower()
	output = re.sub(r"\d\d+", "")
	return output

def main():
	num_arguments = len(sys.argv)
	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	date = sys.argv[3]
	exclude_list = []
	for i in range(4, num_arguments):
		exclude_list.append(sys.argv[i])
	infile = open(infilename, 'r')
	outfile = open(outfilename, 'w')

	preprocess(infile, outfile)

	infile.close()
	outfile.close()

	print "\nDone! Cleaned text is in " + outfilename

main()