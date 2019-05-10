import data_gen as describers
import genetic
from ops import basic_functions as functions

if __name__ == '__main__':

	print('starting')

	hidden_set = describers.build_hidden_set(size=500)

	# for row in hidden_set[:20]:
	# 	print(row)

	ranker = genetic.get_rank_function(
		hidden_set
		)

	genetic.evolve(
		ranker,
		pop_size=20,
		functions=functions,
		maxgen=50,
		mutation_rate=.5,
		breeding_rate=.5,
		pexp=.5,
		pnew=.1
		)

