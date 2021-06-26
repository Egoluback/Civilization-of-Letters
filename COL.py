import copy
import msvcrt
import colorama
from colorama import Fore, Back, Style
import os
import random
import linecache
import time
import Battle.Battlemeh2
from Battle.Battlemeh2 import *
import Stell.stell2
from Stell.stell2 import *

clear = lambda: os.system('cls')

# стоимости постройки строений в городе, города и воинов
costs = {'barrack':{'tree':10,"resources":130,"credit":600},
'market':{'tree':15,"resources":110,"credit":1000},
'mine':{'tree':5,"resources":0,"credit":500},
'port':{'tree':15,"resources":150,"credit":2000},
'sawmill':{'tree':5,"resources":110,"credit":500}}
towncost = 2000
restowncost = 200
treetowncost = 30
warriorcost = 5
flagcost = 5000
flagtreecost = 40
lvl = 0
ver = open("activeversion.txt","r")
ver2 = ver.read()
version = ver2
ver.close()
SetMoneyCheat = 0
SetArmyCheat = 0
SetResCheat = 0
SetProgressCheat = 0
SetTreeCheat = 0
Cheat = False
CheckCheat = 0
itslow = False
slow = 0

# флаг нахождения в море
Insea = False

# Начальное состояние королевства
kingdom = {'credit':3000,'citys':0,'army':100,'resources':350,"warriors":0,"trees":100,"flags":0}


# дней до окончания игры
days = 300

# Символы для описания мира
waterchr = "~"
plainchr = ","
townchr = "#"
flagchr = "F"
treechr = "Y"
chestchr = "M"
slowchr = "T"

# шаблоны структур данных
city = {"owner":-1,"x":0,"y":0,"barrack":0,"market":0,"port":0,"mine":0,"sawmill":0,"Name":None,}
flag = {"x":0,"y":0,}
enemy = {"x":0,"y":0,"army":0,"fortune":0}

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
towns = []
flags = []
Error = ""
world = []
enemies = []
disableactivecheat = False
shippos = {'x':-1,'y':-1}
ppos = {'x':0,'y':0}
language = "english"
localize = {}
itsan = False

# Инициализация цветов для ascii графики
colorama.init()

# #-город; ,-равнина; Y-дерево; ~-вода;
# 7 8 9	 \ | /
# 4 5 6	 - a -
# 1 2 3	 / | \

#локализация
def localization():
	if language == "russian":
		local = open("rus.txt","r")
	elif language == "english":
		local = open("en.txt","r")
	ll = local.readlines()
	ll = [lin.rstrip() for lin in ll]
	for line in ll:
		l = line.split(':')
		localize.update({l[0]:l[1]})
		#print(localize)
		#input()
	local.close()
		#localize = [line.rstrip() for line in localize]
		#print(localize)
		#input()

#функция для очистки экрана
def ClearFullScreen():
	pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
	for i in range(0,10):
		for g in range(0,50):
			print('%s%s%s%s%s' % (pos(i,g),Fore.RED, Back.BLACK, Style.NORMAL,"                                        "), end='')

def PrintPrices():
	clear()
	if language == "russian":
		cohr5 = open("prices_ru.txt","r")
	elif language == "english":
		cohr5 = open("prices_en.txt","r")
	socr5 = cohr5.read()
	print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,socr5), end='')
	print('%s%s%s%s%s%d%s%s%s%d%s%s' % (pos(26,1),Fore.WHITE, Back.RED, Style.NORMAL,localize['pr_flag_1'],flagcost," ",localize['pr_flag_2']," ",flagtreecost," ",localize['pr_flag_3']), end='')
	cohr5.close()
	print('%s%s%s%s%s' % (pos(8,30),Fore.WHITE, Back.RED, Style.NORMAL,localize['exit']), end='')
	input("")
	ClearFullScreen()

def ChangeLanguage():
	global language
	print('%s%s%s%s%s' % (pos(5,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['ch_language']), end='')
	print('%s%s%s%s%s' % (pos(6,2),Fore.RED, Back.WHITE, Style.NORMAL,"1.Русский;"), end='')
	print('%s%s%s%s%s' % (pos(7,2),Fore.RED, Back.WHITE, Style.NORMAL,"2.English."), end='')
	try:
		ln = int(input(""))
		if ln == 1:
			language = "russian"
			ClearFullScreen()
		elif ln == 2:
			language = "english"
			ClearFullScreen()
		else:
			print('%s%s%s%s%s' % (pos(19,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['err_language']), end='')
			input()
			ClearFullScreen()
			return
	except ValueError:
		print('%s%s%s%s%s' % (pos(19,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['err_language']), end='')
		print('%s%s%s%s%s' % (pos(20,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['def_lang']), end='')
		input()
		ClearFullScreen()
		return

localization()
ChangeLanguage()
clear()
#главное меню
if lvl == 0:
	clear()
	errors = 0
	pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
	while 1:
		localization()
		print('%s%s%s%s%s' % (pos(5,10),Fore.RED, Back.BLACK, Style.NORMAL,"Civilization of Letters"), end='')
		print('%s%s%s%s%s' % (pos(6,20),Fore.WHITE, Back.BLACK, Style.NORMAL,localize['menu']), end='')
		print('%s%s%s%s%s' % (pos(11,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['enter_dif']), end='')
		print('%s%s%s%s%s%s%s' % (pos(13,2),Fore.WHITE, Back.RED, Style.NORMAL,"1-",localize['easy'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(14,2),Fore.WHITE, Back.RED, Style.NORMAL,"2-",localize['medium'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(15,2),Fore.WHITE, Back.RED, Style.NORMAL,"3-",localize['hard'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(16,2),Fore.WHITE, Back.RED, Style.NORMAL,"4-",localize['v_hard'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(17,2),Fore.WHITE, Back.RED, Style.NORMAL,"5-",localize['san_m'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(18,2),Fore.WHITE, Back.RED, Style.NORMAL,"6-",localize['training'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(19,2),Fore.WHITE, Back.RED, Style.NORMAL,"7-",localize['ab_game'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,"8-",localize['updates'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(21,2),Fore.WHITE, Back.RED, Style.NORMAL,"9-",localize['c_line'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(22,2),Fore.WHITE, Back.RED, Style.NORMAL,"10-",localize['language'],";"), end='')
		print('%s%s%s%s%s%s%s' % (pos(23,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['version']," - ",version), end='')
		for i in range(-6,6):
			for g in range(-10,10):
				print('%s%s%s%s%s' % (pos(11+i,60+g),Fore.GREEN, Back.YELLOW, Style.NORMAL,","), end='')
		if Cheat or errors > 0:
			print('%s%s%s%s%s' % (pos(11,60),Fore.RED, Back.BLACK, Style.NORMAL,"$"), end='')
		else:
			print('%s%s%s%s%s' % (pos(11,60),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')
		try:
			lvl2 = int(input("\n"))
			clear()
			if lvl2 == 1:
				break
			elif lvl2 == 2:
				break
			elif lvl2 == 3:
				break
			elif lvl2 == 4:
				break
			elif lvl2 == 5:
				itsan = True
				print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_def'],), end='')
				it_def = input()
				if it_def == "y":
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_lvl_s'],), end='')
					lvl_s = int(input())
					if lvl_s < 0 or lvl_s > 4:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_cr_s'],), end='')
					cr_s = int(input())
					if cr_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_cit_s'],), end='')
					cit_s = int(input())
					if cit_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_arm_s'],), end='')
					arm_s = int(input())
					if arm_s < 0 or arm_s > 480:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_res_s'],), end='')
					res_s = int(input())
					if res_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_war_s'],), end='')
					war_s = int(input())
					if war_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_tr_s'],), end='')
					tr_s = int(input())
					if tr_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['ch_fl_s'],), end='')
					fl_s = int(input())
					if fl_s < 0:
						ClearFullScreen()
						print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
						errors += 1
						input()
						continue
					lvl = lvl_s
					break
				elif it_def == "n":
					ClearFullScreen()
					break
				else:
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
					errors += 1
					input()
					continue
			elif lvl2 == 6:
				if language == "russian":
					cohr2 = open("guide_ru.txt","r")
				elif language == "english":
					cohr2 = open("guide_en.txt","r")
				sohr2 = cohr2.read()
				print('%s%s%s%s%s' % (pos(19,2),Fore.WHITE, Back.RED, Style.NORMAL,sohr2), end='')
				cohr2.close()
				print('%s%s%s%s%s' % (pos(10,50),Fore.BLACK, Back.RED, Style.NORMAL,localize['exit']), end='')
				input("")
				ClearFullScreen()
				continue
			elif lvl2 == 7:
				print('%s%s%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['version']," - ",version), end='')
				if language == "russian":
					cohr15 = open("credits_ru.txt","r")
				elif language == "english":
					cohr15 = open("credits_en.txt","r")
				sohr15 = cohr15.read()
				print('%s%s%s%s%s' % (pos(21,2),Fore.WHITE, Back.RED, Style.NORMAL,sohr15), end='')
				cohr15.close()
				print('%s%s%s%s%s' % (pos(11,15),Fore.WHITE, Back.RED, Style.NORMAL,localize['exit']), end='')
				input("")
				ClearFullScreen()
			elif lvl2 == 8:
				if language == "russian":
					cohr3 = open("version_ru.txt","r")
				elif language == "english":
					cohr3 = open("version_en.txt","r")
				sohr3 = cohr3.read()
				print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,sohr3), end='')
				cohr3.close()
				print('%s%s%s%s%s' % (pos(10,54),Fore.BLACK, Back.RED, Style.NORMAL,localize['exit']), end='')
				input("")
				ClearFullScreen()
				continue
			elif lvl2 == 9:
				print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['enter_code']), end='')
				a3 = input("\n").lower()
				if a3 == "setmoney":
					a4 = int(input("\n"))
					SetMoneyCheat = a4
					Cheat = True
					ClearFullScreen()
					continue
				elif a3 == "setarmy":
					a6 = int(input("\n"))
					if a6 <= 480:
						SetArmyCheat = a6
						Cheat = True
						ClearFullScreen()
						continue
					else:
						print('%s%s%s%s%s' % (pos(19,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['err_cheat_1']), end='')
						input(localize['exit'])
						ClearFullScreen()
						continue
				elif a3 == "setres":
					a7 = int(input("\n"))
					SetResCheat = a7
					Cheat = True
					ClearFullScreen()
				elif a3 == "setprogress":
					a8 = int(input("\n"))
					SetProgressCheat = a8
					Cheat = True
					ClearFullScreen()
				elif a3 == "help":
					if language == "russian":
						cohr4 = open("allcheats_ru.txt","r")
					elif language == "english":
						cohr4 = open("allcheats_en.txt","r")
					sohr4 = cohr4.read()
					ClearFullScreen()
					print('%s%s%s%s%s' % (pos(20,2),Fore.WHITE, Back.RED, Style.NORMAL,sohr4), end='')
					cohr4.close()
					print('%s%s%s%s%s' % (pos(10,54),Fore.BLACK, Back.RED, Style.NORMAL,localize['exit']), end='')
					input("")
					ClearFullScreen()
					continue
				elif a3 == "settree":
					a9 = int(input("\n"))
					SetTreeCheat = a9
					Cheat = True
					ClearFullScreen()
				elif a3 == "disableactivecheat":
					disableactivecheat = True
					ClearFullScreen()
				else:
					print('%s%s%s%s%s' % (pos(19,2),Fore.WHITE, Back.RED, Style.NORMAL,localize['err_cheat_2']), end='')
					input(localize['exit'])
					ClearFullScreen()
					continue
			elif lvl2 == 10:
				print('%s%s%s%s%s' % (pos(5,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['ch_language']), end='')
				print('%s%s%s%s%s' % (pos(6,2),Fore.RED, Back.WHITE, Style.NORMAL,"1.Русский;"), end='')
				print('%s%s%s%s%s' % (pos(7,2),Fore.RED, Back.WHITE, Style.NORMAL,"2.English."), end='')
				try:
					ln = int(input(""))
					if ln == 1:
						language = "russian"
						ClearFullScreen()
					elif ln == 2:
						language = "english"
						ClearFullScreen()
					else:
						print('%s%s%s%s%s' % (pos(19,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['err_language']), end='')
						input()
						ClearFullScreen()
						continue
				except:
					print('%s%s%s%s%s' % (pos(19,2),Fore.RED, Back.WHITE, Style.NORMAL,localize['err_language']), end='')
					input()
					ClearFullScreen()
					continue
			else:
				print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
				errors += 1
		except:
			print('%s%s%s%s%s' % (pos(7,30),Fore.RED, Back.YELLOW, Style.NORMAL,localize['error']), end='')
			errors += 1
	lvl = lvl2
	if itsan == True:
		if it_def == 'y':
			kingdom = {'credit':cr_s,'citys':cit_s,'army':arm_s,'resources':res_s,"warriors":war_s,"trees":tr_s,"flags":fl_s}
			lvl = lvl_s
		else:
			kingdom = {'credit':3000,'citys':0,'army':80,'resources':350,"warriors":0,"trees":60,"flags":0}
			lvl = 2
	elif lvl == 1:
		kingdom = {'credit':3000,'citys':0,'army':100,'resources':350,"warriors":0,"trees":100,"flags":0}
	elif lvl == 2:
		kingdom = {'credit':3000,'citys':0,'army':80,'resources':350,"warriors":0,"trees":60,"flags":0}
		days = 400
	elif lvl == 3:
		kingdom = {'credit':3000,'citys':0,'army':50,'resources':350,"warriors":0,"trees":40,"flags":0}
		days = 500
	elif lvl == 4:
		kingdom = {'credit':3000,'citys':0,'army':50,'resources':350,"warriors":0,"trees":40,"flags":0}



# проверка победы
def Win():
#Построить 10 городов.
#Накопить 100000 кредитов.
#Уничтожить всех противников.
	global lvl
	global Cheat
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	if kingdom['citys'] >= 10:
		print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_cityies_1']), end='')
		print('%s%s%s%s%s' % (pos(12,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_cityies_2']), end='')
		print('%s%s%s%s%s' % (pos(14,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win']), end='')
		PrintStatistics()
		print('%s%s%s%s%s' % (pos(20,50),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['exit']), end='')
		input("")
		exit(0)
	elif kingdom['credit'] >= 100000:
		print('%s%s%s%s%s' % (pos(10,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_money_1']), end='')
		print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_money_2']), end='')
		print('%s%s%s%s%s' % (pos(12,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win']), end='')
		PrintStatistics()
		print('%s%s%s%s%s' % (pos(20,50),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['exit']), end='')
		input("")
		exit(0)
	elif enemies == []:
		print('%s%s%s%s%s' % (pos(10,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_war']), end='')
		print('%s%s%s%s%s' % (pos(12,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win']), end='')
		PrintStatistics()
		print('%s%s%s%s%s' % (pos(20,50),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['exit']), end='')
		input("")
		exit(0)
	elif kingdom["flags"] >= 5:
		print('%s%s%s%s%s' % (pos(10,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_flags_1']), end='')
		print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win_flags_2']), end='')
		print('%s%s%s%s%s' % (pos(12,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win']), end='')
		PrintStatistics()
		print('%s%s%s%s%s' % (pos(20,50),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['exit']), end='')
		input("")
		exit(0)
	return

def PrintFlag(x,y):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(x+1,y+1),Fore.WHITE, Back.YELLOW, Style.NORMAL,flagchr), end='')

def PrintFlags():
	for flag in flags:
		PrintFlag(flag['x'],flag['y'])

def BuildFlag(x,y):
	global Error
	global flagcost
	global flagtreecost
	if kingdom["credit"] >= flagcost:
		if kingdom["trees"] >= flagtreecost:
			if world[x][y] == plainchr:
				flags.append(copy.copy(flag))
				flags[len(flags)-1]["x"] = x
				flags[len(flags)-1]["y"] = y
				kingdom["credit"] -= flagcost
				kingdom["trees"] -= flagtreecost
				PrintFlag(flags[len(flags)-1]["x"],flags[len(flags)-1]["y"])
				kingdom['flags'] += 1
				flagcost = flagcost + (flagcost/100*30)
				flagtreecost = flagtreecost + (flagtreecost/100*30)
				Clear()
			else:
				Error = localize['err_flags_1']
		else:
			Error = localize['err_tree_1']
	else:
		Error = localize['err_credits_1']


# строительство корабля
def BuildShip():
	global Error
	if kingdom["citys"] > 0:
		for town in towns:
			if ppos['x'] == town['y'] and ppos['y'] == town['x']:
				if town['owner'] == 1:
					if town['port'] == 1:
						near_water  = False
						for i in range(-1,2):
							for g in range(-1,2):
								if world[town['x']+i][town['y']+g] == waterchr:
									near_water = True
									shippos['x'] = town['x']+i
									shippos['y'] = town['y']+g
									break
							if near_water == True:
								break
					else:
						Error = localize['err_port_1']
			else:
				Error = localize['err_port_2']
	else:
		Error = localize['err_city_1']

def Slowdown():
	global Error
	global itsan
	global days
	global itslow
	global slow
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	if world[ppos['y']][ppos['x']] == slowchr:
		if itsan == False:
			if itslow == False:
				itslow = True
				slow = random.randint(1,20)
				world[ppos["y"]] = world[ppos["y"]][0:ppos["x"]]+plainchr+world[ppos["y"]][ppos["x"]+1:]
			else:
				Error = localize['slow_err']

# Постройка строений в городе
def Build(what):
	global Error
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	# выбор города
	if kingdom["citys"] > 0:
		print('%s%s%s%s%s' % (pos(2,65),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['enter_town']), end='')
		correctnumbers = []
		cnttown = 0
		cnt = 1
		for town in towns:
			if town["owner"] == 1:
				# Если строим порт, то ищем города на побережье
				if what == "port":
					near_water  = False
					for i in range(-1,2):
						for g in range(-1,2):
							if world[town['x']+i][town['y']+g] == waterchr:
								near_water = True
								break
				if what == "port" and near_water == False:
					cnttown += 1
					continue
				if town[what] == 0:
					if kingdom['resources'] >= costs[what]['resources']:
						if kingdom['trees'] >= costs[what]['tree']:
							if kingdom["credit"] >= costs[what]['credit']:
								print('%s%s%s%s%d%s%s' % (pos(2+cnt,65),Fore.MAGENTA, Back.BLACK, Style.NORMAL,cnttown," ",town["Name"]), end='')
								cnt += 1
								correctnumbers.append(cnttown)
							else:
								Error = localize['err_credits_2']
						else:
							Error = localize['err_tree_1']
					else:
						Error = localize['err_res_1']
			cnttown += 1
		if Error == "":
			while 1:
				try:
					print('%s%s%s%s%s' % (pos(2+cnt,65),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"?"), end='')
					answer = int(input())
					break
				except:
					ShowError(10,51,localize['error'])
			if answer in correctnumbers:
				kingdom['credit'] -= costs[what]['credit']
				towns[answer][what] = 1
				kingdom['resources'] -= costs[what]['resources']
				kingdom['trees'] -= costs[what]['tree']
			else:
				print('%s%s%s%s%s' % (pos(2+cnt,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['err_city_2']), end='')
		CityInfo()
	else:
		Error = localize['err_city_1']

# Рубка деревьев
def CutDownTrees():
	global Error
	if world[ppos['y']][ppos['x']] == treechr:
		kingdom["trees"] += random.randint(1,6)
		world[ppos["y"]] = world[ppos["y"]][0:ppos["x"]]+plainchr+world[ppos["y"]][ppos["x"]+1:]
	else:
		Error = localize['err_tree_2']

# Проигрыш
def lose():
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                    "), end='')
	print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.RED, Style.NORMAL,localize['lose']), end='')
	PrintStatistics()
	print('%s%s%s%s%s' % (pos(12,51),Fore.YELLOW, Back.RED, Style.NORMAL,localize['exit']), end='')
	input()
	exit(0)

def Stell():
	global Error
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	if world[ppos['y']][ppos['x']] == chestchr:
		number_iteration = random.randint(2,5)
		newmoney = 0
		for i in range(1,number_iteration):
			clear()
			newmoney += stepLevel(i,0,localize)
		clear()
		newmoney //= 2 
		print('%s%s%s%s%s%d' % (pos(25,51),Fore.CYAN, Back.BLACK, Style.NORMAL,localize['plus_credit'],newmoney), end='')
		input()
		clear()
		kingdom['credit'] += newmoney
		world[ppos["y"]] = world[ppos["y"]][0:ppos["x"]]+plainchr+world[ppos["y"]][ppos["x"]+1:]
		PrintWorld(ppos['x'],ppos['y'])
		if kingdom["citys"] > 0:
			CityInfo()
		PrintPlayer(ppos['y'],ppos['x'])
		Printship()
		PrintEnemies()
		Menu(21,1)
	else:
		Error = localize['err_treasure_1']

# Информация о городах
def CityInfo():
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	cnt = 0
	for town in towns:
		print('%s%s%s%s%s' % (pos(15+cnt,51),Fore.CYAN, Back.BLACK, Style.NORMAL,town['Name'][0:3]), end='')
		str=""
		if town["barrack"] == 1:
			str += '+ '
		else:
			str += '. '
		if town["market"] == 1:
			str += '+ '
		else:
			str += '. '
		if town["port"] == 1:
			str += '+ '
		else:
			str += '. '
		if town["mine"] == 1:
			str += '+ '
		else:
			str += '. '
		if town["sawmill"] == 1:
			str += '+'
		else:
			str += '.'
		print('%s%s%s%s%s' % (pos(15+cnt,55),Fore.CYAN, Back.BLACK, Style.NORMAL,str), end='')
		cnt += 1
	print('%s%s%s%s%s' % (pos(14,55),Fore.CYAN, Back.BLACK, Style.NORMAL,'b r p m s'), end='')


# Битва с i-м противником
def Battle1(i):
	a2 = PrepareBattle(kingdom["army"],enemies[i]["army"],localize)
	if a2 < kingdom["army"]:
		Clear()
		print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                        "), end='')
		print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,localize['win']), end='')
		kingdom["credit"] += enemies[i]["fortune"]
		kingdom["resources"] += int(enemies[i]["fortune"] / 5)
		kingdom["trees"] += int(enemies[i]["fortune"] / 5)
		enemies.pop(i)
		kingdom["army"] -= a2
		input()
		PrintStatistics()
	else:
		lose()
	for enemy in enemies:
		enemy['army'] += random.randint(1,5)


def Battle(i):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	while enemies[i]["army"] > 0 and kingdom["army"] > 0:
		if kingdom["army"] >= 1:
			rnach1 = random.randint(1,kingdom["army"])
			if rnach1 > enemies[i]["army"]:
				rnach1 = enemies[i]["army"]
			print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                              "), end='')
			print('%s%s%s%s%s' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                              "), end='')
			print('%s%s%s%s%s%d%s%d%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"Вы(",kingdom["army"],")>враг(",enemies[i]["army"],")"), end='')
			print('%s%s%s%s%s%d' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"Вы убили  ",rnach1), end='')
			enemies[i]["army"] -= rnach1 
		time.sleep(2)
		if enemies[i]["army"] >= 1:
			rnach2 = random.randint(1,enemies[i]["army"])
			if rnach2 > kingdom["army"]:
				rnach2 = kingdom["army"]
			print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                              "), end='')
			print('%s%s%s%s%s' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                              "), end='')
			print('%s%s%s%s%s%d%s%d%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"Враг(",enemies[i]["army"],")>Вы(",kingdom["army"],")"), end='')
			print('%s%s%s%s%s%d' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"Враг убил ",rnach2), end='')
			kingdom["army"] -= rnach2
		time.sleep(2)
	if enemies[i]["army"] <= 0:
		Clear()
		print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                        "), end='')
		print('%s%s%s%s%s' % (pos(11,51),Fore.YELLOW, Back.GREEN, Style.NORMAL,"Вы победили!"), end='')
		kingdom["credit"] += enemies[i]["fortune"]
		kingdom["resources"] += int(enemies[i]["fortune"] / 5)
		kingdom["trees"] += int(enemies[i]["fortune"] / 5)
		enemies.pop(i)
		PrintStatistics()
	elif kingdom["army"] <= 0:
		lose()
	for enemy in enemies:
		enemy['army'] += random.randint(10,55)

# Проверка нападения на противника
def CheckEnemy():
	i = 0
	for enem in enemies:
		if ppos['x'] == enem['x'] and ppos['y'] == enem['y']:
			pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
			print('%s%s%s%s%s%s%d%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['it_war'],"(",enem["army"],")?"), end='')
			print('%s%s%s%s%s' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"(y/n)"), end='')
			answer3 = input("").lower()
			if answer3 == "y":
				return i
			else:
				print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                            "), end='')
				print('%s%s%s%s%s' % (pos(11,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                            "), end='')
		i += 1
	return -1

# Найм воинов
def HireWarriors():
	global Error
	global warriorcost
	if kingdom["warriors"] > 0:
		if kingdom['credit'] >= warriorcost:
			while 1:
				try:
					pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
					print('%s%s%s%s%s' % (pos(10,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['enter_warriors']), end='')
					answer2 = int(input())
					break
				except:
					ShowError(10,51,localize['error'])
			if answer2 > kingdom['warriors']:
				Error = localize['err_nime_2']
			else:
				if answer2 * warriorcost <= kingdom['credit']:
					kingdom['army'] += answer2
					kingdom['warriors'] -= answer2
				else:
					Error = localize['err_credits_2']
		else:
			Error = localize['err_credits_2']
	else:
		Error = localize['err_nime_2']

# Генерация врагов
def CreateEnemies():
	for i in range(1,7+random.randint(1,20)):
		enemies.append(copy.copy(enemy))
		enemies[len(enemies)-1]['x'] = random.randint(1,45)
		enemies[len(enemies)-1]['y'] = random.randint(1,15)
		while world[enemies[len(enemies)-1]['y']][enemies[len(enemies)-1]['x']] == "~":
			enemies[len(enemies)-1]['x'] = random.randint(1,45)
			enemies[len(enemies)-1]['y'] = random.randint(1,15)
		enemies[len(enemies)-1]['army'] = random.randint(50,110) * lvl
		enemies[len(enemies)-1]['fortune'] = random.randint(1,20) * enemies[len(enemies)-1]['army'] 

# Печать врагов на экране
def PrintEnemies():
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	for enem in enemies:
		print('%s%s%s%s%s' % (pos(enem['y']+1,enem['x']+1),Fore.RED, Back.BLACK, Style.NORMAL,"$"), end='')

# Печать статистики
def PrintStatistics():
	global days
	global itsan
	global itslow
	global slow
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s%s%d' % (pos(2,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['credits'],":",kingdom['credit']), end='')
	print('%s%s%s%s%s%s%d' % (pos(3,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['res'],":",kingdom['resources']), end='')
	print('%s%s%s%s%s%s%d' % (pos(4,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['army'],":",kingdom['army']), end='')
	print('%s%s%s%s%s%s%d' % (pos(5,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['cityies'],":",kingdom['citys']), end='')
	print('%s%s%s%s%s%s%d' % (pos(6,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['naem'],":",kingdom['warriors']), end='')
	print('%s%s%s%s%s%s%d' % (pos(7,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['tree'],":",kingdom['trees']), end='')
	print('%s%s%s%s%s%d%s%d' % (pos(8,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"x:",ppos['x']," y:",ppos['y']), end='')
	if itsan == False:
		if itslow == False:
			print('%s%s%s%s%s%s%d' % (pos(9,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['days'],":",days), end='')
		else:
			print('%s%s%s%s%s%s%d' % (pos(9,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['slow'],":",slow), end='')
	else:
		print('%s%s%s%s%s' % (pos(9,51),Fore.GREEN, Back.BLACK, Style.NORMAL,localize['san']), end='')

# Печать одного города
def PrintTown(x,y,town):
	global townchr
	global waterchr
	global plainchr
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	for i in range(-2,2):
		for g in range(-2,2):
			if world[town['x']+i][town['y']+g] != waterchr:
				print('%s%s%s%s%s' % (pos(x-i,y-g),Fore.MAGENTA, Back.BLACK, Style.NORMAL,townchr), end='')
	#print('%s%s%s%s%s' % (pos(x+1,y+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,townchr), end='')
	#if world[town['x']+i][town['y']+g] == waterchr:

# Печать всех городов
def PrintTowns():
	for town in towns:
		PrintTown(town['x'],town['y'],town)

# Очистка
def Clear():
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	for i in range(1,14):
		print('%s%s%s%s%s' % (pos(i,51),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                             "), end='')
	print('%s%s%s%s%s' % (pos(20,1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"                                 "), end='')

def EditTownName():
	global Error
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	if kingdom["citys"] > 0:
		print('%s%s%s%s%s' % (pos(2,65),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['enter_town']), end='')
		correctnumbers2 = []
		cnttown2 = 0
		cnt2 = 1
		for town in towns:
			if town["owner"] == 1:
				print('%s%s%s%s%d%s%s' % (pos(2+cnt2,65),Fore.MAGENTA, Back.BLACK, Style.NORMAL,cnttown2," ",town["Name"]), end='')
				cnt2 += 1
				correctnumbers2.append(cnttown2)
			cnttown2 += 1
		answer2 = int(input(""))
		if answer2 in correctnumbers2:
			print('%s%s%s%s%s' % (pos(20,1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['enter_name']), end='')
			name2 = input("")
			towns[answer2]["Name"] = name2
		else:
			Error = localize['err_city_2']
		CityInfo()
	else:
		Error = localize['err_city_1']
# Ввод имени города
def EnterTownName(x,y):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(x,y),Fore.MAGENTA, Back.BLACK, Style.NORMAL,localize['enter_name']), end='')
	name = input("")
	return name

# Строительство города
def BuildTown(x,y):
	global Error
	global towncost
	global treetowncost
	global restowncost
	err = 0
	check = 0
	if kingdom['resources'] >= restowncost:
		if kingdom['trees'] >= treetowncost:
			if kingdom["credit"]>=towncost:
				for i in range(-2,1):
					for g in range(-2,1):	
						if world[x][y] == plainchr:
							if world[x-i][y-g] == plainchr or world[x-i][y-g] == waterchr:
								check += 1
							else:
								Error = localize['err_city_5']
								err += 1
						else:
							Error = localize['err_city_0']
							err += 1
			else:
				Error = localize['err_credits_1']
				err += 1
		else:
			Error = localize['err_tree_1']
			err += 1
	else:
		Error = localize['err_res_1']
		err += 1
	if err == 0:
		towns.append(copy.copy(city))
		towns[len(towns)-1]["Name"] = EnterTownName(20,1)
		towns[len(towns)-1]["x"] = x
		towns[len(towns)-1]["y"] = y
		towns[len(towns)-1]["owner"] = 1
		kingdom["credit"] -= towncost
		kingdom["trees"] -= treetowncost
		kingdom["resources"] -= restowncost
		PrintTown(towns[len(towns)-1]["x"],towns[len(towns)-1]["y"],towns[len(towns)-1])
		kingdom['citys'] += 1
		Clear()
		CityInfo()

# Основное меню
def Menu(x,y):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s%s%s%s%s%s%s%s%s' % (pos(x,y),Fore.RED, Back.BLACK, Style.BRIGHT,"[0]-",localize['build_town'],", [r]-",localize['rinka'],", [m]-",localize['mine'],", [t]-",localize['cut_tree'],","), end='')
	print('%s%s%s%s%s%s%s%s%s%s%s' % (pos(x+1,y),Fore.RED, Back.BLACK, Style.BRIGHT,"[p]-",localize['build_port'],", [b]-",localize['barrack'],", [h]-",localize['nime_to_warrior'],";"), end='')
	print('%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (pos(x+2,y),Fore.RED, Back.BLACK, Style.BRIGHT,"[g]-",localize['price'],";[j]-",localize['stell'],";#-",localize['city'],";,-",localize['rav'],";Y-",localize['tree_cnt'],";~-",localize['water'],";"), end='')
	print('%s%s%s%s%s%s%s%s%s%s%s%s%s' % (pos(x+3,y),Fore.RED, Back.BLACK, Style.BRIGHT,"[s]-",localize['build_ship'],";[f]-",localize['flag'],";[l]-",localize['sawmill'],";[u]-",localize['change_name_city'],";"), end='')
	print('%s%s%s%s%s%s%s' % (pos(x+4,y),Fore.RED, Back.BLACK, Style.BRIGHT,localize['version']," - ",version), end='')

# Вывод ошибки
def ShowError(x,y,str):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(x,y),Fore.YELLOW, Back.RED, Style.NORMAL,str), end='')
	time.sleep(1)

# Информационное сообщение
def ShowInfo(x,y,str):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(x,y),Fore.CYAN, Back.GREEN, Style.NORMAL,str), end='')

# Генерация острова
def genIsland():
	octrov = 2*random.randint(1,5)+1
	y_centr = random.randint(6,13)
	x_centr = random.randint(11,39)
	#Печать верхнего треугольника
	for h in range(1,octrov//2+1):
		str = ""
		for w in range(1,2*h):
			d = random.randint(0,1000)
			if d < 600:
				str=str+","
			elif d > 600 and d < 950:
				str=str+"Y"
			elif d > 950 and d < 980:
				str=str+"M"
			else:
				str=str+"T"
		y = y_centr-octrov//2+h-1
		world[y]= world[y][0:x_centr-w//2]+str+world[y][x_centr+w//2+1:]
	#Печать нижнего треугольника
	for h in range(1,octrov//2+1):
		str = ""
		for w in range(1,2*h):
			d = random.randint(0,1000)
			if d < 600:
				str=str+","
			elif d > 600 and d < 950:
				str=str+"Y"
			elif d > 950 and d < 980:
				str=str+"M"
			else:
				str=str+"T"
		y = y_centr+octrov//2-h+1
		world[y]= world[y][0:x_centr-w//2]+str+world[y][x_centr+w//2+1:]
	#Печать центра острова
	str = str + ",,"
	world[y_centr] = world[y_centr][0:x_centr-octrov//2]+str+world[y_centr][x_centr+octrov//2+1:]

#Распечатка мира
def PrintWorld(x,y):
	for i in range(0,19):
		for g in range(0,49):
			pos = lambda g, i: '\x1b[%d;%dH' % (g, i)
			if i == y and g == x:
				print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')
			else:
				if world[i][g] == "~":
					print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.CYAN, Style.NORMAL,"~"), end='')
				if world[i][g] == ",":
					print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.GREEN, Back.YELLOW, Style.NORMAL,","), end='')
				if world[i][g] == "Y":
					print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.GREEN, Back.YELLOW, Style.NORMAL,"Y"), end='')
				if world[i][g] == "M":
					print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.YELLOW, Back.BLACK, Style.NORMAL,"M"), end='')
				if world[i][g] == "T":
					print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.BLACK, Style.NORMAL,"T"), end='')

# Печать игрока сверху карты
def PrintPlayer(x,y):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	print('%s%s%s%s%s' % (pos(x+1,y+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')

# распечатка корабля поверх мира
def Printship():
	if shippos['x'] > -1 and shippos['y'] > -1:
		pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
		print('%s%s%s%s%s' % (pos(shippos['x']+1,shippos['y']+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"P"), end='')

# Печать части мира в том месте, где в прошлом ходу был игрок
def PrintWorldPart(i,g):
	pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
	if world[i][g] == "~":
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.CYAN, Style.NORMAL,"~"), end='')
	if world[i][g] == ",":
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.GREEN, Back.YELLOW, Style.NORMAL,","), end='')
	if world[i][g] == "Y":
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.GREEN, Back.YELLOW, Style.NORMAL,"Y"), end='')
	if world[i][g] == "M":
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.YELLOW, Back.BLACK, Style.NORMAL,"M"), end='')
	if world[i][g] == "T":
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.BLACK, Style.NORMAL,"T"), end='')

#Сделать шаг
def move(dx,dy):
	global Insea
	if ppos['y'] + dy < 0 or ppos['y'] + dy > len(world)-2 or ppos['x'] + dx < 0 or ppos['x'] + dx > 48:
		#Error = "Нельзя"
		return
	if Insea == True:
		if world[ppos['y']+dy][ppos['x']+dx] == waterchr:
			shippos['y'] += dx
			shippos['x'] += dy
			ppos['x'] = shippos['y']
			ppos['y'] = shippos['x']
		else:
			if world[ppos['y']+dy][ppos['x']+dx] != waterchr:
				Insea = False
				ppos['y']+=dy
				ppos['x']+=dx
	else:
		if world[ppos['y']+dy][ppos['x']+dx] != waterchr:
			ppos['y']+=dy
			ppos['x']+=dx
		else:
			if ppos['y']+dy == shippos['x'] and ppos['x']+dx == shippos['y']:
				Insea = True
				ppos['y'] = shippos['x']
				ppos['x'] = shippos['y']
			#else:
				#ShowError(10,51,"Нельзя")

# Иттерация цикла управления
def Upravlenie():
	global Error
	global Insea
	global days
	global lvl
	global win
	global Cheat
	global SetMoneyCheat
	global SetArmyCheat
	global CheckCheat
	global SetResCheat
	global SetProgressCheat
	global itslow
	global slow
	if itsan == False:
		if itslow == False:
			days -= 1
		else:
			if slow > 0:
				slow -= 1
			else:
				itslow = False
	Clear()
	if Error != "":
		ShowError(10,51,Error)
		Error = ""
	Win()
	Bat = CheckEnemy()
	if Bat != -1:
		clear()
		Battle1(Bat)
		clear()
		PrintWorld(ppos['x'],ppos['y'])
		if kingdom["citys"] > 0:
			CityInfo()
	PrintPlayer(ppos['y'],ppos['x'])
	Printship()
	PrintEnemies()
	Menu(21,1)
	Slowdown()
	if Cheat:
		pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
		if disableactivecheat == False:
			print('%s%s%s%s%s' % (pos(11,55),Fore.RED, Back.BLACK, Style.BRIGHT,localize['cheat_on']), end='')
		if CheckCheat != 1:
			if SetMoneyCheat > 0:
				kingdom["credit"] = SetMoneyCheat
				CheckCheat = 1
			if SetArmyCheat > 0:
				kingdom["army"] = SetArmyCheat
				CheckCheat = 1
			if SetResCheat > 0:
				kingdom["resources"] = SetResCheat
				CheckCheat = 1
			if SetProgressCheat > 0:
				if itsan == False:
					days = SetProgressCheat
					CheckCheat = 1
			if SetTreeCheat > 0:
				kingdom["trees"] = SetTreeCheat
				CheckCheat = 1
	PrintStatistics()
	command  = msvcrt.getch()
	if command == b'\xe0':
		command = msvcrt.getch()
	PrintWorldPart(ppos['y'],ppos['x'])
	if command == b'z':
		move(-1,1)
	if command == b'x' or ord(command)==80:
		move(0,1)
	if command == b'c':
		move(1,1)
	if command == b'a' or ord(command)==75:
		move(-1,0)
	if command == b'd' or ord(command)==77:
		move(1,0)
	if command == b'q':
		move(-1,-1)
	if command == b'w' or ord(command)==72:
		move(0,-1)
	if command == b'e':
		move(1,-1)
	if command == b'0':
		BuildTown(ppos['y'],ppos['x'])
	if command == b'b':
		Build("barrack")
	if command == b'r':
		Build("market")
	if command == b'm':
		Build("mine")
	if command == b'h':
		HireWarriors()
	if command == b't':
		CutDownTrees()
	if command == b'p':
		Build("port")
	if command == b's':
		BuildShip()
	if command == b'f':
		BuildFlag(ppos['y'],ppos['x'])
	if command == b'l':
		Build("sawmill")
	if command == b'g':
		PrintPrices()
		PrintWorld(ppos['x'],ppos['y'])
		PrintPlayer(ppos['y'],ppos['x'])
		Printship()
		PrintEnemies()
		Menu(21,1)
		if kingdom["citys"] > 0:
			CityInfo()
	if command == b'u':
		EditTownName()
	if command == b'j':
		Stell()

# генерация начального мира из воды
for i in range(0,20):
	str = ""
	for g in range(0,50):
		str = str+"~"
	world.append(str)

# генерация островов и материков путем наложения островов друг на друга
for j in range(1,random.randint(3,25)):
	genIsland()

#Генерация игрока
ppos['x'] = random.randint(1,30)
ppos['y'] = random.randint(1,15)
while world[ppos['y']][ppos['x']] == "~":
	ppos['x'] = random.randint(1,30)
	ppos['y'] = random.randint(1,15)

PrintWorld(ppos['x'],ppos['y'])
CreateEnemies()
if itsan == True:
	days = 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
# Основной цикл управления
for i in range(0,days):
	# Добавление кредитов игроку
	for town in towns:
		if town['owner'] == 1:
			if town['market'] == 1:
				if lvl == 1:
					kingdom['credit'] += 100
				if lvl == 2:
					kingdom['credit'] += 70
				if lvl == 3:
					kingdom['credit'] += 50
				if lvl == 4:
					kingdom['credit'] += 40
			if town['mine'] == 1:
				if lvl == 1:
					kingdom['resources'] += 10
				if lvl == 2:
					kingdom['resources'] += 7
				if lvl == 3:
					kingdom['resources'] += 5
				if lvl == 4:
					kingdom['resources'] += 4
			if town['barrack'] == 1:
				kingdom['warriors'] += 1
			if town["sawmill"] == 1:
				kingdom["trees"] += 1
	Upravlenie()
	PrintTowns()
	PrintFlags()