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
8. mark dates by time before input date

TODO:
1. put events in chronological order
2. integrate ontology


LAST UPDATED: 1/10/2017
'''
import re #regexes
import sys #command line arguments

date_input = "" #global for date input (can be removed if we use lambdas later)

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

def time_elapsed(match_group):
	date_input_group = re.match(r"(\d+)\/(\d+)\/(\d+)", date_input)
	input_month = int(date_input_group.group(1))
	input_day = int(date_input_group.group(2))
	input_year = int(date_input_group.group(3))
	matched_month = int(match_group.group(1))
	matched_day = int(match_group.group(2))
	matched_year = int(match_group.group(3))

	if input_year - matched_year > 2:
		return "twoyearsago"
	elif input_year - matched_year > 1:
		return "oneyearago"
	elif input_month - matched_month > 9:
		return "ninemonthsago"
	elif input_month - matched_month > 6:
		return "sixmonthsago"
	elif input_month - matched_month > 3:
		return "threemonthsago"
	elif input_month - matched_month > 2:
		return "twomonthsago"
	elif input_month - matched_month > 1:
		return "onemonthago"
	elif input_day - matched_day > 14:
		return "twoweeksago"
	elif input_day - matched_day > 7:
		return "oneweekago"
	else:
		return "recent"

'''
The primary method. Takes input as a string and an exclusion list of strings and outputs a string.
'''
def preprocess(inputstr, exclude_list):
	output = inputstr.lower() #tolowercase
	output = re.sub(r"(\d+)\/(\d+)\/(\d+)", time_elapsed, output) #processes dates of the form MM/DD/YYYY
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
	global date_input
	date_input = sys.argv[3]

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