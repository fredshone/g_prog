import trees
from ops import basic_functions as functions
import data_gen as describers


from operator import itemgetter
from random import random
from math import log
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Generation:

	def __init__(self, pop_size, functions, inputs, depth=3):

		self.pop_size = pop_size
		self.functions = functions
		self.inputs = inputs
		self.depth = depth

		self.population = None
		self.scores = None

	def spawn(self):

		self.population = [trees.make_random_tree(self.functions, self.inputs, depth=self.depth) for i in range(self.pop_size)]

	def score(self, rank_function):

		self.scores = rank_function(self.population)

		return [s for s, t in self.scores]

	def reproduce(self,
					ancestors,
					pnew,
					select_index,
					breeding_rate,
					mutation_rate):

		# elitism
		top = int(self.pop_size * 0.2)
		self.population = [
			ancestors.scores[i][1] for i in range(top)
		]

		# minor mutation of elites
		for elite in [
			ancestors.scores[i][1] for i in range(top)
		]:
			self.population.append(
				trees.minor_mutate(
					elite,
					p=.5
				)
			)

		while len(self.population) < self.pop_size:
			if random() > pnew:
				self.population.append(
					trees.mutate(
						self.functions,
						self.inputs,
						trees.crossover(
							ancestors.scores[select_index()][1],
							ancestors.scores[select_index()][1],
							p=breeding_rate),
						p=mutation_rate,
						pt=ancestors.scores[0][0]
					)
				)

			else:
				self.population.append(trees.make_random_tree(self.functions, self.inputs, depth=self.depth))

	def display(self, i):

		scores = np.array([s[0] for s in self.scores])

		best = max(scores)
		worst = min(scores)
		av = np.mean(scores)

		size, depth = trees.calc_size(self.scores[0][1])

		print(f"\ngen {i + 1}, best: {scores[0]}, size: {size}, depth: {depth}. average:{av}")
		# for rank in range(len(self.population)):
		# 	size, depth = trees.calc_size(self.scores[rank][1])
		# 	print(f"\trank {rank}: {scores[rank]}, size: {size}, depth: {depth}.")

		# self.scores[0][1].display()


def evolve(rank_function,
			inputs=6,
			depth=3,
			pop_size=1000,
			functions=functions,
			maxgen=100,
			mutation_rate=.1,
			breeding_rate=.4,
			pexp=.8,
			pnew=.05
		):

	def select_index():
		"""returns random number, reducing pexp reduces random number"""
		return int(log(random())/log(pexp))

	fig, ax = plt.subplots()
	scores = []

	population = Generation(pop_size, functions, inputs, depth)
	population.spawn()
	fitnesses = population.score(rank_function)
	scores.append(fitnesses)
	plt.plot(scores, 'r-')
	plt.pause(0.001)

	for i in range(maxgen):

		population.display(i)

		if population.scores[0][0] == 1:
			break

		new_population = Generation(pop_size, functions, inputs, depth)

		new_population.reproduce(population,
									pnew,
									select_index,
									breeding_rate,
									mutation_rate)

		population = new_population

		scores.append(population.score(rank_function))

		plt.plot(scores, 'r-')
		plt.pause(0.001)

		population.scores[0][1].display()

	population.scores[0][1].display()
	plt.show()


def get_rank_function(dataset):

	def rank_function(population):
		scores = [(describers.score_function(t, dataset), t) for t in population]
		scores.sort(key=itemgetter(0), reverse=True)
		return scores

	return rank_function
