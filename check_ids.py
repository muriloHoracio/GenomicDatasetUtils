import sys
fls = sys.argv[1:]

for fl in fls:
	ids = dict()
	with open(fl,'r') as f:
		for l in f.readlines():
			if l[0] == '>':
				if l in ids:
					print('repeated header: '+l)
				else:
					ids[l] = 0
		print(fl+': '+str(len(ids)))
