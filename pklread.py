#!/usr/bin/env python
# encoding: utf-8

import pprint, pickle
import sys

pklfile = sys.argv
#print pklfile
#pkl = raw_input()
pkl_file = open(pklfile[1], 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()
