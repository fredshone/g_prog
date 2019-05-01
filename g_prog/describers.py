from random import random, choices

char_corpus = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*'
num_corpus = '1234567890'


def get_char(k=1):
	return ''.join(choices(char_corpus, k=k))


def get_num(k=1):
	return ''.join(choices(num_corpus, k=k))


def get_describer():
	return get_char(k=2) + '_' + get_num(k=4)


def tweak_describer(sample):
	return get_char(k=2) + '_' + get_char() + sample[4:]


def build_features(sample1, sample2):
	return [ord(a) - ord(b) for a, b in zip(sample1, sample2)]


def get_training_candidate():
	
	sample1 = get_describer()
	if random() < .5:
		return build_features(sample1, tweak_describer(sample1)), True

	else:
		sample2 = get_describer()
		return build_features(sample1, sample2), False


def build_hidden_set(size=100):
	rows = []
	for i in range(size):
		rows.append(get_training_candidate())
	return rows


def score_function(tree, hidden_set):

	correct = 0
	for data in hidden_set:
		v = tree.evaluate(data[0])
		if bool(abs(v)) == data[1]:
			correct += 1
	return correct / len(hidden_set)