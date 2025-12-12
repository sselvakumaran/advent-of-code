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
	presents = []
	queries = []
	lines = data.splitlines()
	N = len(lines)

	i = 0
	# assume present shapes are 3x3
	while i < N and re.fullmatch("[0-9]+:", lines[i]):
		presents.append([
			[1 if lines[j][k] == "#" else 0 for k in range(3)]
			for j in range(i+1, i + 4)
		])
		i += 5
	
	while i < N:
		dims, counts = lines[i].split(": ")
		queries.append((
			tuple(map(int, dims.split("x"))),
			list(map(int, counts.split(" ")))
		))
		i += 1

	return presents, queries


def part1(data: str):
	presents, queries = parse_data(data)
	
	out = 0
	for query in queries:
		(h, w), counts = query
		A_shapes = sum([sum(itertools.chain(*present)) * count for present, count in zip(presents, counts)])
		A_total = h * w
		out += 1 if A_shapes <= A_total else 0
	return out

def part2(data: str) -> int:
	pass

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