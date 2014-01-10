'''
customarrayformatter.py

Command line tool / python module to convert Excel (.xlsx) and delimited
text files (.csv or tab delimited .txt) into properly formatted tab
delimited text files for the Custom Array oligo synthesizer.

Usage:

$ python customarrayformatter.py [input file] -o [output file]

The file conversion process is fairly tolerate to formatting discrepencies
and may prompt the user for additional input in non-typical circumstances
(e.g., if the number of columns in the input file is greater than 2).

'''

import argparse
import os
import re

import openpyxl         # Lib for dealing with .xlsx files (MIT License)


class CustomArrayFormatter(object):

    def __init__(self, input_file, output_file=None):
        with open(input_file):  # Make sure the file exists
            pass
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        self.parseFile()
        self.writeFile()

    def parseFile(self):

        def _checkCell(cell):
            ''' Returns false if a cell is blank/empty (otherwise True) '''
            return False if len(cell) < 2 or cell[0] == None else True

        # Identify file type and read in contents
        ext = self.input_file.split('.')[-1]
        if ext == 'xlsx':
            row_data = self._readInXlsx()
        elif ext in ('txt', 'csv'):
            row_data = self._readInDelim()
        else:
            raise ValueError('Input file must be a .xlsx, .csv, or .txt file')
        # Remove blank/empty cells
        self.row_data = filter(_checkCell, row_data)
        # Ask user to ID columns if needed, otherwise automatically ID columns
        nc = len(self.row_data[0])
        if nc > 2:
            print 'Input file contains more than 2 columns of data: '
            for index, cell in enumerate(self.row_data[0]):
                print '\t Column {}: {}'.format(index + 1, cell)
            self.seq_col = self._reqCol(nc, '\t-> Enter oligo sequence column '
                                            'number')
            self.name_col = self._reqCol(nc, '\t-> Enter sequence name column '
                                             'number')
        else:
            self.seq_col = 0 if re.match('^[ATGC\s]+$', self.row_data[0][0]) else 1
            self.name_col = 0 if self.seq_col else 1
        self._dataQC()


    def writeFile(self):
        if not self.output_file:
            fp, ext = os.path.splitext(self.input_file)
            self.output_file = fp + '_CUSTOMARRAY.txt'
        with open(self.output_file, 'wb') as out_fd:
            for row in self.row_data:
                out_fd.write(row[self.seq_col] + '\t' + row[self.name_col] +
                             '\r\n')
        print 'Output file {} successfully written.'.format(self.output_file)
        self._printStats()


    def _readInXlsx(self):
        wb = openpyxl.load_workbook(self.input_file)
        ws = wb.worksheets[0]
        return [[cell.value for cell in row] for row in ws.rows]


    def _readInDelim(self):
        with open(self.input_file, 'rb') as fd:
            fc = fd.read()
        rows = None
        for nl_delim in ('\r\n', '\n\r', '\r', '\n'):
            if re.search(nl_delim, fc):
                rows = re.split(nl_delim, fc)
                break
        if not rows:
            raise ValueError('Newline delimiter could not be identified, check '
                             'to insure that each record is on a new line')
        return [re.split('[,\t]', row) for row in rows]


    def _dataQC(self):
        '''
        Sort the oligos by name, remove white spaces, rename any duplicates
        '''
        def _extractName(cell):
            return cell[self.name_col]
        # Sort cell list by oligo name and remove blanks
        self.row_data.sort(key=_extractName)
        self.row_data = [cell for cell in self.row_data
                         if len(cell) > 1 and cell[0] != None]
        prev_name = None
        prev_name_count = 0
        for index, cell in enumerate(self.row_data):
            # Remove white space
            cell[self.name_col] = cell[self.name_col].strip()
            cell[self.seq_col] = cell[self.seq_col].strip()
            # Print warning if oligo length is greater than 200 bp
            if len(cell[self.seq_col]) > 170:
                print ('WARNING: oligo {} is >170 bp in length: \n\t[{}bp]-> {}'
                      ''.format(cell[self.name_col], len(cell[self.seq_col]),
                                cell[self.seq_col]))
            # Modify name if oligo name is a duplicate
            if cell[self.name_col] == prev_name:
                prev_name_count += 1
                cell[self.name_col] += '_{}'.format(prev_name_count)
            else:
                prev_name = cell[self.name_col]
                prev_name_count = 0


    def _printStats(self):
        seq_lengths = [len(cell[self.seq_col]) for cell in self.row_data]
        print 'Output file statistics: '
        print '\tNumber of oligos: {}'.format(len(seq_lengths))
        print '\tMax oligo length: {}'.format(max(seq_lengths))
        print '\tMin oligo length: {}'.format(min(seq_lengths))
        print '\tAvg oligo length: {}'.format(sum(seq_lengths)/len(seq_lengths))

    def _reqCol(self, num_cols, msg):
        while True:
            try:
                col = int(raw_input(msg + ': '))
                if col > num_cols:
                    print 'Column number must be > 0 and <= {}'.format(num_cols)
                else:
                    return col - 1
            except TypeError:
                print 'Column number must be an integer'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('input_file', help='Input .xlsx, .csv, or .txt file ' +
                                       'containing oligo names and sequences')
    ap.add_argument('--output_file', '-o',
                    help='Optional output filepath/filename')
    args = ap.parse_args()
    cp = CustomArrayFormatter(args.input_file, args.output_file)
    cp.parseFile()
    cp.writeFile()
