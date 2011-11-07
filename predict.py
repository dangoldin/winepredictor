import numpy, csv, random
import scipy.spatial as spatial
from StringIO import StringIO
from collections import defaultdict

FILENAME = 'data/winestrain2.csv'

reader = csv.reader(open(FILENAME, 'r'), delimiter=',', quotechar='"')

col_names = [ 'name', 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Varietal', 'Country', 'SubRegion', 'Appellation', 'Alcohol' ]
category_cols = [ 'year', 'Varietal', 'Country', 'SubRegion', 'Appellation' ]
num_cols = [ 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Alcohol' ]

def parseName(name):
    sizes = ['187mL', '375mL', '375 mL', '500mL', '500 mL', '1.5L', '1.5 L', '3L', '3 L', '5L', '5 L', '6L', '6 L',]
    print name

def getSummaryStats(data):
    summary_vals = defaultdict(list)
    cnt = len(data['name'])
    for i in range(cnt):
        key = "|".join([data[c][i] for c in category_cols])
        summary_vals[key].append( data['price'][i] )
    for key, vals in summary_vals.iteritems():
        a = numpy.array(vals)
        print key,':',numpy.mean(a),numpy.std(a),len(vals)
    return summary_vals

def extractData(row):
    for i,d in enumerate(row):
        print d

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
                    print 
            if col == 'name':
                parseName(d)
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

print 'Summary Stats'
getSummaryStats(data)

exit()

temp_data = numpy.random.rand(1000,5)
t = spatial.cKDTree(data=temp_data)

for i in range(10):
    vals = numpy.random.rand(5)
    res = t.query( vals )
    print vals, '=>', res, '=>', temp_data[res[1]]