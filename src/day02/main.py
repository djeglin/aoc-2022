import os

class RockPaperScissors:

	def __init__(self, input: list):
		self._rounds = [line.strip().split(' ') for line in input]

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	@classmethod
	def calculate_simple_round_score(self, round):
		move_map = {
			'X': 1,
			'Y': 2,
			'Z': 3
		}
		move = ''.join(round)
		result_score = 0
		if move in ['CX', 'AY', 'BZ']:
			result_score = 6
		elif move in ['AX', 'BY', 'CZ']:
			result_score = 3
		return move_map.get(round[1]) + result_score
	
	@classmethod
	def calculate_complex_round_score(self, round):
		result_map = {
			'X': 0,
			'Y': 3,
			'Z': 6
		}
		response_map = {
			'A': {
				'X': 3,
				'Y': 1,
				'Z': 2
			},
			'B': {
				'X': 1,
				'Y': 2,
				'Z': 3
			},
			'C': {
				'X': 2,
				'Y': 3,
				'Z': 1
			}
		}
		return result_map.get(round[1]) + response_map.get(round[0]).get(round[1])

	@property
	def p1(self):
		return sum([self.calculate_simple_round_score(round) for round in self._rounds])

	@property
	def p2(self):
		return sum([self.calculate_complex_round_score(round) for round in self._rounds])


def main():
		rps = RockPaperScissors.read_file()
		print('PART 1: Total score if following strategy guide:', rps.p1)
		print('PART 2: Total score if following complex strategy guide:', rps.p2)

if __name__ == '__main__':
    import timeit
    print('Executed in', timeit.timeit(main, number=1), 'seconds')
		