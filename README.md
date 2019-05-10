# Genetic Programming

*Experiments with applying genetic programming for learning matching rules...*

Given a two strings can genetic programming be used to learn some hidden matching rule?


#### Test Data

We generate sample strings using `data_gen.py`, this format is based on Network Rail Berth Describer ids:
```
def get_describer():
	return get_char(k=2) + '_' + get_num(k=4)
```
Pairs of these strings are generated for the final 'hidden' set (~training data). Pairs are either matching or mismatching (50/50). A mismatched pair are both randomly generated. A match is generated from a given string using a `tweak_describer`:
```
def tweak_describer(sample):
	shifts = choices([-1, 1], k=3)
	return get_char(k=2) + '_' + get_num()\
	+ str(int(sample[-3:]) + shifts[0])\
	+ str(int(sample[-2:]) + shifts[1])\
	+ str(int(sample[-1:]) + shifts[2])
``` 
For each pair a feature is generated from the difference between each Unicode code point of each character:
```
def build_features(sample1, sample2):
	return [ord(a) - ord(b) for a, b in zip(sample1, sample2)]
```
Hence, for example, a generated matching pair of "AA_1234" and "ZX_1325" is represented by the feature [-25, -23, 0, 0, -1, 1, -1].
#### Algorithm Graphs 'Trees'

Matching algorithms are assembled from graphs (DAGs) of operations, here referred to as 'algorithm trees'. Where operations are represented as vertices in the trees.

Operations are integer based although type sensitive trees are supported:
```
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
```
Operations have varying complexity and number of inputs, for example:
```
negative = trees.Function_wrapper(lambda i: - i[0], ['int'], 'int', 'negative')
```
```
def is_between(i):

	if i[1] < i[0] < i[2]:
		return i[3]
	else:
		return i[4]
		
between = trees.Function_wrapper(is_between, ['int', 'int', 'int', 'int', 'int'], 'int', 'is between')
```
Trees are generated randomly and then combined and mutated using a number of recursive functions as required by the genetic optimising algorithm.

#### Evolution

An optimum algorithm tree is searched for using a genetic optimising algorithm. Generations of candidate solutions are generated and then iteratively modified based on fitness. Where fitness is based on how well the algorithm tree solves the matching problem.

The iterative modification between each generation uses elitism and fitness based breeding to move towards an optima, combined with mutation and random generation to maintain generation diversity and try to prevent premature local optima.

This evolution algorithm is highly configurable:
```
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
```
During evolution basic generation statistics are logged to terminal and a plot is generated showing progress:

![evolution stats](https://github.com/fredshone/g_prog/fig.png "evolution stats example")

After a solution is found or preset number of generations completed, the final algorithm is printed to terminal...
```
is greater
 is greater
  is less
   p4
   5
  -
   p2
   p5
 abs
  p5
```
Given the candidate strings A and B, this example translates to:
```
isless = 	
if (A[4]-B[4]) < 5:
		return 1
	else:
		return 0
temp = if i[0] > abs(A[5]-B[5]):
		return 1
	else:
		return 0
		
if temp > abs(A[5]-B[5]):
		return 1
	else:
		return 0
```
This particular example was only 86% accurate across 500 training examples.

#### Features

- type sensitive operations
- features for string matching application
- trial string data generator (rookie)
 
#### todo

- add generation stats to help with tuning
- add tweaking mutations for constants as score is high - ie adjust types of mutations
- implement scoring with NR TD network for training data - based on graph distance?
- implement within mathcing framework for TD stream
