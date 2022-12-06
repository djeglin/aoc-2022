import os

class Handheld:

	def __init__(self, input: str):
		self._buffer = input.strip()
	
	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.read())

	def get_index_with_reqs(self, unique_chars:int):
		idx = -1
		i = 0
		while idx < 0:
			if len(set(self._buffer[i:i + unique_chars])) == unique_chars:
				idx = i
			i += 1
		return idx + unique_chars
	
	@property
	def start_of_packet_index(self):
		return self.get_index_with_reqs(4)

	@property
	def start_of_message_index(self):
		return self.get_index_with_reqs(14)

def main():
	hh = Handheld.read_file()
	print('Start of packet index:', hh.start_of_packet_index)
	print('Start of message index:', hh.start_of_message_index)

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))