import sys
import os
import re

chunk = int(sys.argv[1])
fls = sys.argv[2:]

cleaner = re.compile('[^ACGTN\n]')
complement = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N'}

for fl in fls:
	if os.path.isfile(fl):
		seqs = []
		seq = ''
		header = ''
		with open(fl,'r') as f:
			for l in f.readlines():
				if l[0] == '>':
					if seq != '':
						seqs.append([header, cleaner.subn('N',seq.upper())[0]])
					seq = ''
					header = l
				else:
					seq += l.strip()
		seqs.append([header, cleaner.subn('N',seq.upper())[0]])
		out = ''
		for seq in seqs:
			out += seq[0][:-1] + ' REVERSED COMPLEMENT\n'
			seq[1] = ''.join(reversed([complement[nucleotide] for nucleotide in seq[1]]))
			out += ''.join([seq[1][i:i+chunk]+'\n' for i in range(0,len(seq[1]),chunk)])
		with open(fl,'a+') as f:
			f.write(out)
