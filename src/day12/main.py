import os
import math
from collections import deque

class Hill_Climb:

	def __init__(self, input):
		self._raw_input = input
		self.map = [[ch for ch in line.strip()] for line in input]

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	@property
	def start_point(self):
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				if self.map[y][x] == 'S':
					return [y, x]
	
	@property
	def end_point(self):
		for y in range(len(self.map)):
			for x in range(len(self.map[0])):
				if self.map[y][x] == 'E':
					return [y, x]

	def find_path(self, direction):
		end_marker = 'E' if direction == 'up' else 'a'
		start = self.start_point if direction == 'up' else self.end_point
		queue = deque(((start, 0), ))
		shortest_path = {}
		shortest_length = math.inf
		while queue:
			current, steps = queue.popleft()
			next_steps = steps + 1
			y, x = current
			shortest_path[(y, x)] = steps
			if self.map[y][x] == end_marker:
				shortest_length = min(shortest_length, steps)
			for next in self.get_valid_steps(current, direction):
				ny, nx = next
				if (ny, nx) not in shortest_path or shortest_path[(ny, nx)] > next_steps:
					shortest_path[(ny, nx)] = next_steps
					queue.append(((ny, nx), next_steps))
		return shortest_length

	def convert_point(self, level):
		if level == 'S':
			return 'a'
		elif level == 'E':
			return 'z'
		else:
			return level
	
	def check_next_steps(self, current, next, direction):
		c = self.map[current[0]][current[1]]
		n = self.map[next[0]][next[1]]
		a = self.convert_point(c)
		b = self.convert_point(n)
		return ord(b) - ord(a) <= 1 if direction == 'up' else ord(a) - ord(b) <= 1
	
	def get_valid_steps(self, point, direction):
		y, x = point
		y_opts = list(filter(lambda i: i >= 0 and i < len(self.map), [y - 1, y + 1]))
		x_opts = list(filter(lambda i: i >= 0 and i < len(self.map[0]), [x - 1, x + 1]))
		opts = []
		for py in y_opts:
			opts.append([py, x])
		for px in x_opts:
			opts.append([y, px])
		return list(filter(lambda next: self.check_next_steps(point, next, direction), opts))
	

def main():
	hc = Hill_Climb.read_file()
	print('Part 1:', hc.find_path('up'))
	print('Part 2:', hc.find_path('down'))

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))