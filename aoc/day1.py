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
	pattern = re.compile(r"([LR])([0-9]+)")
	out = []
	for line in data.splitlines():
		if line is None: continue
		tup = re.match(pattern, line)
		if tup is None: raise ValueError("error with pattern")
		dir_raw, val_raw = tup.groups()
		val = int(val_raw)
		out.append(dir_raw, val)
	return out

def part1(data: str):
	lines = parse_data(lines)
	password = 0
	pos = 50
	for line in lines:
		direction, value = line
		shift = value * (1 if direction == "R" else -1)
		pos = (pos + shift) % 100
		if pos == 0: password += 1
	return password

def part2(data: str) -> int:
	lines = parse_data(lines)

	def clicks_and_pos(start, end):
		new_pos = (end % 100)
		num_clicks = 0
		if end >= 100:
			return (end // 100), new_pos
		if 0 <= end and end < 100:
			return (1 if end == 0 else 0), new_pos
		if start == 0:
			return -((end + 99) // 100), new_pos
		return -((end - 1) // 100), new_pos

	password = 0
	pos = 50
	for line in lines:
		direction, value = line
		dir_int = (1 if direction == "R" else -1)
		shift = value * dir_int
		d_password, pos = clicks_and_pos(pos, pos + shift)
		password += d_password
	return password

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