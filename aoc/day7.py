import sys
import os
import argparse
import re
import bisect
from functools import reduce
import operator
from itertools import zip_longest
from dataclasses import dataclass

def part1(data: str):
	lines = data.splitlines()
	splitters = [[] for _ in range(len(lines))]
	start = None
	for i, line in enumerate(lines):
		for j, c in enumerate(line):
			if c == 'S':
				start = (i, j)
			if c == '^':
				splitters[i].append(j)
	
	# simulate
	used_splitters = 0
	beams = set([start[1]])
	for layer in splitters[start[0]+1:]:
		for splitter in layer:
			if splitter in beams:
				beams.add(splitter-1)
				beams.remove(splitter)
				beams.add(splitter+1)
				used_splitters += 1
	return used_splitters


def part2(data: str):
	lines = data.splitlines()
	M, N = len(lines), len(lines[0])
	splitters = [[] for _ in range(M)]
	start = None
	for i, line in enumerate(lines):
		for j, c in enumerate(line):
			if c == 'S':
				start = (i, j)
			if c == '^':
				splitters[i].append(j)
	
	beams = [0 for _ in range(N)]
	beams[start[1]] = 1
	for layer in splitters[start[0]+1:]:
		if not layer: continue
		new_beams = beams.copy()
		for splitter in layer:
			if beams[splitter] > 0:
				num_beams = beams[splitter]
				new_beams[splitter - 1] += num_beams
				new_beams[splitter] = 0
				new_beams[splitter + 1] += num_beams
		beams = new_beams
	return sum(beams)


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