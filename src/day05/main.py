import os
from itertools import zip_longest
from collections import deque

class Moving_crates:

	def __init__(self, input):
		self._stacks = self.parse_stacks(input)
		self._instructions = self.parse_instructions(input)

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f)
	
	@classmethod
	def parse_stacks(self, input):
		stacks = []
		while (line := next(input).rstrip())[1] != '1':
			stacks.insert(0, [line[i] for i in range(1, len(line), 4)])
		stacks = list(zip_longest(*stacks, fillvalue=' '))
		return [deque([crate for crate in stack if crate != ' ']) for stack in stacks]

	@classmethod
	def parse_instructions(self, input):
		instructions = []
		for line in input.readlines():
			if line.startswith('move'):
				segs = line.split()
				instructions.append({"q": int(segs[1]), "f": int(segs[3]), "t": int(segs[5])})
		return instructions
	
	def execute_instructions(self, multi = False):
		for instruction in self._instructions:
			if multi:
				self.move_multiple_crates(instruction)
			else:
				for i in range(instruction["q"]):
					self.move_single_crate(instruction["f"], instruction["t"])

	def move_single_crate(self, from_stack, to_stack):
		self._stacks[to_stack - 1].append(self._stacks[from_stack - 1].pop())

	def move_multiple_crates(self, instruction):
		q, f, t = instruction.values()
		from_stack = list(self._stacks[f - 1])
		to_stack = list(self._stacks[t - 1])
		to_stack.extend(from_stack[-q:])
		self._stacks[t - 1] = deque(to_stack)
		del from_stack[-q:]
		self._stacks[f - 1] = deque(from_stack)

	@property
	def top_crates(self):
		return [stack[-1] for stack in self._stacks]


def main():
	cm9000 = Moving_crates.read_file()
	print("Starting top crates:", ''.join(cm9000.top_crates))
	cm9000.execute_instructions(False)
	print("CM9000 Finishing top crates:", ''.join(cm9000.top_crates))
	cm9001 = Moving_crates.read_file()
	cm9001.execute_instructions(True)
	print("CM9001 Finishing top crates:", ''.join(cm9001.top_crates))


if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))