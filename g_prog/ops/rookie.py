import trees
import describers


print(__name__)


def if_function(i):

	if i[0] > 0:
		return i[1]
	else:
		return i[2]


def is_greater(i):

	if i[0] > i[1]:
		return 1
	else:
		return 0


def is_lesser(i):

	if i[0] < i[1]:
		return 1
	else:
		return 0


def is_between(i):

	if i[1] < i[0] < i[2]:
		return i[3]
	else:
		return i[4]


adder = trees.Function_wrapper(lambda i: i[0] + i[1], ['int', 'int'], 'int', '+')
subber = trees.Function_wrapper(lambda i: i[0] - i[1], ['int', 'int'], 'int', '-')
multiplier = trees.Function_wrapper(lambda i: i[0] * i[1], ['int', 'int'], 'int', '*')
absoluter = trees.Function_wrapper(lambda i: abs(i[0]), ['int'], 'int', 'abs')
iffer = trees.Function_wrapper(if_function, ['int', 'int', 'int'], 'int', 'if')
greater = trees.Function_wrapper(is_greater, ['int', 'int'], 'int', 'is greater')
lesser = trees.Function_wrapper(is_lesser, ['int', 'int'], 'int', 'is less')
between = trees.Function_wrapper(is_between, ['int', 'int', 'int', 'int', 'int'], 'int', 'is between')
negative = trees.Function_wrapper(lambda i: - i[0], ['int'], 'int', 'negative')


basic_functions = {
	'int':
	[
	adder,
	subber,
	multiplier,
	absoluter,
	iffer,
	greater,
	lesser,
	between,
	negative
	]
}


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

	print('building rank function')

	def rank_function(population):
		scores = [(describers.score_function(t, dataset), t) for t in population]
		scores.sort(key=itemgetter(0))
		return scores

	return rank_function


if __name__ == '__main__':

	print('starting')

	hidden_set = describers.build_hidden_set()

	print('hidden set:')

	for row in hidden_set[:20]:
		print(row)

	print('building rank function:')
	ranker = get_rank_function(
		hidden_set
		)

	evolve(
		7,
		500,
		ranker,
		functions=basic_functions,
		mutation_rate=.6,
		breeding_rate=.6,
		pexp=.7,
		pnew=.3
		)

