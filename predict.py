import numpy, scipy, csv
from StringIO import StringIO
from collections import defaultdict

FILENAME = 'data/winestrain2.csv'

#types = (('name', '|S137'), ('year', '<i4'), ('price', '<f8'), ('WS', '<i4'), ('RP', '<i4'), ('ST', '<i4'), ('WE', '<i4'), ('CG', '<i4'), ('GR', '<i4'), ('WN', '<i4'), ('BH', '<i4'), ('WS_1', '<i4'), ('Varietal', '|S31'), ('Country', '|S15'), ('SubRegion', '|S23'), ('Appellation', '|S32'), ('Alcohol', '<f8'))

col_names = ['name', 'year', 'price', 'WS', 'RP', 'ST', 'WE', 'CG', 'GR', 'WN', 'BH', 'WS1', 'Varietal', 'Country', 'SubRegion', 'Appellation', 'Alcohol' ]

data = numpy.genfromtxt(FILENAME, delimiter=',', skip_header=1, comments='\\',# missing_values='NA',
	names = col_names,
	dtype = ['|S200', '<i4', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '<f8', '|S40', '|S40', '|S40', '|S40', '<f8'],
	)

print data.shape

#final_data = numpy.zeros((data.shape[0],len(col_names)))

#for r_idx,d in enumerate(data):
#	for c_idx,x in enumerate(col_names):
#		final_data[r_idx,c_idx] = d[c_idx]

#print final_data

#print data[:10]

#print a