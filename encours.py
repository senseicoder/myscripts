import re
from enum import Enum

pathEncours = "/home/cedric/Sync/Central/Dossiers/Suivis/encours.txt"

rexTitre = re.compile('^[ A-Z]+$')
rexDone = re.compile('^DONE [0-9]{4}-[0-9]{2}-[0-9]{2}.*')
rexKifs = re.compile('^KIFS.*[0-9]{4}-[0-9]{2}-[0-9]{2}.*')
rexVide = re.compile('^$')
rexTask = re.compile('^KIFS.*[0-9]{4}-[0-9]{2}-[0-9]{2}.*')
rexComment = re.compile('^\t.*')

class NL(Enum):
	INCONNUE = 0
	TITRE = 1
	DONE = 2
	KIFS = 3
	VIDE = 4
	TASK = 5
	COMMENT = 6

with open(pathEncours) as handle:
	for line in handle:
		line = line.strip()

		nature = NL.INCONNUE
		if rexTitre.match(line):
			print(">>" + line + ">>")
		elif rexDone.match(line):
			print("<<" + line + "<<")
		elif rexKifs.match(line):
			print("++" + line + "++")
		#else:	
		#	print("::" + line.strip() + "::")
