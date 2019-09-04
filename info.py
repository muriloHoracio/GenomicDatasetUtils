import os
import sys

repeats = []
dic = dict()
dbs = dict()

_bases = ["DPTE","PGSB","REPBASE","RiTE","SPTE","TEfam","TREP"]

bases = {
	"DPTE": 0,
	"PGSB": 0,
	"REPBASE": 0,
	"RiTE": 0,
	"SPTE": 0,
	"TEfam": 0,
	"TREP": 0
}

_superfamilies = ["Copia", "Gypsy","Bel-Pao","Retrovirus","ERV","DIRS","Ngaro","VIPER","Penelope","R2","RTE","Jockey","LINE","L1","I","SINE","tRNA","7SL","5S","Mariner","hAT","Mutator","Merlin","Transib","P","PiggyBac","PIF","CACTA","Crypton","Helitron","Maverick","MITE","TRIM"]

superfamilies = {
	"Copia": dict(bases), 
	"Gypsy": dict(bases),
	"Bel-Pao": dict(bases),
	"Retrovirus": dict(bases),
	"ERV": dict(bases),
	"DIRS": dict(bases),
	"Ngaro": dict(bases),
	"VIPER": dict(bases),
	"Penelope": dict(bases),
	"R2": dict(bases),
	"RTE": dict(bases),
	"Jockey": dict(bases),
	"LINE": dict(bases),
	"L1": dict(bases),
	"I": dict(bases),
	"SINE": dict(bases),
	"tRNA": dict(bases),
	"7SL": dict(bases),
	"5S": dict(bases),
	"Mariner": dict(bases),
	"hAT": dict(bases),
	"Mutator": dict(bases),
	"Merlin": dict(bases),
	"Transib": dict(bases),
	"P": dict(bases),
	"PiggyBac": dict(bases),
	"PIF": dict(bases),
	"CACTA": dict(bases),
	"Crypton": dict(bases),
	"Helitron": dict(bases),
	"Maverick": dict(bases),
	"MITE": dict(bases),
	"TRIM": dict(bases)
}

for db in [d for d in os.listdir('.') if os.path.isdir(d)]:
	for fl in os.listdir(db):
		with open(db+'/'+fl,'r') as f:
			for l in f.readlines():
				if l[0] == '>':
					superfamilies[fl.split('.')[0]][db] += 1
header = 'Superfamily'
for db in _bases:
	header += ','+db
header += '\n'

out = ''
for s in _superfamilies:
	out += s
	_sum = 0
	for db in _bases:
		_sum += superfamilies[s][db]
		out += ','+str(superfamilies[s][db])
	out +=','+str(_sum)+'\n'

out = header + out

with open('seqs.csv','w+') as f:
	f.write(out)
