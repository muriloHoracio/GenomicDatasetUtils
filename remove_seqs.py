import sys

l = sys.argv[1]
fls = sys.argv[2:]

remove_headers = dict()
with open(l,'r') as f:
	for l in f.readlines():
		remove_headers[l] = 0

for fl in fls:
	with open(fl,'r') as f:
		seq = ''
		header = ''
		out = ''
		for l in f.readlines():
			if l[0]=='>':
				if seq != '':
					if header not in remove_headers:
						out += header
						out += seq.upper()
				seq = ''
				header = l
			else:
				seq += l
		if header not in remove_headers:
			out += header
			out += seq.upper()

	with open(fl.split('.')[0]+'_UNIQUES.fa','w+') as f:
		f.write(out)
