#!/bin/env python3

import os
import sys
import argparse
import random

lines = []
delim = "_" * 80

origlinenum = 0
origwordnum = 0
linenum = 0
wordnum = 0
spaceind = 0

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--cl", default=20, help="context length in words", type=int)
parser.add_argument("--mode", choices=["hero","gm","revgm"], default="hero")
parser.add_argument("--ma",help="move amount in gm mode",type=int, default=1)
parser.add_argument("-n",help="number of words to guess",type=int,default=1)
parser.add_argument("--hint",help="show hint of results",action="store_true")
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
		spaceind = random.randrange(1, args.cl-args.n)
	elif args.mode == "gm":
		spaceind = args.cl - args.n
	else:
		spaceind = 0
	linenum = origlinenum
	wordnum = origwordnum	

def forward_vars(amount):
	global origlinenum, origwordnum, wordnum, linenum
	for _ in range(0,amount):
		origwordnum += 1
		if origwordnum >= len(lines[origlinenum]):
			origlinenum +=1
			origwordnum = 0
	wordnum = origwordnum
	linenum = origlinenum

def backward_vars(amount):
	global origlinenum, origwordnum, wordnum, linenum
	for _ in range(0, amount):
		origwordnum -= 1
		if origwordnum < 0:
			origlinenum -= 1
			origwordnum = len(lines[origlinenum]) - 1
	wordnum = origwordnum
	linenum = origlinenum

def one_round():
	global origlinenum, origwordnum, wordnum, linenum
	print(delim+"\n")
	line = lines[linenum]
	exc = ""
	spacewords = []
	i = 0
	j = 0
	while i < args.cl:
		if i >= spaceind and i < spaceind+args.n:
			j = i-spaceind+1
			exc += f"[..{j}]"
			spacewords.append(line[wordnum])
		else:
			exc += line[wordnum]
			j = 0
		i+=1
		wordnum += 1
		if wordnum >= len(line):
			exc += "\n"
			linenum += 1
			wordnum = 0
			line = lines[linenum]
		else:
			exc += " "
	print(exc)
	print(delim+"\n")
	print()
	if args.hint:
		hints = spacewords.copy()
		random.shuffle(hints)
		hintstr = " ".join(hints).replace("\n","")
		input("Press ENTER to reveal hint...")
		print(f"\033[1AHint: {hintstr}\033[K")
		print()
	w = input("> ")
	print("= "+" ".join(spacewords))
	print()
	input("Press ENTER to continue...")
	
try:
	randomize_vars()
	while True:
		screen_clear()
		if args.mode == "hero":
			randomize_vars()
		elif args.mode == "gm": 
			forward_vars(args.ma+args.n-1)	
		else:
			backward_vars(args.ma+args.n-1)
		one_round()
except KeyboardInterrupt:
	print("\n\nThanks for visiting the writer's gym!\n")
