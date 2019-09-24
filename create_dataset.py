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

seqs_sampled = dict()
for c in args.classes:
	seqs_sampled[c] = []
	for db in args.databases:
		if os.path.exists(db+'/'+c+'.fa') and os.path.isfile(db+'/'+c+'.fa'):
			with open(db+'/'+c+'.fa','r') as f:
				seq_counter = 0
				for l in f.readlines():
					if l[0] == '>':
						seqs_sampled[c].append([db,seq_counter])
						seq_counter += 1
	seqs_sampled[c] = np.asarray(seqs_sampled[c])
	if args.train_size + args.test_size > len(seqs_sampled[c]):
		print("ERROR:\tTrain size and test size do not match the amount of sequences across the databases for class "+c)
		exit(-1)
	seqs_sampled[c] = seqs_sampled[c][np.random.choice(len(seqs_sampled[c]), args.train_size + args.test_size, replace=False)]
	_seqs_sampled = sorted(seqs_sampled[c], key=lambda x: x[0])
	seqs_sampled[c] = dict()
	for db in args.databases:
		seqs_sampled[c][db] = []
	for i in _seqs_sampled:
		seqs_sampled[c][i[0]].append(i[1])
	del _seqs_sampled

seqs = dict()
headers = dict()

for c in args.classes:
	seqs[c] = []
	headers[c] = []
	for db in args.databases:
		if os.path.exists(db+'/'+c+'.fa') and os.path.isfile(db+'/'+c+'.fa'):
			with open(db+'/'+c+'.fa','r') as f:
				seq = ''
				header = ''
				seq_counter = -1
				for l in f.readlines():
					if l[0] == '>':
						if seq != '' and str(seq_counter) in seqs_sampled[c][db]:
							seqs[c].append(clr.subn('N',seq.upper())[0])
							headers[c].append(db+'\t'+header)
						seq = ''
						header = l
						seq_counter += 1
					else:
						seq += l
				if str(seq_counter) in seqs_sampled[c][db]:
					seqs[c].append(clr.subn('N',seq.upper())[0])
					headers[c].append(db+'\t'+header)
	out_seqs = ''
	out_headers = ''
	for i in range(args.train_size):
		out_seqs += '>'+headers[c][i].split('>')[-1] + seqs[c][i]
		out_headers += headers[c][i]
	with open(args.dataset_path+'/Train/'+c+'.fa','w+') as f: f.write(out_seqs)
	with open(args.dataset_path+'/Headers/'+c+'_train_headers.txt','w+') as f: f.write(out_headers)

	out_seqs = ''
	out_headers = ''
	for i in range(args.train_size, args.train_size + args.test_size):
		out_seqs += '>'+headers[c][i].split('>')[-1] + seqs[c][i]
		out_headers += headers[c][i]
	with open(args.dataset_path+'/Test/'+c+'.fa','w+') as f: f.write(out_seqs)
	with open(args.dataset_path+'/Headers/'+c+'_test_headers.txt','w+') as f: f.write(out_headers)
