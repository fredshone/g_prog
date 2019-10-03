from random import random, choices
import networkx as nx
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from collections import defaultdict
import random

ground_truth_dir = Path('/Users/fred.shone/Projects/captain/test_data')
test_trains_dir = Path('/Users/fred.shone/Projects/captain/test_data/trains_2/')

print("build ground truth graph")
test_paths = {n.stem: n for n in ground_truth_dir.iterdir() if n.suffix == '.csv'}

def pad(area, raw, length=4):
    """
    Pads raw berth id with 0s so that it is 4 digits long and adds the area code as a prefix. Plus use upper case.
    """
    return (area + "_" + str(raw).rjust(length, '0')).upper()


def yield_areas(area, path):
    """
    Yield all the padded O-D pairs from a given .csv path.
    """
    df = pd.read_csv(path)
    for _, (row) in df.iterrows():
        o_area, o, d_area, d = row[:4]
        yield (pad(o_area, o), pad(d_area, d))


# build a Directional Graph (aka DiGraoph) using networkx...
G = nx.DiGraph()
for area, path in test_paths.items():
    for o, d in yield_areas(area, path):
        G.add_edge(o, d)


print("building test data")
desc_paths = {}
# make a dict of paths to the step csvs:
for path in test_trains_dir.iterdir():
    if not path.suffix == '.csv':
        continue
    desc = path.stem.split('_')[0]
    if desc not in desc_paths:
        desc_paths[desc] = {}
    if path.stem[-8:] == 'step_log':
        desc_paths[desc]['step_log'] = path
    if path.stem[-9:] == 'berth_log':
        desc_paths[desc]['berth_log'] = path


def yield_step_ods(path):
    """
    Yield all the padded O-D pairs from a given .csv path.
    """
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        _, _, _, _, o, d, time = row[:7]
        yield (o, d, time)


matches = []
missmatches = []
for desc, paths in desc_paths.items():
    for (o, d, time) in yield_step_ods(paths['step_log']):
        # check o and d are in G
        if o not in G.nodes:
            continue
        if d not in G.nodes:
            continue
        try:
            path= nx.shortest_path(G, source=o, target=d, weight=None, method='dijkstra')

            if len(path) == 2:
                matches.append((o,d))
            else:
                missmatches.append((o,d))

        except nx.NetworkXNoPath:
            missmatches.append((o,d))


def get_missmatch():
    return choices(missmatches)[0]


def get_match():
    return choices(matches)[0]


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


def get_training_candidate():

    if random.random() < .5:
        return build_features(get_missmatch()), False
    else:
        return build_features(get_match()), True


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
