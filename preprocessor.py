'''
Clinical Note Preprocessor

Current features:
1. All numbers replaced with word version of number(i.e. 3 -> three)
2. Strips all new lines
3. Strips extra whitespace
4. All sentence boundaries converted to carats

Features in development:
1. Numbers with more than one digit removed
2. Turn dates into recognizable ML tokens
3. Convert input format to command line arguments
4. Abstract processing into method

Created by Peter Lu (peterlu6@stanford.edu)
Last modified: 13 September 2016
'''

from num2words import num2words #package needed for number to word conversion
import re #package needed for regular expression search for digits

def clean_line(line):
	numberarray = re.findall('\\d+', line);#gets array of numbers found in string
	cleaned = "";
	curindex = 0; #tracks how much of the original string has been copied over so far
	for num in numberarray:
		startindex = line.find(num);
		endindex = startindex + len(num);#getting start and end index of each number found in string
		cleaned = cleaned + line[curindex:startindex] + num2words(int(num));
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


def clean_file(infile, outfile):
	newfiledata = ''
	for line in infile:
		newfiledata = newfiledata + clean_line(line); #writing cleaned text to output string
	newfiledata = ' '.join(newfiledata.split());
	newfiledata = newfiledata.replace('^ ', '^');
	outfile.write(newfiledata);

def main():
	infilename = raw_input('Input text filename? (Ex: progressnote.txt) ');
	outfilename = raw_input('Output filename? (Ex: output.txt) ');

	infile = open(infilename, 'r');
	outfile = open(outfilename, 'w');

	clean_file(infile, outfile);

	infile.close();
	outfile.close();

	print "\nDone! Cleaned text is in " + outfilename;

main()