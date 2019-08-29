import os

dbs = [db for db in os.listdir('.') if os.path.isdir(db)]

dic = dict()
repeated = dict()
for db in dbs:
	for fl in [f for f in os.listdir(db) if not os.path.isdir(db+'/'+f)]:
		with open(db+'/'+fl,'r') as f:
			seq = ''
			for l in f.readlines():
				if l[0] == '>':
					if seq != '':
						seq = seq.upper()
						if seq not in dic:
							dic[seq] = [db+'/'+fl, header]
						else:
							print('repeated: '+dic[seq][0]+': '+dic[seq][1].strip()+', '+db+'/'+fl+': '+header.strip())
							if seq not in repeated:
								repeated[seq] = [[db+'/'+fl, header],[dic[seq][0],dic[seq][1]]]
							else:
								repeated[seq].append([db+'/'+fl, header])
					seq = ''
					header = l
				else:
					seq += l
			seq = seq.upper()
			if seq not in dic:
				dic[seq] = [db+'/'+fl, header]
			else:
				print('repeated: '+dic[seq][0]+': '+dic[seq][1].strip()+', '+db+'/'+fl+': '+header.strip())
				if seq not in repeated:
					repeated[seq] = [[db+'/'+fl, header],[dic[seq][0],dic[seq][1]]]
				else:
					repeated[seq].append([db+'/'+fl, header])
