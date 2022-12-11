#!/bin/env python3

import os
import argparse
import random

lines = []
delim = "-" * 80

origlinenum = 0
origwordnum = 0
linenum = 0
wordnum = 0
spaceind = 0

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("-n", default=20, help="number of words in context", type=int)
parser.add_argument("--mode", choices=["hero","gm","revgm"], default="hero")
parser.add_argument("-c",help="move interval in gm mode",type=int, default=1)
args = parser.parse_args()

f = open(args.filename,"r")
for x in f:
	words = x.split(" ")
	if len(words) == 0: continue
	lines.append(words)
f.close()

def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

def randomize_vars():
	global origlinenum, origwordnum, wordnum, linenum
	global spaceind
	origlinenum = random.randrange(0, len(lines))
	origwordnum = random.randrange(0, len(lines[origlinenum]))
	if args.mode == "hero":
		spaceind = random.randrange(0, args.n)
	elif args.mode == "gm":
		spaceind = args.n - 1
	else:
		spaceind = 0
	linenum = origlinenum
	wordnum = origwordnum	

def forward_vars(amount):
	global origlinenum, origwordnum, wordnum, linenum
	origwordnum += amount
	while origwordnum >= len(lines[origlinenum]):
		origwordnum += len(lines[origlinenum])
		origlinenum += 1
	wordnum = origwordnum
	linenum = origlinenum

def backward_vars(amount):
	global origlinenum, origwordnum, wordnum, linenum
	origwordnum -= amount
	while origwordnum < 0 :
		origwordnum += len(lines[origlinenum])
		origlinenum -= 1	
	wordnum = origwordnum
	linenum = origlinenum

def one_round():
	global origlinenum, origwordnum, wordnum, linenum
	print(delim)
	line = lines[linenum]
	exc = ""
	spaceword = ""
	i = 0
	while i < args.n:
		if i == spaceind:
			exc += "[..]"
			spaceword = line[wordnum]
		else:
			exc += line[wordnum]
		i+=1
		wordnum += 1
		if wordnum >= len(line):
			exc += "\n"
			linenum += 1
			wordnum = 0
		else:
			exc += " "
	print(exc)
	print(delim)
	print()
	w = input("> ")
	print("= "+spaceword)
	print()
	input("Press ENTER to continue...")
	
randomize_vars()
while True:
	screen_clear()
	if args.mode == "hero":
		randomize_vars()
	elif args.mode == "gm": 
		forward_vars(args.c)	
	else:
		backward_vars(args.c)
	one_round()
