import re
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
	return switcher.get(nature, "invalid NL for switchOut")

def switchBlock():
	global nature
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
	return switcher.get(nature, "invalid NL for switchBlock")

def switchTask():
	global nature
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
	return switcher.get(nature, "invalid NL for switchTask")

def switchComment():
	global nature
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
	return switcher.get(nature, "invalid NL for switchTask")

def switchErr():
	print('erreur execution')

aBlocks = {}
oBlock = {}

state = ST.OUT
prevstate = ST.OUT
with open(pathEncours) as handle:
	for line in handle:
		#line = line.rstrip()

		nature = NL.INCONNUE
		if rexTitre.match(line): nature = NL.TITRE
		elif rexDone.match(line): nature = NL.DONE
		elif rexKifs.match(line): nature = NL.KIFS
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

