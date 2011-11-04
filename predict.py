import numpy, csv, random
import scipy.spatial as spatial
from StringIO import StringIO
from collections import defaultdict

FILENAME = 'data/winestrain2.csv'

reader = csv.reader(open(FILENAME, 'r'), delimiter=',', quotechar='"')

col_names = [ 'name', 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Varietal', 'Country', 'SubRegion', 'Appellation', 'Alcohol' ]
category_cols = [ 'name', 'Varietal', 'Country', 'SubRegion', 'Appellation' ]
num_cols = [ 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Alcohol' ]

def extractData(row):
    for col in col_names:
        pass

data = defaultdict(list)
i = 0
for row in reader:
    if i > 0:
        for i,d in enumerate(row):
            col = col_names[i]
            if d == 'NA':
                d = -1 if col in num_cols else ''
            if col in num_cols:
                try:
                    d = float(d)
                except:
                    print d
            data[ col ].append(d)
    i += 1

for col, vals in data.iteritems():
    print col, len(vals),
    if col in num_cols:
        a = numpy.array(vals)
        new_a = a[a <> -1]
        print numpy.mean(new_a)
    else:
        print 


temp_data = numpy.random.rand(1000,5)
t = spatial.cKDTree(data=temp_data)

for i in range(10):
    vals = numpy.random.rand(5)
    res = t.query( vals )
    print vals, '=>', res, '=>', temp_data[res[1]]