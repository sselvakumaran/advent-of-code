import sys
import os
import argparse
import re
import bisect
from functools import reduce
import operator
from itertools import zip_longest

def part1(data: str):
	lines = [line.split() for line in data.splitlines()]
	out = 0
	problems = zip(*lines)
	for problem in problems:
		vals, op = map(int, problem[:-1]), problem[-1]
		if op == '+':
			out += reduce(operator.add, vals, 0)
		elif op == '*':
			out += reduce(operator.mul, vals, 1)
		else:
			raise ValueError(f"FAIL! operator not recognized: {problem[-1]}")
	return out

def part2(data: str):
	lines = data.splitlines()
	op_line = lines[-1]
	problems = []
	i = 0
	N = len(lines) - 1
	while i < len(op_line):
		j = i + 1
		while j < len(op_line) and op_line[j] == ' ':
			j += 1
		problem_len = j - i - (1 if j < len(op_line) else 0)
		nums = []
		for problem_i in range(i, i + problem_len):
			num = ''
			for problem_j in range(0, N):
				num += lines[problem_j][problem_i]
			nums.append(int(num.strip()))
		problems.append((
			nums,
			op_line[i]
		))
		i = j
	out = 0

	for problem in problems:
		vals, op = problem[0], problem[1]
		if op == '+':
			out += reduce(operator.add, vals, 0)
		elif op == '*':
			out += reduce(operator.mul, vals, 1)
		else:
			raise ValueError(f"FAIL! operator not recognized: {problem[-1]}")
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