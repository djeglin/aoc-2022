import os

class CRT:

	def __init__(self, input):
		self._raw_input = input
		self.instructions = [line.strip() for line in input]
		self.register = 1
		self.clock_ticks = 0
		self.signal_strengths = []
		self.instruction_on_stack = ''
		self.output = [[' ' for x in range(40)] for y in range(6)]
		self.pixel_position = [0,0]
		
	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	def run(self):
		while len(self.instructions) > 0:
			self.tick()

	def tick(self):
		self.clock_ticks += 1
		self.signal_strengths.append(self.signal_strength)
		self.draw_pixel()
		if self.instruction_on_stack == '':
			instruction = self.instructions.pop(0)
			self.execute(instruction)
		else:
			instruction = self.instruction_on_stack
			self.register += int(instruction.strip().split()[1])
			self.instruction_on_stack = ''
	
	def execute(self, instruction):
		if instruction == 'noop':
			pass
		else:
			self.instruction_on_stack = instruction
	
	def set_monitor_ticks(self, ticks):
		self.monitor_ticks = ticks

	def draw_pixel(self):
		y, x = self.pixel_position
		r = self.register
		if x in [r - 1, r, r + 1]:
			self.output[y][x] = '#'
		if x == len(self.output[0]) - 1:
			self.pixel_position = [y + 1, 0]
		else:
			self.pixel_position = [y, x + 1]

	
	@property
	def signal_strength(self):
		return self.clock_ticks * self.register
	
	@property
	def monitored_signal_strengths(self):
		return [self.signal_strengths[i-1] for i in self.monitor_ticks]

def main():
	monitor = CRT.read_file()
	monitor.set_monitor_ticks([20, 60, 100, 140, 180, 220])
	monitor.run()
	print(monitor.monitored_signal_strengths)
	print('Signal strength sum:', sum(monitor.monitored_signal_strengths))
	for line in monitor.output:
		print(''.join(line))


if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))