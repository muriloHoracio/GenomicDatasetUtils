import sys

fls = sys.argv[1:]

for fl in fls:
	with open(fl,'r') as f:
		out = ''
		for l in f.readlines():
			out += l
	if len(fl.split('_'))> 1:
		with open(fl.split('_')[1].split('.')[0]+'.fa','w+') as f:
			f.write(out)
