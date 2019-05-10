import trees

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


