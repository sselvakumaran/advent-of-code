import sys
import os
import argparse
import re
import bisect
from functools import reduce, cache
import operator
import itertools
from dataclasses import dataclass, field
import heapq
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple
from fractions import Fraction

def parse_data(data: str):
	return [
		map(int, interval.split("-"))
		for interval in data.split(",")
	]

def part1(data: str):
	intervals = parse_data(data)
	out = 0
	for interval in intervals:
		l, h = interval
		for x in range(l, h + 1):
			x_str = str(x)
			if len(x_str) % 2 != 0:
				continue
			half = len(x_str) // 2
			out += x if x_str[:half] == x_str[half:] else 0
	return out

def part2(data: str) -> int:
	intervals = parse_data(data)

	@cache
	def get_divisors(l: int):
		out = []
		for d in range(1, l // 2 + 1):
			if l % d == 0:
				out.append(d)
		return out

	def is_invalid(x: int):
		x_str = str(x)
		for seq_len in get_divisors(len(x_str)):
			num_sequences = len(x_str) // seq_len
			base = x_str[:seq_len]
			if all([base == x_str[i*seq_len:(i+1)*seq_len] for i in range(1, num_sequences)]):
				return True
		return False

	out = 0
	for interval in intervals:
		l, h = interval
		for x in range(l, h+1):
			out += x if is_invalid(x) else 0
	return out

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