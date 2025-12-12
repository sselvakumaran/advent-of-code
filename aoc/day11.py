import sys
import os
import argparse
import re
import bisect
from functools import reduce
import operator
import itertools
from dataclasses import dataclass, field
import heapq
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
from fractions import Fraction

def parse_data(data: str):
	A = dict()
	for line in data.splitlines():
		n0, ns = line.split(": ")
		A[n0] = ns.split(" ")
	return A

def part1(data: str):
	A = parse_data(data)
	A['out'] = []
	# 1. topological sort
	V = set()
	P = set()
	stack = []
	def dfs(n):
		if n in V: return True
		if n in P: return False
		P.add(n)
		for m in A[n]:
			if not dfs(m): return False
		P.remove(n)
		V.add(n)
		stack.append(n)
		return True
	for n in A.keys():
		if n not in V: dfs(n)
	
	while stack and stack[-1] != "you":
		stack.pop()
	
	nodes = reversed(stack)
	node_counts = defaultdict(int)
	node_counts['you'] = 1
	for n in nodes:
		v = node_counts[n]
		for m in A[n]:
			node_counts[m] += v
	return node_counts['out']

def part2(data: str) -> int:
	A = parse_data(data)
	A['out'] = []
	# 1. topological sort
	V = set()
	P = set()
	stack = []
	def dfs(n):
		if n in V: return True
		if n in P: return False
		P.add(n)
		for m in A[n]:
			if not dfs(m): return False
		P.remove(n)
		V.add(n)
		stack.append(n)
		return True
	for n in A.keys():
		if n not in V: dfs(n)
	
	while stack and stack[-1] != 'svr':
		stack.pop()
	nodes = list(reversed(stack))
	node_counts = defaultdict(lambda: [0, 0, 0, 0])
	node_counts['svr'] = [1, 0, 0, 0]
	add_vals = lambda x, y: [x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3]]
	for n in nodes:
		v = node_counts[n].copy()
		if n == 'fft':
			v[1] = v[0]
			v[3] = v[2]
		if n == 'dac':
			v[2] = v[0]
			v[3] = v[1]
		for m in A[n]:
			node_counts[m] = add_vals(node_counts[m], v) 
	#print(node_counts)
	return node_counts['out'][3]

def valid_file(path):
	if not os.path.isfile(path):
		raise argparse.ArgumentTypeError(f"input file does not exist: {path}")
	return path

def get_parser():
	parser = argparse.ArgumentParser(
		prog="advent of code problem",
	)
	parser.add_argument('input', type=valid_file, help="path to aoc input file")
	parser.add_argument("part", type=int, choices=[1, 2], help="what part to run")
	return parser

if __name__ == "__main__":
	parser = get_parser()
	args = parser.parse_args()
	
	data_file = open(args.input)
	data = data_file.read()
	data_file.close()

	out = part1(data) if args.part == 1 else part2(data)
	print(out)