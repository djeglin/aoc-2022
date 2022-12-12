import os
import math
import functools
from itertools import groupby

class Monkey_business:

	def __init__(self, input):
		self._raw_input = input
		self.monkeys = self.parse_input(input)
		
	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	def parse_input(self, input):
		input = self._raw_input
		monkeys_list = [list(g) for k, g in groupby(input, lambda x: x == "\n") if not k]
		monkeys = []
		for m in monkeys_list:
			monkey = {}
			monkey["items"] = list(map(int, m[1].strip().split(': ')[1].split(', ')))
			operand = m[2].strip().split(' ')[-1]
			monkey["operation"] = { 
				"operator" : "multiply" if m[2].find('*') > -1 else "add", 
				"operand" : operand if operand == 'old' else int(operand)
			}
			monkey["test"] = {
				"divisor" : int(m[3].strip().split('divisible by ')[1]),
				"true_target": int(m[4].strip().split('monkey ')[1]),
				"false_target": int(m[5].strip().split('monkey ')[1])
			}
			monkey["inspection_count"] = 0
			monkeys.append(monkey)
		return monkeys
	
	def do_round(self, relieve):
		for m in range(len(self.monkeys)):
			self.take_turn(m, relieve)
	
	def take_turn(self, i, relieve):
		m = self.monkeys[i]
		while len(m["items"]) > 0:
			self.monkeys[i]["inspection_count"] += 1
			item = m["items"].pop(0)
			item = self.do_operation(item, m["operation"])
			if relieve:
				item = math.trunc(item / 3)
			else:
				item = item % self.common_divisor
			target = self.get_target(item, m["test"])
			self.monkeys[target]["items"].append(item)

	def do_operation(self, item, operation):
		operator, operand = operation.values()
		if operator == "multiply":
			return item * item if operand == 'old' else item * operand
		else:
			return item + operand
	
	def get_target(self, item, test):
		divisor, true_target, false_target = test.values()
		if item % divisor == 0:
			return true_target
		else:
			return false_target
	
	@property
	def monkey_inspection_counts(self):
		return list(sorted([m["inspection_count"] for m in self.monkeys], reverse=True))

	@property
	def monkey_business_total(self):
		counts = self.monkey_inspection_counts
		return counts[0] * counts[1]
	
	@property
	def common_divisor(self):
		return functools.reduce(lambda cd, x: cd * x, (m["test"]["divisor"] for m in self.monkeys))

	
def main():
	p1 = Monkey_business.read_file()
	for _ in range(20):
		p1.do_round(True)
	print("Part 1 – Monkey business after 20 rounds:", p1.monkey_business_total)
	p2 = Monkey_business.read_file()
	for _ in range(10000):
		p2.do_round(False)
	print("Part 2 – Monkey business after 10000 rounds:", p2.monkey_business_total)


if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))