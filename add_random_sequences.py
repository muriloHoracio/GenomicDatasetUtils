import sys
import os
import re
import numpy as np

cleaner = re.compile('[^ACGTN\n]')

random_seqs_n = int(sys.argv[1])
chunk = int(sys.argv[2])
root_dir = sys.argv[3]
if not os.path.isdir(root_dir):
	print('ERROR!\n\nThe specified root directory does not exist. Please run again with a valid root directory.')
	exit(-1)

fls = [root_dir+'/'+fl for fl in os.listdir(root_dir) if os.path.isfile(root_dir+'/'+fl) and fl.split('.')[-1].upper() in ['FA','FASTA']]

if len(fls) == 0:
	print('ERROR!\n\nThe specified root directory does not contain any FASTA file. Please run again with a valid root directory.')
	exit(-2)

seqs = []
for fl in fls:
	seq = ''
	with open(fl,'r') as f:
		for l in f.readlines():
			if l[0] == '>':
				if seq != '':
					seqs.append(cleaner.subn('N',seq.upper())[0])
				seq = ''
			else:
				seq += l.strip()
		seqs.append(cleaner.subn('N',seq.upper())[0])
out = ''
for i, index in enumerate(np.random.choice(len(seqs),random_seqs_n,replace=False)):
	out += '>RANDOM '+str(i)+'\n'
	seq = ''.join([seqs[index][j] for j in np.random.permutation(len(seqs[index]))])
	out += ''.join([seq[j:j+chunk]+'\n' for j in range(0,len(seq),chunk)])
with open(root_dir+'/Random.fa','w+') as f:
	f.write(out)
