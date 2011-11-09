import numpy, csv
import copy as c
from collections import defaultdict

class DataTable:

    def __init__(self, csv_file):
        self.text_to_int_map = {}
        self.int_to_text_map = {}
        self.cols = []
        self.col_map = {}
        self.idx = 0
        self.loadCSVFile(csv_file)
    
    def loadCSVFile(self, csv_file):
        reader = csv.reader(open(csv_file, 'r'), delimiter=',', quotechar='"')
        header = None
        numeric_cols = set()
        non_numeric_cols = set()
        non_numeric_cols.add('year')
        data = defaultdict(list)
        for row in reader:
            if header is None:
                header = row
            else:
                for i,d in enumerate(row):
                    col = header[i]
                    if d == 'NA':
                        d = None #-1 if col in num_cols else ''
                    if d is not None and col not in non_numeric_cols:
                        try:
                            d = float(d)
                        except:
                            non_numeric_cols.add(col)
                    if col in non_numeric_cols:
                        if d in self.text_to_int_map:
                            d = self.text_to_int_map[d]
                        else:
                            self.text_to_int_map[d] = self.idx
                            self.int_to_text_map[self.idx] = d
                            d = self.idx
                            self.idx += 1
                    data[ col ].append(d)
        self.non_numeric_cols = non_numeric_cols
        for col in header:
            self.cols.append(col)
            self.col_map[col] = 'Text' if col in non_numeric_cols else 'Numeric'
        # Create the numpy table
        a = numpy.zeros( (len( data[header[0]] ), len(header)) )
        print a.shape
        for i,col in enumerate(self.cols):
            a[:,i] = numpy.array( data[col] )
        self.data = a
    
    def filter(self, filter_map):
        print 'Filtering to', filter_map
        bit_vec = None
        for key, val in filter_map.iteritems():
            col_idx = self.cols.index(key)
            int_val = self.text_to_int_map[val]
            if bit_vec is None:
                bit_vec = (self.data[:,col_idx] == int_val)
            else:
                bit_vec = numpy.logical_and(bit_vec, self.data[:,col_idx] == int_val)
        self.data = self.data[bit_vec, :]
        print self.data.shape
    
    def apply(self, fn, col, new_col, is_numeric):
        self.cols.append(new_col)
        col_idx = self.cols.index(col)
        if col in self.non_numeric_cols:
            source_vals = [ self.int_to_text_map[x] for x in self.data[:,col_idx] ]
        else:
            source_vals = [ x for x in self.data[:,col_idx] ]
        vals = map(fn, source_vals)
        if not is_numeric:
            new_vals = []
            for val in vals:
                if val in self.text_to_int_map:
                    d = self.text_to_int_map[val]
                else:
                    self.text_to_int_map[val] = self.idx
                    self.int_to_text_map[self.idx] = val
                    d = self.idx
                    self.idx += 1
                new_vals.append(d)
            self.data = numpy.column_stack( [ self.data, new_vals ] )
        else:
            self.data = numpy.column_stack( [ self.data, vals ] )
        print self.data.shape

    def copy(self):
        return c.deepcopy(self)

    def printInfo(self):
        print self.data.shape

    def getCol(self, col):
        col_idx = self.cols.index(col)
        if col in self.non_numeric_cols:
            return [ self.int_to_text_map[x] for x in self.data[:,col_idx] ]
        else:
            return c.deepcopy(self.data[:, col_idx])
    
    def summarize(self, cols):
        col_idxs = [self.cols.index(col) for col in cols]
        