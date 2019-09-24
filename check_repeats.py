import os
import sys

root = sys.argv[1]

dic = dict()
count = 0

for folder in [fld for fld in os.listdir(root) if os.path.isdir(root+'/'+fld) and fld != 'Headers']:
	for fl in [_file for _file in os.listdir(root+'/'+folder) if os.path.isfile(root+'/'+folder+'/'+_file)]:
		with open(root+'/'+folder+'/'+fl, 'r') as f:
			seq = ''
			header = ''
			for l in f.readlines():
				if l[0] == '>':
					if seq != '':
						seq = seq.upper()
						if seq in dic:
							print('Repeat found: \n\t'+folder+'\t'+fl+'\t'+header+'\t'+'\t'.join(dic[seq]))
							count += 1
						else:
							dic[seq] = [folder, fl, header]
					seq = ''
					header = l
				else:
					seq += l.strip()
			seq = seq.upper()
			if seq in dic:
				print('Repeat found: \n\t'+folder+'\t'+fl+'\t'+header+'\t'+'\t'.join(dic[seq]))
				count += 1
			dic[seq] = header

print(str(len(dic))+' UNIQUE SEQUENCES FOUND')
print(str(count)+' REPEATS FOUND!')
