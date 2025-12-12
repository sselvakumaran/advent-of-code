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

def part2(data: str) -> int:

	LARGE = Fraction(10**10)
	def row_sub(target: List[Fraction], source: List[Fraction], factor: Fraction) -> None:
		for j in range(len(target)):
			target[j] -= factor * source[j]

	def row_scale(row: List[Fraction], divisor: Fraction) -> None:
		for j in range(len(row)):
			row[j] /= divisor

	def pivot(tableau: List[List[Fraction]], row: int, col: int) -> None:
		row_scale(tableau[row], tableau[row][col])
		for r in range(len(tableau)):
			if r != row and tableau[r][col] != 0:
				row_sub(tableau[r], tableau[row], tableau[r][col])


	def simplex(A: List[List[int]], b: List[int]) -> Optional[Tuple[List[Fraction], Fraction]]:
		m, n = len(A), len(A[0])

		tableau = [
			[Fraction(A[i][j]) for j in range(n)]
			+ [Fraction(1 if i == k else 0) for k in range(m)]
			+ [Fraction(b[i])]
			for i in range(m)
		]

		basis = list(range(n, n + m))
		obj = [Fraction(0) for _ in range(n)] + [Fraction(1) for _ in range(m)] + [Fraction(0)]

		for row in tableau:
			row_sub(obj, row, Fraction(1))
		tableau.append(obj)

		while True:
			entering = min(range(n + m), key=lambda j: tableau[-1][j])
			if tableau[-1][entering] >= 0:
				break

			leaving, best_ratio = None, None
			for i in range(m):
				if tableau[i][entering] > 0:
					ratio = tableau[i][-1] / tableau[i][entering]
					if best_ratio is None or ratio < best_ratio:
						leaving, best_ratio = i, ratio

			if leaving is None:
				return None

			pivot(tableau, leaving, entering)
			basis[leaving] = entering

		if tableau[-1][-1] < 0:
			return None

		for i, basis_var in enumerate(basis):
			if basis_var >= n:
				for j in range(n):
					if tableau[i][j] != 0:
						pivot(tableau, i, j)
						basis[i] = j
						break

		tableau[-1] = [Fraction(1) for _ in range(n)] + [Fraction(0) for _ in range(m+1)]
		for i, basis_var in enumerate(basis):
			if tableau[-1][basis_var] != 0:
				row_sub(tableau[-1], tableau[i], tableau[-1][basis_var])

		while True:
			entering = min(range(n), key=lambda c: tableau[-1][c])
			if tableau[-1][entering] >= 0:
				break

			leaving, best_ratio = None, None
			for i in range(m):
				if tableau[i][entering] > 0:
					ratio = tableau[i][-1] / tableau[i][entering]
					if best_ratio is None or ratio < best_ratio:
						leaving, best_ratio = i, ratio

			if leaving is None:
				return None

			pivot(tableau, leaving, entering)
			basis[leaving] = entering

		x = [Fraction(0) for _ in range(n)]
		for i, basis_var in enumerate(basis):
			if basis_var < n:
				x[basis_var] = tableau[i][-1]

		return x, sum(x)

	def lp_with_bounds(
		A: List[List[int]],
		b: List[int],
		lb: List[int],
		ub: List[Optional[int]],
	) -> Optional[Tuple[List[Fraction], Fraction]]:
		m, n = len(A), len(A[0])

		lb_constraints = [(j, lb[j]) for j in range(n) if lb[j] > 0]
		ub_constraints = [(j, ub[j]) for j in range(n) if ub[j] is not None]

		n_aug = n + len(lb_constraints) + len(ub_constraints)

		A_aug = [row + [0 for _ in range(n_aug - n)] for row in A]
		b_aug = b.copy()

		for i, (j, val) in enumerate(lb_constraints):
			row = [0 for _ in range(n_aug)]
			row[j] = 1
			row[n + i] = -1
			A_aug.append(row)
			b_aug.append(val)

		for i, (j, val) in enumerate(ub_constraints):
			row = [0 for _ in range(n_aug)]
			row[j] = 1
			row[n + len(lb_constraints) + i] = 1
			A_aug.append(row)
			b_aug.append(val)

		result = simplex(A_aug, b_aug)
		if result is None:
			return None

		x_aug, _ = result
		return x_aug[:n], sum(x_aug[:n])

	def ilp(A: List[List[int]], b: List[int]) -> int:
		n = len(A[0])
		best_obj: Fraction = LARGE

		def branch_and_bound(lb: List[int], ub: List[Optional[int]]) -> None:
			nonlocal best_obj

			result = lp_with_bounds(A, b, lb, ub)
			if result is None:
				return

			x_lp, obj_lp = result
			if obj_lp >= best_obj:
				return

			frac_idx = next((j for j in range(n) if x_lp[j].denominator != 1), None)

			if frac_idx is None:
				best_obj = min(obj_lp, best_obj)
				return

			floor_val = int(x_lp[frac_idx])

			ub_branch = ub.copy()
			ub_branch[frac_idx] = floor_val if ub[frac_idx] is None else min(ub[frac_idx], floor_val)
			branch_and_bound(lb, ub_branch)

			lb_branch = lb.copy()
			lb_branch[frac_idx] = floor_val + 1
			branch_and_bound(lb_branch, ub)

		branch_and_bound([0 for _ in range(n)], [None for _ in range(n)])

		if best_obj >= LARGE:
			raise ValueError("No feasible integer solution found")

		return int(best_obj)


	parsed = parse_data(data)
	total = 0
	for _, buttons, joltages in parsed:
		num_joltages, num_buttons = len(joltages), len(buttons)

		A = [[0 for _ in range(num_buttons)] for _ in range(num_joltages)]
		for col, button_set in enumerate(buttons):
			for row in button_set:
				A[row][col] = 1

		total += ilp(A, list(joltages))

	return total

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