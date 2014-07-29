'''
Tools to facilitate manual Custom Array chip layout.

'''

import random

import numpy as np


CHIP_DIMENSIONS = {
    '12K': (54, 224),
    '90K': (272, 349)
}


def getElectrodePosition(electrode_num, chip_type='12K'):
    ''' Returns the electrode position (row, col) given the electrode number
    '''
    chip_rows, chip_cols = CHIP_DIMENSIONS[chip_type]
    col = electrode_num / chip_rows
    row = electrode_num % chip_rows
    return row, col


def getElectrodeNumber(row, col):
    ''' Returns the electrode number given its position (row, col)
    '''
    return row * col


class Oligo:

    def __init__(self, name, sequence, replicates=1, notes=''):
        self.name = name
        self.seq = sequence
        self.electrode_idxs = []
        self.notes = notes

# XML headers

xml_headers = '''
<?xml version="1.0" encoding="UTF-8"?>
<chipDesign version="2_6" docState="Submission" xmlns="urn:probe-design-service">
  <chipDesignInfo detectionType="EMPTY" xmlns="urn:probe-design-service">
    <elementCount count="{element_count}">
      <oligoCount count="{oligo_count}" targetCount="0" backgroundClusterCount="0" probeCount="{oligo_count}"/>
      <layoutCount count="{oligo_count}">
        <microarrayListLength count="{oligo_count}" length="1">
          <probeAssignmentCount count="{oligo_count}"/>
        </microarrayListLength>
      </layoutCount>
    </elementCount>
    <microarrayInfo type="12k"/>
  </chipDesignInfo>
<changeHistory xmlns="urn:probe-design-service">
</changeHistory>
'''

# values to provide
# element_count = 2x number of oligos
# oligo_count = # of oligos

class ChipLayout:

    def __init__(self, chip_type='12K', mask_corners=True):
        assert chip_type in CHIP_DIMENSIONS.keys()
        self.type = chip_type
        self.dims = CHIP_DIMENSIONS[chip_type]
        self.array = np.zeros(self.dims)
        self.oligos = []
        self.oligo_names = []
        self.array[:] = -1
        if mask_corners:
            self.maskCorners()

    def availableElectrodes(self):
        return sum(sum(self.array == -1))

    def usedElectrodes(self, include_masked=False):
        if not include_masked:
            used_electrodes = sum(sum(self.array > -1))
        else:
            used_electrodes = sum(sum(self.array != 0))

    def maskCorners(self):
        self.maskElectrodes(None, 4, None, 4)       # Top left
        self.maskElectrodes(-4, None, None, 4)      # Bottom left
        self.maskElectrodes(None, 4, -4, None)      # Top right
        self.maskElectrodes(-4, None, -4, None)     # Bottom right

    def maskElectrodes(self, row_start=None, row_end=None, col_start=None,
                       col_end=None):
        self.array[row_start:row_end, col_start:col_end] = -2

    def addOligo(self, name, sequence, replicates=1, notes='',
                 random_placement=False):
        if self.availableElectrodes() < replicates:
            raise ValueError('Array is too full to fit oligo {} with {} '
                             'replicates'.format(name, replicates))
        if name in self.oligo_names:
            raise ValueError('Duplicate oligo name: {}'.format(name))
        o = Oligo(name, sequence, replicates, notes)
        self.oligos.append(o)
        self.oligo_names.append(name)
        oligo_arr_idx = len(self.oligos) - 1
        num_populated = 0

        if random_placement:
            row_max = self.dims[0] - 1
            col_max = self.dims[1] - 1
            while num_populated < replicates:
                row_idx = random.randint(0, row_max)
                col_idx = random.randint(0, col_max)
                if self.array[row_idx, col_idx] == -1:
                    self.array[row_idx, col_idx] = oligo_arr_idx
                    o.electrode_idxs.append(row_idx * col_idx)
                    num_populated += 1
        else:
            finished = False
            for row_idx, row in enumerate(self.array):
                if finished:
                    break
                for col_idx, electrode in enumerate(row):
                    if num_populated == replicates:
                        finished = True
                        break
                    if electrode == -1:
                        row[col_idx] = oligo_arr_idx
                        o.electrode_idxs.append(row_idx * col_idx)
                        num_populated += 1

    def writeXML(self, fn, fp=None):


cl = ChipLayout()
print cl.availableElectrodes()
cl.addOligo('test', 'ATGC', replicates=12000, random_placement=True)
print cl.availableElectrodes()
print cl.oligo_names
