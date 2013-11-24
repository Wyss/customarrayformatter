'''
test.py 

Contains unit tests for customarrayparse.py

'''

from customarrayparse import CustomArrayParse

# Tab delimited input file
test = CustomArrayParse('test/tab_delim.txt')
test.process()

# Blank lines in inupt file
test = CustomArrayParse('test/blank_lines.csv')
test.process()

# Reversed columns in input file
test = CustomArrayParse('test/reversed_columns.csv')
test.process()

# Multiple oligo name duplicates in input file
test = CustomArrayParse('test/multiple_duplicates.csv')
test.process()

# Custom output file
test = CustomArrayParse('test/tab_delim.txt', 
					    output_file='test/CUSTOM_OUTPUT_FN.txt')
test.process()

# Xslx test
test = CustomArrayParse('test/xlsx_test.xlsx')
test.process()

# Full 12k test
test = CustomArrayParse('test/12k.csv')
test.process()

# Full 96k test
test = CustomArrayParse('test/96k.csv')
test.process()

# Multiple oligo name duplicates in input file
test = CustomArrayParse('test/three_columns.csv')
test.process()
