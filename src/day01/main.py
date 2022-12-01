import os

class Day:

	def __init__(self, inventory_input: str):
		raw_inventory = [
			[int(item) for item in elves.split('\n')] 
			for elves in inventory_input.strip().split('\n\n') 
		]
		self._inventory = sorted([sum(elf_inventory) for elf_inventory in raw_inventory], reverse=True)

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.read())

	@property
	def most_calories(self):
		return self._inventory[0]

	@property
	def top_3(self):
		return sum(self._inventory[:3])


def main():
    cc = Day.read_file()
    print('Elf with most calories has:', cc.most_calories)
    print('Top 3 elves by calories carried have:', cc.top_3)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))