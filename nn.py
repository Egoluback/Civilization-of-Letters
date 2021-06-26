import colorama
from colorama import Fore, Back, Style
import time

colorama.init()

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
#print('%s%s%s%s%s' % (pos(x+3,y),Fore.RED, Back.BLACK, Style.BRIGHT,"[s]-создание корабля"), end='')
armysize = 100

def PrintArmy(size):
	pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
	for i in range(0,size):
		print('%s%s%s%s%s' % (pos(5+i//10,51-size//10+i%10),Fore.RED, Back.BLACK, Style.BRIGHT,"$"), end='')
		time.sleep(0.1)
	for i in range(0,size):
		print('%s%s%s%s%s' % (pos(5+i//10,size//10+1-i%10),Fore.MAGENTA, Back.BLACK, Style.BRIGHT,"$"), end='')
		time.sleep(0.1)
	input()
pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
for i in range(0,21):
	for g in range(0,51):
		print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.RED, Back.GREEN, Style.BRIGHT," "), end='')
PrintArmy(armysize)