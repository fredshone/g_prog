from random import random, randint, choice
from copy import deepcopy
from math import log


class Function_wrapper:
	"""
	wrapper for node operations
	"""

	def __init__(self, function, types_in, type_out, name):
		self.f = function
		self.childcount = len(types_in)
		self.types_in = types_in
		self.type_out = type_out
		self.name = name


class Node:

	def __init__(self, function_wrapper, children):
		self.function = function_wrapper.f
		self.types_in = function_wrapper.types_in
		self.type_out = function_wrapper.type_out
		self.name = function_wrapper.name
		self.children = children

	def evaluate(self, input):
		results = [n.evaluate(input) for n in self.children]
		return self.function(results)

	def display(self, indent=0):
		print(('  ' * indent) + self.name)
		for c in self.children:
			c.display(indent + 1)


class Param_node:

	def __init__(self, idx):
		self.idx = idx
		self.type_out = 'int'

	def evaluate(self, input):
		return input[self.idx]

	def display(self, indent=0):
		print(f"{'  ' * indent}p{str(self.idx)}")


class Const_node:

	def __init__(self, v):
		self.v = v
		self.type_out = 'int'

	def evaluate(self, input):
		return self.v

	def mutate(self):
		self.v += choice([-1, 1])

	def display(self, indent=0):
		print(f"{'  ' * indent}{str(self.v)}")


integer_nodes = [Param_node, Const_node]


def make_random_tree(functions, pc, out_type='int', depth=2, fpr=.5, ppr=.6):
	
	# make list of available functions for input to last node
	available_functions = functions.get(out_type)

	if random() < fpr and depth > 0:
		f = choice(available_functions)

		children = []  # TODO convert to list comp
		for in_type in f.types_in:
			children.append(make_random_tree(functions, pc, in_type, depth - 1, fpr, ppr))
		return Node(f, children)

	elif random() < ppr:
		return Param_node(randint(0, pc - 1))

	else:
		return Const_node(randint(0, 10))


def mutate(functions, pc, tree, p=.1, pt=.5):

	if random() < p:
		if isinstance(tree, Const_node) and random() < pt:
			tree.mutate()
			return tree
		else:
			return make_random_tree(
				functions,
				pc,
				depth=choice([1, 2, 3, 4]),
				out_type=tree.type_out
			)
	else:
		result = deepcopy(tree)

		if isinstance(tree, Node):
			result.children = [
				mutate(functions, pc, child, p) for child in tree.children
			]

		return result


def minor_mutate(tree, p=.5):

	result = deepcopy(tree)

	if isinstance(result, Const_node) and random() < p:
		result.mutate()
		return result

	else:

		if isinstance(result, Node):
			result.children = [
				minor_mutate(child, p) for child in tree.children
			]

		return result


def crossover(tree1, tree2, p=.4, top=1):

	if random() < p and not top and tree2.type_out == tree1.type_out:
		return deepcopy(tree2)
	else:
		result = deepcopy(tree1)
		if isinstance(tree1, Node) and isinstance(tree2, Node):
			result.children = [crossover(c, choice(tree2.children), p, 0)
			for c in tree1.children]

		return result


def calc_size(node):

	if not isinstance(node, Node):

		return 1, 1

	else:

		size = 0
		depths = []

		for child in node.children:

			child_size, child_depth = calc_size(child)

			size += child_size 
			depths.append(child_depth)

		return size + 1, max(depths) + 1






