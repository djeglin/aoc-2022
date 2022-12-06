import os

class Overlapping_duties:

	def __init__(self, input: list):
		_pairs = [
			{ 
				"a": {"start": int(pair[0].split("-")[0]), "end": int(pair[0].split("-")[1])}, 
				"b": {"start": int(pair[1].split("-")[0]), "end": int(pair[1].split("-")[1])}
			} for pair in [line.strip().split(",") for line in input]
		]
		self._pairs = _pairs
	
	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	@classmethod
	def is_contained(self, pair):
		a = pair.get("a")
		b = pair.get("b")
		if a.get("start") <= b.get("start") and a.get("end") >= b.get("end"):
			return True
		elif b.get("start") <= a.get("start") and b.get("end") >= a.get("end"):
			return True
		else:
			return False
	
	@classmethod
	def is_overlapping(self, pair):
		a = pair.get("a")
		b = pair.get("b")
		if a.get("start") <= b.get("start") <= a.get("end") or \
			a.get("start") <= b.get("end") <= a.get("end") or \
			b.get("start") <= a.get("start") <= b.get("end") or \
			b.get("start") <= a.get("end") <= b.get("end"):
				return True
		else:
			return False
	
	@property
	def contained_pairs(self):
		return [pair for pair in self._pairs if self.is_contained(pair)]

	@property
	def overlapping_pairs(self):
		return [pair for pair in self._pairs if self.is_overlapping(pair)]

def main():
	od = Overlapping_duties.read_file()
	print('Contained pairs:', len(od.contained_pairs))
	print('Overlapping pairs:', len(od.overlapping_pairs))

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))