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

pattern = re.compile(r"\[([\.#]+)\] (( ?\([\d,]+\))+) {([\d,]+)}")
activation_table = {'.': '0', '#': '1'}
def parse_data(data: str):
	def transform(line: str):
		m = re.match(pattern, line)
		if m is None: raise ValueError("pattern incompatible with \"{line}\"")
		activation_str, buttons_str, _, joltages = m.groups()
		return (
			"".join(activation_table[c] for c in activation_str),
			list(map(lambda t_str: tuple(map(int, t_str[1:-1].split(","))), buttons_str.split(" "))),
			tuple(map(int, joltages.split(",")))
		)
	return list(map(transform, data.splitlines()))

def part1(data: str):
	# list(map(lambda t: sum(map(lambda x: 1 << (num_lights - x - 1), t)), buttons_plain))
	parsed = parse_data(data)
	out = 0
	def search(target, vals):
		Q = [0]
		V = set()
		count = 0
		while Q:
			new_Q = [] 
			for v in Q:
				if v in V: continue
				if v == target: return count
				V.add(v)
				for delta in vals:
					nxt = v ^ delta
					if nxt not in V: new_Q.append(nxt)
			Q = new_Q
			count += 1
		return -1
	for target_raw, buttons, _ in parsed:
		target = int(target_raw, 2)
		vals = list(map(lambda t: sum(map(lambda x: 1 << (len(target_raw) - x - 1), t)), buttons))
		search_out = search(target, vals)
		out += search_out
	return out

def part2(data: str):
	parsed = parse_data(data)

	# no, i'm NOT going to import numpy!!
	@dataclass(frozen=True)
	class Vector:
		lst: List[int]
		def __add__(self, other): return Vector(list(map(operator.add, self.lst, other.lst)))
		def __sub__(self, other): return Vector(list(map(operator.sub, self.lst, other.lst)))
		def __mul__(self, scalar: int): return Vector(list(map(lambda x: x * scalar, self.lst)))
		def __le__(self, other): return all(a <= b for a, b in zip(self.lst, other.lst))
		def __lt__(self, other): return self.max() < other.max()
		def __eq__(self, other): return self.lst == other.lst
		def __len__(self): return len(self.lst)
		def l1(self): return sum(self.lst)
		def max(self): return max(self.lst)
		def argmax(self): return max(range(len(self.lst)), key=self.lst.__getitem__)
		def __getitem__(self, i): return self.lst[i]
		@staticmethod
		def zero(size: int): return Vector([0 for _ in range(size)])
		def pos_idxs(self): return [i for i, d in enumerate(self.lst) if d > 0]
		def dot(self, A: List['Vector']): return sum(map(lambda c, x: x.__mul__(c), self.lst, A))
		@staticmethod
		def from_idx(idxs: List[int], size: int):
			data = [0 for _ in range(size)]
			for i in idxs:
				data[i] = 1
			return Vector(data)
		def __hash__(self): return hash(tuple(self.lst))

	def gaussian_elimination(A: List[List[int]], b: List[int]):
		m, n = len(A), len(A[0])
		
		M = [A[i] + [b[i]] for i in range(m)]
		pivots = [-1 for _ in range(n)]

		row = 0
		for col in range(n):
			pivot = None
			for r in range(row, m):
				if M[r][col] != 0:
					pivot = r
					break
			if pivot is None: continue
			M[row], M[pivot] = M[pivot], M[row]
			pivots[col] = row

			denominator = M[row][col]
			for r in range(m):
				if r == row: continue
				if M[r][col] == 0: continue
				numerator = M[r][col]
				# instead of division, use denominator * M[r] - numerator * M[row]
				for c in range(col, n + 1):
					M[r][c] = denominator * M[r][c] - numerator * M[row][c]
			row += 1
		for r in range(m):
			if all(M[r][c] == 0 for c in range(n)) and M[r][n] != 0:
				raise ValueError("done messed up bud")
		bound, free = [], []
		for i in range(m):
			if pivots[i] < 0: free.append(i)
			else: bound.append(i)
		return M, (bound, free)
	
	def determine_x_from_free_variables(M, bound: List[int], free: Dict[int, int]):
		m, n = len(M), len(M[0]) - 1
		x = [0 for _ in range(n)]
		for c, v in free.items():
			x[c] = v
		
		# ...

	def ILP(A: List[Vector], y: Vector):
		N = len(A)
		D = len(y)

		v_to_idx = {i: v.pos_idxs() for i, v in enumerate(A)}
		idx_to_v = defaultdict(list)
		for i, ds in v_to_idx.items():
			for d in ds: idx_to_v[d].append(i)
		
		# ideally: iterate over free variables to determine values

		return 

	from tqdm import tqdm

	out = 0
	for _, buttons, joltages in tqdm(parsed):
		N = len(joltages)
		Vs = list(map(lambda b: Vector.from_idx(b, N), buttons))
		J = Vector(list(joltages))
		out += ILP(sorted(Vs, key=lambda x: len(x.pos_idxs()), reverse=True), J)
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