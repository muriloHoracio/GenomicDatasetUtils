import os
import sys
import re
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-c', dest='classes', metavar='C', type=str, nargs='+', help='Classes that should compose the train and test sets. classes should be the name of the files that represent the class through the database folders, without extension. Exp: -c Copia Gypsy Bel-Pao. In each database that has these classes\' sequences, there should be the files Copia.fa, Gypsy.fa and Bel-Pao.fa')
parser.add_argument('-db', dest='databases', metavar='DBs', type=str, nargs='+', help='Databases that should compose the train and test sets. Each database folder should contain the classes\' files. Exp: DPTE REPBASE PGSB')
parser.add_argument('-tr', dest='train_size', metavar='train_size', type=int, help='Amount of sequences for each superfamily in the train set')
parser.add_argument('-ts', dest='test_size', metavar='test_size', type=int, help='Amount of sequences for each superfamily in the test set')
parser.add_argument('-ds', dest='dataset_path', metavar='dataset', type=str, help='Path to store the train and test sets')

args = parser.parse_args()

print('Superfamilies: '+' '.join(args.classes))
print('Databases: '+' '.join(args.databases))
print('Train set size: '+str(args.train_size))
print('Test set size: '+str(args.test_size))
print('Dataset path: '+args.dataset_path)

if not os.path.exists(args.dataset_path):
	os.mkdir(args.dataset_path)
	if not os.path.exists(args.dataset_path+'/Train'):
		os.mkdir(args.dataset_path+'/Train')
	if not os.path.exists(args.dataset_path+'/Test'):
		os.mkdir(args.dataset_path+'/Test')
	if not os.path.exists(args.dataset_path+'/Headers'):
		os.mkdir(args.dataset_path+'/Headers')

clr = re.compile('[^ACGTN\n]')

for s in args.classes:
	seqs = []
	for db in args.databases:
		if os.path.exists(db+'/'+s+'.fa') and os.path.isfile(db+'/'+s+'.fa'):
			with open(db+'/'+s+'.fa','r') as f:
				seq = ''
				for l in f.readlines():
					if l[0] == '>':
						if seq != '':
							seqs[-1][1] = clr.subn('N',seq.upper())[0]
						seqs.append([l,''])
						seq = ''
					else:
						seq += l
				seqs[-1][1] = clr.subn('N',seq.upper())[0]
	seqs = np.asarray(seqs)
	samples = np.random.choice(len(seqs), args.train_size + args.test_size if len(seqs) > args.train_size + args.test_size else len(seqs), replace=False)
	train = seqs[samples[:args.train_size]]
	test = seqs[samples[args.train_size:]]

	if len(train) > 1:
		out = ''
		headers = ''
		for t in train:
			out += t[0]+t[1]
			headers += t[0]
		with open(args.dataset_path+'/Train/'+s+'.fa','w+') as f: f.write(out)
		with open(args.dataset_path+'/Headers/'+s+'_Train_Headers.fa','w+') as f: f.write(headers)

	if len(test) > 1:
		out = ''
		headers = ''
		for t in test:
			out += t[0]+t[1]
			headers += t[0]
		with open(args.dataset_path+'/Test/'+s+'.fa','w+') as f: f.write(out)
		with open(args.dataset_path+'/Headers/'+s+'_Test_Headers.fa','w+') as f: f.write(headers)

"""
for fl in fls:
	with open(fl,'r') as f:
		_seqs = []
		for l in f.readlines():
			if l[0] == '>':
				if seq != '':
					_seqs[-1][1] = clr.subn('N',seq.upper())[0]
				_seqs.append([l,''])
				seq = ''
			else:
				seq += l		
"""
