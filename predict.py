import numpy, scipy, csv
from StringIO import StringIO
from collections import defaultdict

FILENAME = 'data/winestrain2.csv'

reader = csv.reader(open(FILENAME, 'r'), delimiter=',', quotechar='"')

col_names = [ 'name', 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Varietal', 'Country', 'SubRegion', 'Appellation', 'Alcohol' ]
category_cols = [ 'name', 'Varietal', 'Country', 'SubRegion', 'Appellation' ]
num_cols = [ 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Alcohol' ]

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
    print col, len(vals)
    if col in num_cols:
        a = numpy.array(vals)
        new_a = a[a <> -1]
        print numpy.mean(new_a)