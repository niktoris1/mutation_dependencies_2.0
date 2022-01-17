import re
import csv
from data_preparation import neutral_forward_mut, funct_forward_mut


class Node:
    def __init__(self, node_id, mutations, time, type):
        self.node_id = node_id
        self.mutations = mutations
        self.time = time
        self.type = type


# backward muts have the same number, but the origin and mutated nucleotyde swap places
neutral_backward_mut = neutral_forward_mut[-1] + neutral_forward_mut[1:-1]+neutral_forward_mut[0]
funct_backward_mut = funct_forward_mut[-1] + funct_forward_mut[1:-1]+funct_forward_mut[0]
muts_list = [neutral_forward_mut, neutral_backward_mut, funct_forward_mut, funct_backward_mut]

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/sample_paths.txt", "r")

nodes_with_data = []

for line in file:
    word_list = re.split(': |,|\n', line)
    node_id = word_list[0]
    node_id = re.split('\|', node_id)[0]
    node_muts = word_list[1:-1]

    chosen_muts = []

    for mut in node_muts:
        if mut in muts_list:
            chosen_muts.append(mut)

    if node_id[0:3] == 'EPI':
        nodes_with_data.append(Node(node_id, chosen_muts, 'Unknown', 'Sample'))
    else:
        nodes_with_data.append(Node(node_id, chosen_muts, 'Unknown', 'Coalescence'))

file.close()

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/chron_dates_out.tsv", "r")

read_tsv = csv.reader(file, delimiter="\t")

dict_nodes_times = {}

for line in read_tsv: # TODO - it works for long
    dict_nodes_times.update({line[0]: line [1]}) # adds a new node-time pair

for node in nodes_with_data:
    node.time = dict_nodes_times[node.node_id]


