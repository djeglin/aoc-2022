import os

class Space_finder:

	def __init__(self, input:list):
		self._raw_input = input
		self.terminal_output = self.parse_input(input)
		self.get_folder_sizes(0)
		

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())

	@classmethod 
	def parse_input(cls, input:list):
		output = []
		for line in input:
			ol = {}
			parts = line.strip().split()
			if line[0] == "$":
				ol["type"] = "command"
				ol["command"] = parts[1]
				if len(parts) > 2:
					ol["folder"] = parts[2]
			elif line[0] == "d":
				ol["type"] = "dir"
				ol["name"] = parts[1]
			else:
				ol["type"] = "file"
				ol["name"] = parts[1]
				ol["size"] = int(parts[0])
			output.append(ol)
		return output
	
	def get_folder_sizes(self, start_index):
		i = start_index + 1
		o = self.terminal_output
		folder_size = 0
		while i < len(o):
			if "folder" in o[i] and o[i]["folder"] == "..":
				self.terminal_output[start_index]["size"] = folder_size
				return folder_size, i + 1
			elif "folder" in o[i]:
				tmp_folder_size, next_index = self.get_folder_sizes(i)
				folder_size += tmp_folder_size
				i = next_index
			elif o[i]["type"] == "file":
				folder_size += o[i]["size"]
				i += 1
			else:
				i += 1
		self.terminal_output[start_index]["size"] = folder_size
		return folder_size, i + 1
	
	def get_folder_with_required_space(self, required: int):
		folders = sorted(self.folder_sizes, key = lambda x: x[1])
		for f in folders:
			if f[1] >= required:
				return f
	
	@property
	def folder_sizes(self):
		return [[f["folder"], f["size"]] for f in self.terminal_output if "size" in f and "folder" in f]

	@property
	def folders_under_100k(self):
		return [f for f in self.folder_sizes if f[1] < 100000]

	@property
	def total_used_space(self):
		return [f[1] for f in self.folder_sizes if f[0] == "/"][0]
	

def main():
	sf = Space_finder.read_file()
	folders_under_100k = sf.folders_under_100k
	print('Sum of folders under 100k:', sum([f[1] for f in folders_under_100k]))
	space_required = 30000000 - (70000000 - sf.total_used_space)
	print('Space required:', space_required)
	folder_to_delete = sf.get_folder_with_required_space(space_required)
	print('Size of folder to delete:', folder_to_delete[1])
	

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))