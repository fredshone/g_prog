from random import random, randint, choice
from copy import deepcopy
from math import log
from operator import itemgetter
import trees
from trees import Node, Param_node, Const_node
from ops.basic import basic_functions


def hidden_function(x, y):

	return (x * (y + 10)) + ((y + 5) * 2) - 1

def build_hidden_set():
	rows = []
	for i in range(200):
		x = randint(0, 50)
		y = randint(0, 50)
		z = randint(0, 50)
		rows.append([x, y, hidden_function(x, y)])
	return rows


def score_function(tree, s):

	dif = 0
	for data in s:
		v = tree.evaluate([data[0], data[1]])
		dif += abs(v - data[2])
	return dif


def evolve(pc,
			pop_size,
			rank_function,
			functions=basic_functions,
			maxgen=500,
			mutation_rate=.1,
			breeding_rate=.4,
			pexp=.8,
			pnew=.05
		):

	def select_index():
		"""returns random number, reducing pexp reduces random number"""
		return int(log(random())/log(pexp))


	population = [trees.make_random_tree(functions, pc, depth=4) for i in range(pop_size)]

	for i in range(maxgen):
		scores = rank_function(population)
		print(f"gen {i + 1}, av error: {scores[0][0] / 200}")
		if scores[0][0] == 0:
			break

		new_population = [scores[0][1], scores[1][1]]

		while len(new_population) < pop_size:
			if random() > pnew:
				new_population.append(trees.mutate(
					functions,
					pc,
					trees.crossover(scores[select_index()][1],
						scores[select_index()][1],
						p=breeding_rate),
					p=mutation_rate))

			else:
				new_population.append(trees.make_random_tree(functions, pc, depth=3))


		population = new_population

	scores[0][1].display()

	return scores[0][1]


def get_rank_function(dataset):

	def rank_function(population):
		scores = [(score_function(t, dataset), t) for t in population]
		scores.sort(key=itemgetter(0))
		return scores

	return rank_function


if __name__ == '__main__':

	hidden_set = build_hidden_set()
	for row in hidden_set[:20]:
		print(row)

	ranker = get_rank_function(
		hidden_set
		)

	evolve(
		2,
		500,
		ranker,
		functions=basic_functions,
		mutation_rate=.6,
		breeding_rate=.6,
		pexp=.7,
		pnew=.3
		)

	
	




