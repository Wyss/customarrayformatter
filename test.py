'''
test.py 

Contains unit tests for customarrayformatter.py

'''

from customarrayformatter import CustomArrayFormatter

# Tab delimited input file
test = CustomArrayFormatter('test/tab_delim.txt')
test.process()

# Blank lines in inupt file
test = CustomArrayFormatter('test/blank_lines.csv')
test.process()

# Reversed columns in input file
test = CustomArrayFormatter('test/reversed_columns.csv')
test.process()

# Multiple oligo name duplicates in input file
test = CustomArrayFormatter('test/multiple_duplicates.csv')
test.process()

# Custom output file
test = CustomArrayFormatter('test/tab_delim.txt', 
					    output_file='test/CUSTOM_OUTPUT_FN.txt')
test.process()

# Xslx test
test = CustomArrayFormatter('test/xlsx_test.xlsx')
test.process()

# Full 12k test
test = CustomArrayFormatter('test/12k.csv')
test.process()

# Full 96k test
test = CustomArrayFormatter('test/96k.csv')
test.process()

# Multiple oligo name duplicates in input file
test = CustomArrayFormatter('test/three_columns.csv')
test.process()
