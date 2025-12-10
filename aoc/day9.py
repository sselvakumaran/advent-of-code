import sys
import os
import argparse
import re
import bisect
from functools import reduce
import operator
import itertools
from dataclasses import dataclass
import heapq
from collections import Counter

def parse_data(data: str):
	return [tuple(map(int, line.split(","))) for line in data.splitlines()]

def part1(data: str):
	points = parse_data(data)
	def area(p1p2):
		p1, p2 = p1p2
		x1, y1 = p1
		x2, y2 = p2
		l_x = max(x1, x2) - min(x1, x2) + 1
		l_y = max(y1, y2) - min(y1, y2) + 1
		return l_x * l_y
	best = max(
		itertools.combinations(points, 2), 
		key=area)
	return area(best)

def part2(data: str):
	points = parse_data(data)
	# compress the points
	Xs = sorted(set(map(lambda t: t[0], points)))
	Ys = sorted(set(map(lambda t: t[1], points)))
	rev_Xs = {x: i for i, x in enumerate(Xs)}
	rev_Ys = {y: i for i, y in enumerate(Ys)}
	M, N = len(Xs), len(Ys)
	pts = list(map(lambda t: (rev_Xs[t[0]], rev_Ys[t[1]]), points))

	A = [[1 for _ in range(N)] for _ in range(M)]
	for pairs in itertools.pairwise(pts + pts[:1]):
		p1, p2 = pairs
		x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
		y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
		if x1 == x2:
			for y in range(y1, y2 + 1):
				A[x1][y] = 2
		if y1 == y2:
			for x in range(x1, x2 + 1):
				A[x][y1] = 2

	Q = [(0, 0), (0, N - 1), (M - 1, 0), (M - 1, N - 1)]

	while Q:
		x, y = Q.pop()
		if x < 0 or x >= M or y < 0 or y >= N or A[x][y] != 1:
			continue
		A[x][y] = 0
		Q.extend([(x, y-1), (x, y+1), (x-1, y), (x+1, y)])
	
	B = [[0 for _ in range(N+1)] for _ in range(M+1)]
	for x in range(M):
		for y in range(N):
			B[x+1][y+1] = B[x+1][y] + B[x][y+1] - B[x][y] + (1 if A[x][y] > 0 else 0)
	
	def area(p1, p2):
		x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
		y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
		return (x2 - x1 + 1) * (y2 - y1 + 1)
	
	def is_valid_rectangle(p1, p2):
		x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
		y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
		return (B[x2+1][y2+1] - B[x1][y2+1] - B[x2+1][y1] + B[x1][y1]) == area(p1, p2)
	
	to_real = lambda t: (Xs[t[0]], Ys[t[1]])
	def real_area(p1, p2):
		return area(to_real(p1), to_real(p2))

	best = max(
		filter(
			lambda t: is_valid_rectangle(*t), 
			itertools.combinations(pts, 2)),
		key=lambda t: real_area(*t))
	return real_area(*best)

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