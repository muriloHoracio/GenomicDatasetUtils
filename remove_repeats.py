import os
import sys
import re

clr_seq = re.compile('[^ACGTN\n]')
repeated = ''
out = ''
seqs = dict()

for db in [d for d in os.listdir('.') if os.path.isdir(d)]:
	seqs[db] = dict()
	for fl in [f for f in os.listdir(db) if os.path.isfile(db+'/'+f)]:
		seqs[db][fl] = dict()
		with open(db+'/'+fl,'r') as f:
			seq = ''
			header = ''
			for l in f.readlines():
				if l[0] == '>':
					if seq != '':
						seq = clr_seq.subn('N',seq.upper())[0]
						if seq in seqs[db][fl]:
							repeated += db + '\t' + fl + '\t' + header.strip() + '\t' + db + '\t' + fl + '\t' + seqs[db][fl][seq][0].strip() + '\n'
						seqs[db][fl][seq] = [header, True]
					header = l
					seq = ''
				else:
					seq += l
			seq = clr_seq.subn('N',seq.upper())[0]
			if seq in seqs[db][fl]:
				repeated += db + '\t' + fl + '\t' + header.strip() + '\t' + db + '\t' + fl + '\t' + seqs[db][fl][seq][0].strip() + '\n'
			seqs[db][fl][seq] = [header, True]


for db in seqs:
	for fl in seqs[db]:
		for s in seqs[db][fl]:
			for _db in seqs:
				#for _fl in [f for f in seqs[_db] if f != fl]:
				for _fl in seqs[_db]:
					if not (db == _db and fl == _fl):
						if s in seqs[_db][_fl] and seqs[_db][_fl][s][1]:
							repeated += db + '\t' + fl + '\t' + seqs[db][fl][s][0].strip() + '\t' + _db + '\t' + _fl + '\t' + seqs[_db][_fl][s][0].strip() + '\n'
							if len(seqs[db][fl]) > len(seqs[_db][_fl]):
								seqs[db][fl][s][1] = False
							else:
								seqs[_db][_fl][s][1] = False

for db in seqs:
	for fl in seqs[db]:
		out = ''
		for s in seqs[db][fl]:
			if seqs[db][fl][s][1]:
				out += seqs[db][fl][s][0] + s
		with open(db+'/'+fl.split('.')[0]+'_UNIQUES.fa','w+') as f:
			f.write(out)

with open('repeated_seqs_list.tsv','w+') as f:
	f.write(repeated)

"""
print(len(seqs))
for db in seqs:
	print('\t'+str(len(seqs[db])))
	for fl in seqs[db]:
		print('\t\t'+str(len(seqs[db][fl])))
"""
"""
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
"""
