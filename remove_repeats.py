import sys

fls = sys.argv[1:]

repeated = ''
out = ''
seqs = dict()

def check_repeat(fl,header,seq):
	if seq in seqs:
		repeated += fl + '\t' + seqs[fl][seq].strip() + '\t' + fl + '\t' + header.strip() + '\n'
	seqs[seq] = header

for fl in fls:
	with open(fl,'r') as f:
		seq = ''
		for l in fl.readlines():
			if l[0] == '>':
				if seq != '':
					check_repeat(fl,header,seq)
				header = l
				seq = ''
			else:
				seq += l
		check_repeat(fl,header,seq)

for i in range(len(fls)):
	for s in seqs[fls[i]]:
		for j in range(len(fls)):
			if i != j:
				if s in seqs[fls[j]]:
					repeated += fls[i] + '\t' + seqs[fls[i]][s].strip() + '\t' + fls[j] + '\t' + seqs[fls[j]][s].strip() + '\n'
					if len(seqs[fls[i]]) > len(seqs[fls[j]]):
						seqs[fls[i]].pop(s,None)
					else:
						seqs[fls[j]].pop(s,None)

for fl in fls:
	out = ''
	for s in seqs[fl]:
		out += seqs[fl][s] + s
	with open(fl.split('.')[0]+'_UNIQUES.tsv','w+') as f:
		f.write(out)

with open('repeated_list.txt','w+') as f:
	f.write(repeated)
