import sys
import os
import argparse

def part1(data: str):
	lines = data.splitlines()
	M = len(lines)
	N = len(lines[0])
	A = [[0 for _ in range(N)] for _ in range(M)]
	for i, line in enumerate(lines):
		for j, c in enumerate(line):
			A[i][j] = 1 if c == "@" else 0
	out = 0
	DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
	IS_VALID = lambda x, y: x >= 0 and x < M and y >= 0 and y < N
	for i in range(M):
		for j in range(N):
			if A[i][j] == 0:
				continue
			local_count = 0
			for dx, dy in DIRECTIONS:
				x, y = i + dx, j + dy
				if not IS_VALID(x, y): continue
				if A[x][y] == 1:
					local_count += 1
			if local_count < 4:
				out += 1
	return out

def part2(data: str):
	lines = data.splitlines()
	M = len(lines)
	N = len(lines[0])
	DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
	IS_VALID = lambda x, y: x >= 0 and x < M and y >= 0 and y < N

	A = [[0 for _ in range(N)] for _ in range(M)]
	for i, line in enumerate(lines):
		for j, c in enumerate(line):
			A[i][j] = 1 if c == "@" else 0
	
	out = 0
	to_update = [1]
	while to_update:
		to_update = []
		for i in range(M):
			for j in range(N):
				if A[i][j] == 0:
					continue
				local_count = 0
				for dx, dy in DIRECTIONS:
					x, y = i + dx, j + dy
					if not IS_VALID(x, y): continue
					if A[x][y] == 1:
						local_count += 1
				if local_count < 4:
					to_update.append((i, j))
		
		out += len(to_update)
		for i, j in to_update:
			A[i][j] = 0
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