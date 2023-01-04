import os
import re
import numpy as np
from itertools import zip_longest
from functools import cmp_to_key

class Distress_signal:

	def __init__(self, input):
		self._raw_input = input
		self.input = self.parse_input()

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.read())

	def parse_input(self):
		input = self._raw_input
		pairs = input.split('\n\n')
		pairs = [p.split('\n') for p in pairs]
		for pair in pairs:
			for i in range(len(pair)):
				pair[i], _ = self.parse_array(pair[i])
				# print(pair[i])
		return pairs
				
	def parse_array(self, string, start = 1):
		i = start
		arr = []
		while i < len(string):
			char = string[i]
			if char == '[':
				group, next_index = self.parse_array(string, i + 1)
				arr.append(group)
				i = next_index
			elif char == ']':
				return arr, i + 1
			elif char == ',':
				i += 1
			else:
				next_separator = re.search(r'\D', string[i:]).span()[0] + i
				arr.append(int(string[i:next_separator]))
				i = next_separator
		return arr, i
	
	def check_pair(self, left, right):
		if not right:
			return -1
		left = left if isinstance(left, list) else [left]
		right = right if isinstance(right, list) else [right]
		for ll, rr in zip_longest(left, right, fillvalue = None):
			if ll == None: return 1
			elif rr == None: return -1
			elif isinstance(ll, int) and isinstance(rr, int):
				if rr == ll:
					continue
				return 1 if ll < rr else -1
			else:
				ll = ll if isinstance(ll, list) else [ll]
				rr = rr if isinstance(rr, list) else [rr]
				compare =  self.check_pair(ll, rr)
				if compare in [1, -1]: return compare
		return 0

	@property
	def valid_pairs(self):
		valid_pairs = []
		for i in range(len(self.input)):
			valid = self.check_pair(self.input[i][0], self.input[i][1])
			if valid == 1:
				valid_pairs.append(i+1)
		return valid_pairs

	@property
	def sorted_packets(self):
		all = [[[2]], [[6]]]
		for i in self.input:
			all.append(i[0])
			all.append(i[1])
		output = sorted(all, key=cmp_to_key(self.check_pair), reverse=True)
		return output

	@property
	def decoder_key(self):
		dividers = [[[2]], [[6]]]
		packets = self.sorted_packets
		indices = []
		for i in range(len(packets)):
			if packets[i] in dividers:
				indices.append(i + 1)
		return np.product(indices)
	
	@property
	def valid_pairs_sum(self):
		return sum(self.valid_pairs)



def main():
	ds = Distress_signal.read_file()
	print(ds.valid_pairs)
	print(ds.valid_pairs_sum)
	print(ds.decoder_key)
	
if __name__ == "__main__":
	import timeit
	print(timeit.timeit(main, number=1))
	