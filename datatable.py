import numpy, csv
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
                            d = self.idx
                            self.idx += 1
                    data[ col ].append(d)
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
                bit_vec = self.data[:,col_idx] == int_val
            else:
                bit_vac = numpy.logical_and(bit_vec, self.data[:,col_idx] == int_val)
        self.data = self.data[bit_vec, :]
        print self.data.shape
    
    def apply(self, fn, col, new_col):
        pass