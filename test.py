import sys
import os

bases = {
	"DPTE": 0,
	"PGSB": 0,
	"REPBASE": 0,
	"RiTE": 0,
	"SPTE": 0,
	"TEfam": 0,
	"TREP": 0
	}

superfamilies = {
	"Copia": dict(bases),
	"Gypsy": dict(bases),
	"ERV": dict(bases),
	"Bel-Pao": dict(bases)
	}

superfamilies["Copia"]["DPTE"] = 10
superfamilies["Gypsy"]["DPTE"] = 100

print(str(superfamilies["Copia"]))
print(str(superfamilies["Gypsy"]))
