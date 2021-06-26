import copy
import msvcrt
import colorama
from colorama import Fore, Back, Style
import os
import random
import time

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

colorama.init()

world = []
ppos = {'x':0,'y':0}
skychr = '.'
landchr = '-'
chestchr = 'M'
chests = []
trees = []
chest = {'x':0,'y':0}
tree = {'x':0,'y':0}
ex = {'x':0,'y':0}
exitList = []

def CreateWorld(y_sky,y_land,x_sky,x_land):
    for i in range(0,y_sky):
        str = ""
        for g in range(0,x_sky):
            str = str+"."
        world.append(str)
    for i in range(y_sky,y_land):
        str = ""
        for g in range(0,x_land):
            str = str+"-"
        world.append(str)

def CreatePlayer():
    ppos['x'] = random.randint(0,30)
    ppos['y'] = 12

def PrintWorld(x,y):
    for i in range(0,24):
        for g in range(0,60):
            pos = lambda g, i: '\x1b[%d;%dH' % (g, i)
            if i == y and g == x:
                print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')
            else:
                if world[i][g] == '.':
                    print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.CYAN, Style.NORMAL,"."), end='')
                if world[i][g] == '-':
                    print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.YELLOW, Back.GREEN, Style.NORMAL,"-"), end='')

def CreateChest():
    for i in range(1,7+random.randint(1,10)):
        chests.append(copy.copy(chest))
        chests[len(chests)-1]['x'] = random.randint(1,45)
        chests[len(chests)-1]['y'] = random.randint(1,15)
        while world[chests[len(chests)-1]['y']][chests[len(chests)-1]['x']] == ".":
            chests[len(chests)-1]['x'] = random.randint(1,45)
            chests[len(chests)-1]['y'] = random.randint(1,15)

def PrintChest():
    pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
    for ch in chests:
        print('%s%s%s%s%s' % (pos(ch['y']+1,ch['x']+1),Fore.YELLOW, Back.BLACK, Style.NORMAL,"M"), end='')

def CreateTrees():
    for i in range(1,7+random.randint(1,50)):
        trees.append(copy.copy(tree))
        trees[len(trees)-1]['x'] = random.randint(1,45)
        trees[len(trees)-1]['y'] = random.randint(1,15)
        while world[trees[len(trees)-1]['y']][trees[len(trees)-1]['x']] == ".":
            trees[len(trees)-1]['x'] = random.randint(1,45)
            trees[len(trees)-1]['y'] = random.randint(1,15)

def PrintTrees():
    pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
    for tr in trees:
        a = 0
        b = 0
        for ch in chests:
            if tr['x'] == ch['x'] and tr['y'] == ch['y']:
                a += 1
        for ex in exitList:
            if tr['x'] == ex['x'] and tr['y'] == ex['y']:
                b += 1
        if a == 0 and b == 0:
            print('%s%s%s%s%s' % (pos(tr['y']+1,tr['x']+1),Fore.YELLOW, Back.GREEN, Style.NORMAL,"Y"), end='')

def CreateexitList():
    exitList.append(copy.copy(ex))
    exitList[len(exitList)-1]['x'] = random.randint(1,45)
    exitList[len(exitList)-1]['y'] = random.randint(1,15)
    while world[exitList[len(exitList)-1]['y']][exitList[len(exitList)-1]['x']] == ".":
        exitList[len(exitList)-1]['x'] = random.randint(1,45)
        exitList[len(exitList)-1]['y'] = random.randint(1,15)

def PrintexitList():
    pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
    for ex in exitList:
        print('%s%s%s%s%s' % (pos(ex['y']+1,ex['x']+1),Fore.WHITE, Back.RED, Style.NORMAL,"#"), end='')

class Player:
    def __init__(self,money):
        self.money = money

    def PrintPlayer(self,x,y):
        pos = lambda x, y: '\x1b[%d;%dH' % (x, y)
        print('%s%s%s%s%s' % (pos(x+1,y+1),Fore.MAGENTA, Back.BLACK, Style.NORMAL,"$"), end='')

    def PrintWorldPart(self,i,g):
        pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
        if world[i][g] == ".":
            print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.BLUE, Back.CYAN, Style.NORMAL,"."), end='')
        if world[i][g] == "-":
            print('%s%s%s%s%s' % (pos(i+1,g+1),Fore.YELLOW, Back.GREEN, Style.NORMAL,"-"), end='')

    def moveP(self,dx,dy):
        if ppos['y'] + dy < 0 or ppos['y'] + dy > len(world)-2 or ppos['x'] + dx < 0 or dx + ppos['x'] > 59:
            return
        if world[ppos['y']+dy][ppos['x']+dx] != skychr:
            ppos['y']+=dy
            ppos['x']+=dx

    def CheckChest(self):
        i = 0
        for ch in chests:
            if ppos['x'] == ch['x'] and ppos['y'] == ch['y']:
                return i
            i += 1
        return -1
    
    def CheckExitList(self):
        for ex in exitList:
            if ppos['x'] == ex['x'] and ppos['y'] == ex['y']:
                exit(0)

    def LiftChest(self,i):
        chests.pop(i)
        self.money += random.randint(1,50)

    def printMoney(self):
        pos = lambda i, g: '\x1b[%d;%dH' % (i, g)
        print('%s%s%s%s%s' % (pos(20,61),Fore.RED, Back.BLACK, Style.NORMAL,"Найдено богатств: "), end='')
        print('%s%s%s%s%d' % (pos(21,61),Fore.RED, Back.BLACK, Style.NORMAL,self.money), end='')

    def step(self):
        self.CheckExitList()
        PrintChest()
        PrintexitList()
        PrintTrees()
        self.PrintPlayer(ppos['y'],ppos['x'])
        command = msvcrt.getch()
        self.PrintWorldPart(ppos['y'],ppos['x'])
        if command == b'w':
            self.moveP(0,-1)
        elif command == b'd':
            self.moveP(1,0)
        elif command == b's':
            self.moveP(0,1)
        elif command == b'a':
            self.moveP(-1,0)
        elif command == b'c':
            itChest = self.CheckChest()
            if itChest != -1:
                self.LiftChest(itChest)