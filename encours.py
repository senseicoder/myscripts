#TODO
#extraire la date
#prendre des params
#lister les blocs
#extraire kifs et done dans des fichiers archives (sauf ceux du jour)
#pouvoir retrier un bloc quelconque vers prj (comme un fichier texte)
#pouvoir retrier un bloc quelconque vers les autres blocs

import re
import pprint
pp = pprint.PrettyPrinter(indent=1)
from enum import Enum

pathEncours = "/home/cedric/Sync/Central/Dossiers/Suivis/encours.txt"

rexTitre = re.compile(r'^[ A-Z0-9]+$')
rexDone = re.compile(r'^DONE [0-9]{4}-[0-9]{2}-[0-9]{2}.*')
rexKifs = re.compile(r'^KIFS.*[0-9]{4}-[0-9]{2}-[0-9]{2}.*')
rexVide = re.compile(r'^$')
rexTask = re.compile(r'^.+$')
rexComment = re.compile(r'^[\t].*')
rexRems = re.compile(r'^#.*')

class MyEnum(Enum):
	def __repr__(self):
		return '%s.%s' % (self.__class__.__name__, self.name)

class NL(MyEnum):
	INCONNUE = 0
	TITRE = 1
	DONE = 2
	KIFS = 3
	VIDE = 4
	TASK = 5
	COMMENT = 6
	REMS = 7

class ST(MyEnum):
	OUT = 0
	BLOCK = 1
	TASK = 2
	ERR = 3
	COMMENT = 4

def switchOut():
	global nature
	global aBlocks
	global idBlock
	global idTask

	switcher={
		NL.INCONNUE: 	ST.ERR,
		NL.TITRE: 		ST.BLOCK,
		NL.DONE: 		ST.BLOCK,
		NL.KIFS: 		ST.BLOCK,
		NL.VIDE: 		ST.OUT,
		NL.TASK: 		ST.ERR,
		NL.COMMENT: 	ST.ERR,
		NL.REMS:		ST.OUT
	}
	result = switcher.get(nature, "invalid NL for switchOut")
	if(result == ST.BLOCK):
		aBlocks.append({'titre': line, 'nature': nature, 'tasks': []})
		idBlock = len(aBlocks) - 1
	return result

def switchBlock():
	global nature
	global aBlocks
	global idBlock
	global idTask

	switcher={
		NL.INCONNUE: 	ST.ERR,
		NL.TITRE: 		ST.TASK,
		NL.DONE: 		ST.TASK,
		NL.KIFS: 		ST.TASK,
		NL.VIDE: 		ST.OUT,
		NL.TASK: 		ST.TASK,
		NL.COMMENT: 	ST.ERR,
		NL.REMS:		ST.BLOCK
	}
	result = switcher.get(nature, "invalid NL for switchBlock")
	if(result == ST.TASK):
		aBlocks[idBlock]['tasks'].append({'task': line, 'comments': []})
		idTask = -1
	return result

def switchTask():
	global nature
	global aBlocks
	global idBlock
	global idTask

	switcher={
		NL.INCONNUE: 	ST.ERR,
		NL.TITRE: 		ST.TASK,
		NL.DONE: 		ST.TASK,
		NL.KIFS: 		ST.TASK,
		NL.VIDE: 		ST.OUT,
		NL.TASK: 		ST.TASK,
		NL.COMMENT: 	ST.COMMENT,
		NL.REMS:		ST.TASK
	}
	result = switcher.get(nature, "invalid NL for switchTask")
	if(result == ST.TASK):
		aBlocks[idBlock]['tasks'].append({'task': line, 'comments': []})
		idTask = len(aBlocks[idBlock]['tasks']) - 1
		print("idTask+ " + str(idTask))
	if(result == ST.COMMENT):
		print("idTask cmt " + str(idTask))
		aBlocks[idBlock]['tasks'][idTask]['comments'].append(line)
	return result

def switchComment():
	global nature
	global aBlocks
	global idBlock
	global idTask

	switcher={
		NL.INCONNUE: 	ST.ERR,
		NL.TITRE: 		ST.TASK,
		NL.DONE: 		ST.TASK,
		NL.KIFS: 		ST.TASK,
		NL.VIDE: 		ST.OUT,
		NL.TASK: 		ST.TASK,
		NL.COMMENT: 	ST.COMMENT,
		NL.REMS:		ST.COMMENT
	}
	result = switcher.get(nature, "invalid NL for switchTask")
	if(result == ST.TASK):
		aBlocks[idBlock]['tasks'].append({'task': line, 'comments': []})
	if(result == ST.COMMENT):
		aBlocks[idBlock]['tasks'][idTask]['comments'].append(line)
		idTask = len(aBlocks[idBlock]['tasks']) - 1
	return result

def switchErr():
	print('erreur execution')

print("init")
aBlocks = []
idBlock = -1
idTask = -1

state = ST.OUT
prevstate = ST.OUT
with open(pathEncours) as handle:
	for line in handle:
		nature = NL.INCONNUE
		if rexDone.match(line): nature = NL.DONE
		elif rexKifs.match(line): nature = NL.KIFS
		elif rexTitre.match(line): nature = NL.TITRE
		elif rexVide.match(line): nature = NL.VIDE
		elif rexComment.match(line): nature = NL.COMMENT
		elif rexRems.match(line): nature = NL.REMS
		elif rexTask.match(line): nature = NL.TASK

		switcher = {
			ST.OUT: switchOut,
			ST.BLOCK: switchBlock,
			ST.TASK: switchTask,
			ST.COMMENT: switchComment,
			ST.ERR: switchErr
		}
		func = switcher.get(state)
		prevstate = state
		state = func()

		print(repr(nature) + ' (' + repr(prevstate) + '=>' + repr(state) + '): ' + line.rstrip())

#print(aBlocks)
#pp.pprint(aBlocks[1])
#pp.pprint(aBlocks[8])
pp.pprint(aBlocks[15])