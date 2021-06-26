import copy
import msvcrt
import colorama
from colorama import Fore, Back, Style
import os
import random
import time

colorama.init()

#pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
#print('%s%s%s%s%s' % (pos(15,10),Fore.WHITE, Back.RED, Style.BRIGHT,"Введите число ваших воинов."), end='')
#a = int(input())
#Ikolvo = a
#print('%s%s%s%s%s' % (pos(15,10),Fore.WHITE, Back.RED, Style.BRIGHT,"Введите число воинов противника."), end='')
#b = int(input())
#enemkolvo = b
#print('%s%s%s%s%s' % (pos(15,10),Fore.WHITE, Back.BLACK, Style.BRIGHT,"                                   "), end='')

maks_hp = 20
maks_force = 20


FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
battlefield = []


def TakeStock(squad):
	i = 0
	for warrior in squad:
		if warrior["hp"] > 0:
			i+=1
	InitSquad(squad,i)


def PrintBattlefield():
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	for i in range(0,20):
		for t in range(0,52):
			print('%s%s%s%s%d' % (pos(i+1,t+1),Fore.RED, Back.BLACK, Style.BRIGHT,battlefield[i][t]["type"]), end='')


def ClearBattlefield():
	battlefield.clear()
	battlefieldpos = {"type":0,"id":-1}
	r = []
	for t in range(0,52):
		r.append(copy.deepcopy(battlefieldpos))
	for i in range(0,21):
		battlefield.append(copy.deepcopy(r))


def PlaceSquad(squad,enemy = False):
	i = 0
	size = len(squad)
	for warrior in squad:
		warrior["x"] = 1+i%20
		if enemy:
			warrior["y"] = 51-(size//20)+(i//20)
			battlefield[warrior["x"]][warrior["y"]]["type"] = 2
			battlefield[warrior["x"]][warrior["y"]]["id"] = i
			
		else:
			warrior["y"] = size//20+1-i//20
			battlefield[warrior["x"]][warrior["y"]]["type"] = 1
			battlefield[warrior["x"]][warrior["y"]]["id"] = i
		i += 1


def InitSquad(squad,kolvo):
	global maks_hp
	global maks_force
	squad.clear()
	for i in range(0,kolvo):
		squad.append({"hp":maks_hp,"x":-1,"y":-1,"force":maks_force})


a_mer = 0
e_mer = 0
ClearBattlefield()
enemies = []
army = []
pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
#enemkolvo = 5
#Ikolvo = 5

#InitSquad(enemies,enemkolvo)
#PlaceSquad(enemies,True)
#InitSquad(army,Ikolvo)
#PlaceSquad(army)
pos = lambda x, y: '\x1b[%d;%dH' % (x, y)

def PrepareBattle(Ikolvo,enemkolvo):
	InitSquad(enemies,enemkolvo)
	PlaceSquad(enemies,True)
	InitSquad(army,Ikolvo)
	PlaceSquad(army)
	BattleBegin(l)

def PrintPlayer(warrior,Enemy = False):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	if warrior["hp"] > 0:
		if Enemy == False:
			print('%s%s%s%s%s' % (pos(warrior["x"],warrior["y"]),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')
		else:
			print('%s%s%s%s%s' % (pos(warrior["x"],warrior["y"]),Fore.RED, Back.BLACK, Style.NORMAL,"2"), end='')


def ClearPlayer(warrior):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(warrior["x"],warrior["y"]),Fore.MAGENTA, Back.BLACK, Style.NORMAL," "), end='')


def warriorTurn(warrior,Enemy=False):
	global a_mer
	global e_mer
	ClearPlayer(warrior)
	Verstep = 1
	step = 1
	type = 1
	opptype = 2
	canMove = True
	if warrior["y"] == 25:
		canMove = False
	if Enemy:
		if warrior["y"] == 26:
			canMove = False
		step = -1
		type = 2
		opptype = 1
	#ХодИгрока
	#Если можем походить вперёд
	if battlefield[warrior["x"]][warrior["y"]+step]["type"] == 0 and canMove:
		battlefield[warrior["x"]][warrior["y"]+step]["type"] = battlefield[warrior["x"]][warrior["y"]]["type"]
		battlefield[warrior["x"]][warrior["y"]+step]["id"] = battlefield[warrior["x"]][warrior["y"]]["id"]
		battlefield[warrior["x"]][warrior["y"]]["type"] = 0
		battlefield[warrior["x"]][warrior["y"]]["id"] = -1
		warrior["y"] += step
	#Если перед нами противник
	elif battlefield[warrior["x"]][warrior["y"]+step]["type"] == opptype:
		if Enemy:
			army[battlefield[warrior["x"]][warrior["y"]+step]["id"]]["hp"] -= random.randint(1,warrior["force"])
			if army[battlefield[warrior["x"]][warrior["y"]+step]["id"]]["hp"] <= 0:
				battlefield[warrior["x"]][warrior["y"]+step]["type"] = 0
				a_mer += 1
				ClearPlayer(army[battlefield[warrior["x"]][warrior["y"]+step]["id"]])
		else:
			enemies[battlefield[warrior["x"]][warrior["y"]+step]["id"]]["hp"] -= random.randint(1,warrior["force"])
			if enemies[battlefield[warrior["x"]][warrior["y"]+step]["id"]]["hp"] <= 0:
				battlefield[warrior["x"]][warrior["y"]+step]["type"] = 0
				e_mer += 1
				ClearPlayer(enemies[battlefield[warrior["x"]][warrior["y"]+step]["id"]])
	else:
		if warrior["x"] > 10:
			Verstep = -1
		if battlefield[warrior["x"]+Verstep][warrior["y"]]["type"] == 0 and warrior["x"]!=10:
			battlefield[warrior["x"]+Verstep][warrior["y"]]["type"] = battlefield[warrior["x"]][warrior["y"]]["type"]
			battlefield[warrior["x"]+Verstep][warrior["y"]]["id"] = battlefield[warrior["x"]][warrior["y"]]["id"]
			battlefield[warrior["x"]][warrior["y"]]["type"] = 0
			battlefield[warrior["x"]][warrior["y"]]["id"] = -1
			warrior["x"] += Verstep
	PrintPlayer(warrior,Enemy)

def BattleBegin(l):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	while a_mer < len(army) and e_mer < len(enemies):
		for warrior in army:
			if warrior["hp"] > 0:
				warriorTurn(warrior)
		pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
		print('%s%s%s%s%s%d%s%s%d%s%s' % (pos(22,10),Fore.GREEN, Back.BLACK, Style.BRIGHT,l['battlemeh_1'],a_mer," ",l['battlemeh_2'],e_mer," ",l['battlemeh_3']), end='')
		time.sleep(0.1)
		for enemy in enemies:
			if enemy["hp"] > 0:
				warriorTurn(enemy,True)
		time.sleep(0.1)
	if e_mer < len(enemies):
		pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
		print('%s%s%s%s%s' % (pos(15,10),Fore.RED, Back.BLACK, Style.BRIGHT,l['battlemeh_4']), end='')
	else:
		pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
		print('%s%s%s%s%s' % (pos(15,10),Fore.GREEN, Back.BLACK, Style.BRIGHT,l['battlemeh_4']), end='')
#PrepareBattle(10,10)