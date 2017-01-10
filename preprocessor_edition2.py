'''
Clinical note preprocessor for machine learning algorithms.

CREATED BY: Peter Lu (peterlu6@stanford.edu)

USAGE: python preprocessor.py inputfile.txt outputfile.txt date excludelist1 excludelist2 ...

FEATURES:
1. change all text to lowercase
2. remove all numbers except single digits
3. remove all special characters
4. remove all matches to exclude list
5. substitute all one digit numbers with strings
6. remove extraneous whitespace
7. remove new lines

TODO:
1. recognize dates
2. mark dates by time before input date
3. put events in chronological order
4. possibly merge words that are separated by dashes?


LAST UPDATED: 1/8/2017
'''
import re #regexes
import sys #command line arguments

def concatenate_into_string(infile):
	total_text = ""
	for line in infile:
		line = line.replace('\n', ' ')
		total_text += line
	return total_text

def substitute_word_for_digit(output):
	output = re.sub(r"0", " zero ", output)
	output = re.sub(r"1", " one ", output)
	output = re.sub(r"2", " two ", output)
	output = re.sub(r"3", " three ", output)
	output = re.sub(r"4", " four ", output)
	output = re.sub(r"5", " five ", output)
	output = re.sub(r"6", " six ", output)
	output = re.sub(r"7", " seven ", output)
	output = re.sub(r"8", " eight ", output)
	output = re.sub(r"9", " nine ", output)
	return output

def remove_forbidden_tokens(output, exclude_list):
	for item in exclude_list:
		output = re.sub(r""+re.escape(item)+r"", "", output)
	return output


'''
The primary method. Takes input as a string and an exclusion list of strings and outputs a string.
'''
def preprocess(inputstr, exclude_list):
	output = inputstr.lower()
	output = re.sub(r"\d\d+", "", output) #remove multidigit numbers
	output = re.sub(r'[;()"%\'\.\/\:\?\-,]', '', output) #remove special characters
	output = substitute_word_for_digit(output) #substitute single digit numbers with words
	output = remove_forbidden_tokens(output, exclude_list)
	output = re.sub(r" +", " ", output) #remove extraneous whitespace
	return output

def write_to_file(outputstr, outfile):
	outfile.write(outputstr)

def main():
	num_arguments = len(sys.argv)
	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	date = sys.argv[3]

	exclude_list = []
	for i in range(4, num_arguments): #populate exclude list
		exclude_list.append(sys.argv[i])

	infile = open(infilename, 'r')
	inputstr = concatenate_into_string(infile)
	infile.close()

	outputstr = preprocess(inputstr, exclude_list)
	outfile = open(outfilename, 'w')
	write_to_file(outputstr, outfile)
	outfile.close()

	print "\nDone! Cleaned text is in " + outfilename

main()