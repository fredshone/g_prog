import step_gen as describers
import genetic
from ops import basic_functions as functions

if __name__ == '__main__':

	print('starting')

	hidden_set = describers.build_hidden_set(size=10000)

	# for row in hidden_set[:20]:
	# 	print(row)

	ranker = genetic.get_rank_function(
		hidden_set
		)

	genetic.evolve(
		ranker,
		depth=4,
		pop_size=100,
		functions=functions,
		maxgen=100,
		mutation_rate=.3,
		breeding_rate=.6,
		pexp=.5,
		pnew=.1
		)

