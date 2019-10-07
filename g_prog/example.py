import argparse


parser = argparse.ArgumentParser(description='Process some berth_ids.')
parser.add_argument('a', type=str,
                    help='a string berth id')
parser.add_argument('b', type=str,
                    help='a string berth id')

args = parser.parse_args()


def extract_numeric(code):
    num = ''
    for i in code:
        if i.isnumeric():
            num += i
    try:
        num = int(num)
    except ValueError:
        num = 0
    return num


def build_features(sample):
    features = []

    if sample[0][:2] == sample[1][:2]:
        features.append(1)
    else:
        features.append(0)

    features.append(extract_numeric(sample[0][3:]) - extract_numeric(sample[0][3:]))

    features.extend([ord(a) - ord(b) for a, b in zip(sample[0][3:], sample[1][3:])])

    return features


def is_match(A, B):

    params = build_features([A, B])

    return bool(abs((params[0] > params[2]) - (params[4] > params[2])))


print(is_match(args.a, args.b))
