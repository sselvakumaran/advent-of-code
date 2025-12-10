import sys
import os
import argparse
import re
import bisect
from functools import reduce
import operator
from itertools import zip_longest, combinations
from dataclasses import dataclass
import heapq
from collections import Counter
def part1(data: str):
	def dist(t1, t2):
		x1, y1, z1 = t1
		x2, y2, z2 = t2
		return pow(x2 - x1, 2) + pow(y2 - y1, 2) + pow(z2 - z1, 2)
	coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]
	N = len(coords)
	idx_to_coord = dict(enumerate(coords))

	distances = list(map(
		lambda idx_t: (
			dist(idx_to_coord[idx_t[0]], idx_to_coord[idx_t[1]]), 
			idx_t[0], 
			idx_t[1]), 
		combinations(range(N), 2)))
	heapq.heapify(distances)

	parents = [i for i in range(N)]

	def get_parent(i):
		while parents[i] != i:
			i = parents[i]
		return i
	NUM_MERGES = 1000
	for _ in range(NUM_MERGES):
		if not distances: break
		_, i1, i2 = heapq.heappop(distances)
		p1 = get_parent(i1)
		p2 = get_parent(i2)
		parents[p2] = p1
	owners = [get_parent(i) for i in range(N)]
	C = Counter(owners)
	#print(C)
	(_, t1), (_, t2), (_, t3) = C.most_common(3)
	return t1 * t2 * t3

def part2(data: str):
	def dist(t1, t2):
		x1, y1, z1 = t1
		x2, y2, z2 = t2
		return pow(x2 - x1, 2) + pow(y2 - y1, 2) + pow(z2 - z1, 2)
	coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]
	N = len(coords)
	idx_to_coord = dict(enumerate(coords))

	distances = list(map(
		lambda idx_t: (
			dist(idx_to_coord[idx_t[0]], idx_to_coord[idx_t[1]]), 
			idx_t[0], 
			idx_t[1]), 
		combinations(range(N), 2)))
	heapq.heapify(distances)

	parents = [i for i in range(N)]

	def get_parent(i):
		while parents[i] != i:
			i = parents[i]
		return i
	last = None
	while distances:
		_, i1, i2 = heapq.heappop(distances)
		p1 = get_parent(i1)
		p2 = get_parent(i2)
		parents[p2] = p1
		if p1 != p2:
			last = (i1, i2)
	owners = [get_parent(i) for i in range(N)]
	C = Counter(owners)
	print(last)
	return idx_to_coord[last[0]][0] * idx_to_coord[last[1]][0]

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