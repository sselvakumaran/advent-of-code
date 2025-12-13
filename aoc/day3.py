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
	return [map(int, bank) for bank in data.splitlines()]

def part1(data: str):
	banks = parse_data(data)
	out = 0
	for bank in banks:
		batteries = list(enumerate(bank))
		digit10 = max(batteries[:-1], key=lambda t: t[1])
		digit1 = max(batteries[digit10[0]+1:], key=lambda t: t[1])
		out += digit10[1] * 10 + digit1[1]
	return out
		
def part2(data: str) -> int:
	banks = parse_data(data)

	POWERS = list(map(lambda x: pow(10, x), range(0, 13)))
	MAX_VAL = POWERS[12]

	def via_dp(batteries: List[int]):
		N = len(batteries)
		dp = [[-MAX_VAL for _ in range(13)] for _ in range(N)]

		def search(i: int, remaining: int):
			if i >= N:
				return -MAX_VAL if remaining > 0 else 0
			if remaining == 0:
				return 0
			if dp[i][remaining] >= 0:
				return dp[i][remaining]
			out = max(
				batteries[i] * POWERS[remaining - 1] + search(i+1, remaining-1),
				search(i+1, remaining)
			)
			dp[i][remaining] = out
			return out
		return search(0, 12)

	out = 0
	for bank in banks:
		out += via_dp(list(bank))
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