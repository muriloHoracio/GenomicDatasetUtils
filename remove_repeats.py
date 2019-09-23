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
							repeated += db + '\t' + fl + '\t' + header.strip() + '\t|<>|\t' + db + '\t' + fl + '\t' + seqs[db][fl][seq][0].strip() + '\n'
						seqs[db][fl][seq] = [header, True]
					header = l
					seq = ''
				else:
					seq += l.strip()
			seq = clr_seq.subn('N',seq.upper())[0]
			if seq in seqs[db][fl]:
				repeated += db + '\t' + fl + '\t' + header.strip() + '\t|<>|\t' + db + '\t' + fl + '\t' + seqs[db][fl][seq][0].strip() + '\n'
			seqs[db][fl][seq] = [header, True]

seqs_amount = dict()
for db in seqs:
	seqs_amount[db] = dict()
	for fl in seqs[db]:
		seqs_amount[db][fl] = len(seqs[db][fl])

for db in seqs:
	for fl in seqs[db]:
		for s in seqs[db][fl]:
			for _db in seqs:
				for _fl in seqs[_db]:
					if not (db == _db and fl == _fl):
						if s in seqs[_db][_fl] and seqs[_db][_fl][s][1]:
							repeated += db + '\t' + fl + '\t' + seqs[db][fl][s][0].strip() + '\t|<>|\t' + _db + '\t' + _fl + '\t' + seqs[_db][_fl][s][0].strip() + '\n'
							if seqs_amount[db][fl] > seqs_amount[_db][_fl]:
								seqs[db][fl][s][1] = False
								seqs_amount[db][fl] += -1
							else:
								seqs[_db][_fl][s][1] = False
								seqs_amount[_db][_fl] += -1

for db in seqs:
	for fl in seqs[db]:
		out = ''
		for s in seqs[db][fl]:
			if seqs[db][fl][s][1]:
				out += seqs[db][fl][s][0]
				for chunk in range(0,len(s),60):
					out += s[chunk:chunk+60]
		with open(db+'/'+fl.split('.')[0]+'_UNIQUES.fa','w+') as f:
			f.write(out)

with open('repeated_seqs_list.tsv','w+') as f:
	f.write(repeated)
