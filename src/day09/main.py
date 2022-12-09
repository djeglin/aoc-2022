import os

class Ropey_Rope:

	def __init__(self, input: list):
		self._raw_input = input
		self.movements = [[line.strip().split()[0], int(line.strip().split()[1])] for line in input]
		self.tail_locations = {'0,0'}
		self.knots = []

	
	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	def create_knots(self, count):
		self.knots = [[0,0] for i in range(count)]

	def move(self, instruction):
		direction, distance = instruction
		for _ in range(distance):
			if direction == 'R':
				self.knots[0][1] += 1
			elif direction == 'L':
				self.knots[0][1] -= 1
			elif direction == 'U':
				self.knots[0][0] -= 1
			elif direction == 'D':
				self.knots[0][0] += 1
			
			for k in range(1, len(self.knots)):
				self.knots[k] = self.move_tail(self.knots[k - 1], self.knots[k])
				
				if k == len(self.knots) - 1:
					self.tail_locations.add(",".join([str(i) for i in self.knots[-1]]))

	def move_tail(self, head, tail):
		diff_y = head[0] - tail[0]
		diff_x = head[1] - tail[1]
		if -1 <= diff_y <= 1 and -1 <= diff_x <= 1:
			return tail
		# diagonal motion
		if diff_y >= 1 and diff_x >= 1:
			return [tail[0] + 1, tail[1] + 1]
		elif diff_y >= 1 and diff_x <= -1:
			return [tail[0] + 1, tail[1] - 1]
		elif diff_y <= -1 and diff_x >= 1:
			return [tail[0] - 1, tail[1] + 1]
		elif diff_y <= -1 and diff_x <= -1:
			return [tail[0] - 1, tail[1] - 1]
		# vertical motion
		elif diff_y > 1 and diff_x == 0:
			return [tail[0] + 1, tail[1]]
		elif diff_y < -1 and diff_x == 0:
			return [tail[0] - 1, tail[1]]
		# horizontal motion
		elif diff_y == 0 and diff_x > 1:
			return [tail[0], tail[1] + 1]
		elif diff_y == 0 and diff_x < -1:
			return [tail[0], tail[1] - 1]
		
	
	@property
	def visited_tail_positions(self):
		return len(self.tail_locations)
	

def main():
	p1 = Ropey_Rope.read_file()
	p1.create_knots(2)
	for m in p1.movements:
		p1.move(m)
	print('Tail positions with only 2 knots:', p1.visited_tail_positions)
	p2 = Ropey_Rope.read_file()
	p2.create_knots(10)
	for m in p2.movements:
		p2.move(m)
	print('Tail positions with 10 knots:', p2.visited_tail_positions)
	

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))