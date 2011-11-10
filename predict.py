import numpy, csv, random
import scipy.spatial as spatial
from StringIO import StringIO
from collections import defaultdict
from datatable import DataTable

FILENAME = 'data/winestrain2.csv'

reader = csv.reader(open(FILENAME, 'r'), delimiter=',', quotechar='"')

col_names = [ 'name', 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Varietal', 'Country', 'SubRegion', 'Appellation', 'Alcohol' ]
category_cols = [ 'year', 'Varietal', 'Country', 'SubRegion', 'Appellation' ]
num_cols = [ 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Alcohol' ]

def getSize(name):
    sizes = {'187mL' : 187,
             '375mL' : 375,
             '375 mL' : 375,
             '500mL' : 500,
             '500 mL' : 500,
             '750 mL' : 750,
             '750mL' : 750,
             '1.5L' : 1500,
             '1.5 L' : 1500,
             '3L' : 3000,
             '3 L' : 3000,
             '5L' : 5000,
             '5 L' : 5000,
             '6L' : 6000,
             '6 L' : 6000}
    for s, size in sizes.iteritems():
        if s in name:
            return str(size)
    return '750'
        
def getSummaryStats(data):
    summary_vals = defaultdict(list)
    cnt = len(data['name'])
    for i in range(cnt):
        key = "|".join([data[c][i] for c in category_cols])
        summary_vals[key].append( data['price'][i] )
    for key, vals in summary_vals.iteritems():
        a = numpy.array(vals)
        #print key,':',numpy.mean(a),numpy.std(a),len(vals)
    return summary_vals

dt = DataTable(FILENAME)
dt.apply( getSize, 'name', 'size', False)
dt.shuffle()

dt_train = dt.copy()
dt_train.split(0.75, True)

dt_test = dt.copy()
dt_test.split(0.75, False)

years = set(dt_train.getCol('year'))
varietals = set(dt_train.getCol('Varietal'))
countries = set(dt_train.getCol('Country'))
subregions = set(dt_train.getCol('SubRegion'))
appellations = set(dt_train.getCol('Appellation'))
sizes = set(dt_train.getCol('size'))

summary = dt_train.summarize( category_cols + ['size'], 'price' )

rows,cols = dt_test.dims()

diffs = []
vals1 = []
for i in range(rows):
    row = dt_test.getRow(i)
    key = tuple( [row[x] for x in category_cols + ['size']] )
    if key in summary:
        guess = summary[key][1]
    else:
        vals1.append(row['price'])
        guess = 92.0
    diffs.append(abs(guess - row['price']))

#print diffs
    
print 'Avg L1:', numpy.mean(diffs)

print 'Random avg:', numpy.mean(vals1), len(vals1)
    
exit()

"""
summary_info = {}
for year in years:
    for varietal in varietals:
        for country in countries:
            for subregion in subregions:
                for appellation in appellations:
                    dt_tmp = dt.copy()
                    dt_tmp.filter( {'year': year,
                                    'Varietal': varietal,
                                    'Country': country,
                                    'SubRegion': subregion,
                                    'Appellation': appellation,
                                    })
                    prices = dt_tmp.getCol('price')
                    summary_info[ (year, varietal, country, subregion, appellation) ] = ( len(prices), numpy.mean(prices), numpy.std(prices) )
                    #print 'Year: %s, %d, %f, %f' % (year, len(prices), numpy.mean(prices), numpy.std(prices))

print summary_info

#dt.filter( { 'Appellation': 'Napa Valley' } )
#dt.apply( firstChar, 'name', 'first_char', False)
#d = dt.copy()

exit()
        
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

dt = DataTable(data)

dt.filter( { 'Appellation': 'Napa Valley' } )



exit()
    
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
"""