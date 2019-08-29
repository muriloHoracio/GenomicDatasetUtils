import sys

fls = sys.argv[1:]

repeated = ''
out = ''
seqs = dict()

for fl in fls:
	with open(fl,'r') as f:
		seqs[fl] = dict()
		seq = ''
		for l in f.readlines():
			if l[0] == '>':
				if seq != '':
					seq = seq.upper()
					if seq in seqs:
						repeated += fl + '\t' + seqs[fl][seq][0].strip() + '\t' + fl + '\t' + header.strip() + '\n'
					seqs[fl][seq] = [header, True]
				header = l
				seq = ''
			else:
				seq += l
		seq = seq.upper()
		if seq in seqs:
			repeated += fl + '\t' + seqs[fl][seq][0].strip() + '\t' + fl + '\t' + header.strip() + '\n'
		seqs[fl][seq] = [header, True]

for i in range(len(fls)):
	for s in seqs[fls[i]]:
		for j in range(len(fls)):
			if i != j:
				if s in seqs[fls[j]]:
					repeated += fls[i] + '\t' + seqs[fls[i]][s][0].strip() + '\t' + fls[j] + '\t' + seqs[fls[j]][s][0].strip() + '\n'
					if len(seqs[fls[i]]) > len(seqs[fls[j]]):
						seqs[fls[i]][s][1] = False
					else:
						seqs[fls[j]][s][1] = False

for fl in fls:
	out = ''
	for s in seqs[fl]:
		if seqs[fl][s][1] == True:
			out += seqs[fl][s][0] + s
	with open(fl.split('.')[0]+'_UNIQUES.tsv','w+') as f:
		f.write(out)

with open('repeated_list.txt','w+') as f:
	f.write(repeated)
