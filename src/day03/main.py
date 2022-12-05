import os
import string

class Rucksack_rearrangement:

	def __init__(self, rucksacks_input: str):
		raw_rucksacks = [list(rucksack.strip()) for rucksack in rucksacks_input]
		_rucksacks = []
		for rucksack in raw_rucksacks:
			half_point = len(rucksack) // 2
			_rucksacks.append([list(rucksack[:half_point]), list(rucksack[half_point:])])
		_elf_groups = []
		for i in range(0, len(raw_rucksacks), 3):
			_elf_groups.append(raw_rucksacks[i:i+3])
		self.rucksacks = _rucksacks
		self.elf_groups = _elf_groups

	_alphabet=list(string.ascii_lowercase)

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())
	
	@classmethod
	def get_common_item(self, group):
		sets = [set(subgroup) for subgroup in group]
		intersection = sets[0].intersection(*sets)
		return list(intersection)[0]

	@classmethod
	def get_priority(self, letter):
		priority_start = 27 if letter.isupper() else 1
		return self._alphabet.index(letter.lower()) + priority_start

	@property
	def missorted_item_priority(self):
		common_items = [self.get_common_item(rucksack) for rucksack in self.rucksacks]
		return sum(map(self.get_priority, common_items))

	@property
	def elf_group_priority(self):
		stickers = [self.get_common_item(group) for group in self.elf_groups]
		return sum(map(self.get_priority, stickers))


def main():
		rr = Rucksack_rearrangement.read_file()
		print('Missorted item priority:', rr.missorted_item_priority)
		print('Elf group priority:', rr.elf_group_priority)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))