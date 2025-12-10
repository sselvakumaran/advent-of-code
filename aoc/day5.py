import sys
import os
import argparse
import re
import bisect

def get_ranges_queries(data: str):
	lines = data.splitlines()
	ranges = []
	queries = []
	range_pattern = re.compile(r"(\d+)-(\d+)")
	for line in lines:
		if len(line) == 0:
			continue
		range_match = re.fullmatch(range_pattern, line)
		if range_match is None:
			queries.append(int(line))
		else:
			ranges.append((int(range_match[1]), int(range_match[2])))
	return ranges, queries

def part1(data: str):
	ranges_unsorted, queries = get_ranges_queries(data)
	# merge ranges
	ranges_sorted = sorted(ranges_unsorted)
	ranges = []
	i, N = 0, len(ranges_sorted)
	while i < N:
		l, r = ranges_sorted[i]
		i += 1
		while i < N and ranges_sorted[i][0] <= r:
			r = max(r, ranges_sorted[i][1])
			i += 1
		ranges.append((l, r))

	lows, highs = list(zip(*ranges))
	count = 0
	for query in queries:
		i = bisect.bisect_right(lows, query)
		if i == 0: continue
		if lows[i - 1] <= query and query <= highs[i-1]:
			count += 1
	return count

def part2(data: str):
	ranges_unsorted, _ = get_ranges_queries(data)
	# merge ranges
	ranges_sorted = sorted(ranges_unsorted)
	i, N = 0, len(ranges_sorted)
	out = 0
	while i < N:
		l, r = ranges_sorted[i]
		i += 1
		while i < N and ranges_sorted[i][0] <= r:
			r = max(r, ranges_sorted[i][1])
			i += 1
		out += (r - l + 1)
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