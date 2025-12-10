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
from collections import Counter
from typing import List, Optional, Tuple

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
	
	# ESTIMATOR - DOES NOT FIND GLOBAL MINIMUM
	def greedy(A: List[Vector], y: Vector):
		N = len(y)
		y_hat = Vector.zero(N)
		dims_required = set(range(N))
		count = 0
		def greed_factor(v):
			nonlocal dims_required
			idxs = v.nonzero_idxs()
			return (len(set(v.nonzero_idxs()) & dims_required), -len(idxs))
		while dims_required:
			# find A that covers the most dimensions within dims_required
			v = max(A, key=greed_factor)
			# c = minimum amount to fulfill all deficits / maximum deficit
			c = (y - y_hat).max()
			y_hat = y_hat + (v * c)
			dims_required.difference_update(v.pos_idxs())
			count += c
		return count

	# use DFS, however update so one action is adding maximum without exceeding bounds
	# for each vector, find maximum it can be used without going over bounds
	"""
(3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
 0 1 2 3 4 5
[0 0 0 0 1 1] x >= 3
[0 1 0 0 0 1] x >= 5
[0 0 1 1 1 0] x >= 4
[1 1 0 1 0 0] x >= 7
x4 + x5 >= 3
x1 + x5 >= 5
x2 + x3 + x4 >= 3
x0 + x1 + x3 >= 7

bind v0 = x0 + x1 + x3
v0 >= 7
bind v1 = 

"""
	def ILP(A: List[Vector], y: Vector):
		N = len(A)
		D = len(y)

		best_cost = greedy(A, y)
		# g, cost, x, y_hat
		# note: g = cost + max(remaining_deficits)
		Q = [(0, 0, Vector.zero(), Vector.zero())]
		while Q:
			_, cost, x, y_hat = heapq.heappop(Q)
			if y <= y_hat:
				best_cost = min(best_cost, cost)
				continue
			deficits: Vector = (y - y_hat)
			# ... something here

			# dont add if cost is too high (> best_cost)



		# def dfs(x: Vector, y_hat: Vector, cost: int):
		# 	nonlocal best_cost
		# 	if cost >= best_cost: return
		# 	if y <= y_hat: best_cost = min(best_cost, cost)
		# 	deficits = (y - y_hat)
			
		# 	# for all nonzero deficits,
		# 	pass

		return best_cost

	out = 0
	for _, buttons, joltages in parsed:
		N = len(joltages)
		Vs = list(map(lambda b: Vector.from_idx(b, N), buttons))
		J = Vector(list(joltages))
		print(greedy(Vs, J))
		#out += sum(ILP(Vs, J))
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