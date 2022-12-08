import os

class Tree_Finder:

	def __init__(self, input):
		self._raw_input = input
		self.tree_map = [[int(i) for i in line.strip()] for line in input]

	@classmethod
	def read_file(cls):
		absolute_path = os.path.dirname(os.path.abspath(__file__))
		filename = absolute_path + "/input.txt"
		with open(filename) as f:
			return cls(f.readlines())
	
	def get_compass_trees(self, y, x):
		w_trees = list(reversed(self.tree_map[y][:x]))
		e_trees = self.tree_map[y][x+1:]
		n_trees = list(reversed([row[x] for row in self.tree_map[:y]]))
		s_trees = [row[x] for row in self.tree_map[y+1:]]
		return w_trees, e_trees, n_trees, s_trees

	def tree_is_visible(self, y, x):
		if 0 in (y,x) or y == len(self.tree_map) - 1 or x == len(self.tree_map[0]) - 1:
			return False # we deal with perimeter trees separately, so don't count them again
		tree = self.tree_map[y][x]
		w_trees, e_trees, n_trees, s_trees = self.get_compass_trees(y,x)
		if all(t < tree for t in w_trees) or \
			all(t < tree for t in e_trees) or \
			all(t < tree for t in n_trees) or \
			all(t < tree for t in s_trees):
			return True
		else:
			return False
	
	def get_scenic_score(self, y, x):
		tree = self.tree_map[y][x]
		w_trees, e_trees, n_trees, s_trees = self.get_compass_trees(y,x)
		w_score = self.get_direction_score(w_trees, tree)
		e_score = self.get_direction_score(e_trees, tree)
		n_score = self.get_direction_score(n_trees, tree)
		s_score = self.get_direction_score(s_trees, tree)
		return w_score * e_score * n_score * s_score
	
	@classmethod
	def get_direction_score(cls, trees, tree):
		for i in range(len(trees)):
			if trees[i] >= tree:
				return i + 1
		return len(trees)
	
	@property
	def visible_trees(self):
		return [[y,x] for x in range(len(self.tree_map[0])) for y in range(len(self.tree_map)) if self.tree_is_visible(y,x)]

	@property
	def perimeter(self):
		x_len = len(self.tree_map[0])
		y_len = len(self.tree_map)
		return x_len * 2 + y_len * 2 - 4
	
	@property
	def scenic_score_map(self):
		return [[self.get_scenic_score(y,x) for x in range(len(self.tree_map[0]))] for y in range(len(self.tree_map))]
	
	@property
	def max_scenic_score(self):
		return max([max(row) for row in self.scenic_score_map])


def main():
	tf = Tree_Finder.read_file()
	print("Perimeter:", tf.perimeter)
	print("Visible trees:", len(tf.visible_trees))
	print("Total visible trees:", tf.perimeter + len(tf.visible_trees))
	print("Max scenic score:", tf.max_scenic_score)

if __name__ == '__main__':
	import timeit
	print(timeit.timeit(main, number=1))