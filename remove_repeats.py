import os
import sys

repeats = []
dic = dict()
dbs = dict()

for db in [d for d in os.listdir('.') if os.path.isdir(d)]:
	dbs[db] = dict()
	for fl in os.listdir(db):
		dbs[db][fl] = 0
		with open(db+'/'+fl,'r') as f:
			for l in f.readlines():
				if l[0] == '>':
					dbs[db][fl] += 1

for db in dbs:
	print(db)
	for cl in dbs[db]:
		print('\t'+cl+': '+str(dbs[db][cl]))

"""
for fl in fls:
	with open(fl,'r') as f:
		seq = ''
		header = ''
		for l in f.readlines():
			if l[0] == '>':
				if seq != '':
					if seq in dic:
						repeats.append([dic[seq][-1],dic[seq][0],fl,header])
					else:
						dic[seq] = [header, fl]
				seq = ''
				header = l
			else:
				seq += l.upper().strip()
		if seq in dic:
			repeats.append([dic[seq][-1],dic[seq][0],fl,header])

for r in repeats
"""
