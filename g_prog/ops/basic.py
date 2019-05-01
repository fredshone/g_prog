from trees import Function_wrapper


def safe_div(a, b):
	if b == 0:
		return 0
	if b > 10000:
		return 0
	else:
		try:
			return int(a / b)
		except:
			return 0


def safe_pow(a, b):
	if a == 0 or b == 0:
		return 0
	if a > 100 or b > 100:
		return 10000
	else:
		try:
			return a ** b
		except:
			return 10000


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

def is_between(i):

	if i[1] < i[0] < i[2]:
		return i[3]
	else:
		return i[4]

def is_string(i):

	if isinstance(i, str):
		return True
	else:
		return False

adder = Function_wrapper(lambda i: i[0] + i[1], ['int', 'int'], 'int', '+')
subber = Function_wrapper(lambda i: i[0] - i[1], ['int', 'int'], 'int', '-')
multiplier = Function_wrapper(lambda i: i[0] * i[1], ['int', 'int'], 'int', '*')
powerer = Function_wrapper(lambda i: safe_pow(i[0], i[1]), ['int', 'int'], 'int', '**')
divider = Function_wrapper(lambda i: safe_div(i[0], i[1]), ['int', 'int'], 'int', '/')
absoluter = Function_wrapper(lambda i: abs(i[0]), ['int'], 'int', 'abs')
iffer = Function_wrapper(if_function, ['int', 'int', 'int'], 'int', 'if')
greater = Function_wrapper(is_greater, ['int', 'int'], 'int', 'is greater')
between = Function_wrapper(is_between, ['int', 'int', 'int', 'int', 'int'], 'int', 'is between')
negative = Function_wrapper(lambda i: - i[0], ['int'], 'int', 'negative')

tester = Function_wrapper(is_string, ['str'], 'bool', 'str')


basic_functions = {
'int':
	[
	adder,
	subber,
	multiplier,
	# iffer,
	# greater,
	# between,
	# powerer,
	# divider,
	# absoluter,
	# negative
	],
'bool':
	[
	tester
	]
}


def example_tree():

	return Node(iffer, [
		Node(greater, [Param_node(0), Const_node(3)]),
		Node(adder, [Param_node(1), Const_node(5)]),
		Node(subber, [Param_node(1), Const_node(2)]),
		])

