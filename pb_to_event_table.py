import re
import csv
from tree_class_from_newick import MakeTreeClassTree
import ciso8601

import time

from tree_class_tree_to_binary import tree_to_binary

import datetime

samples_with_one_mutation = []

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/samples_with_at_least_one_mutation.txt", "r")

for line in file:
    samples_with_one_mutation.append(line.split()[0])

samples_with_one_mutation.remove("sample")

file.close()

for sample_name_num in range(len(samples_with_one_mutation)):
    samples_with_one_mutation[sample_name_num] = re.split('\|', samples_with_one_mutation[sample_name_num])[0]

class Node:
    def __init__(self, node_id, mutations, time, type):
        self.node_id = node_id
        self.mutations = mutations
        self.time = time
        self.type = type

nodes_with_data = []
neutral_forward_mut, funct_forward_mut = 'C501T', 'C452A'

# backward muts have the same number, but the origin and mutated nucleotyde swap places
neutral_backward_mut = neutral_forward_mut[-1] + neutral_forward_mut[1:-1]+neutral_forward_mut[0]
funct_backward_mut = funct_forward_mut[-1] + funct_forward_mut[1:-1]+funct_forward_mut[0]
muts_list = [neutral_forward_mut, neutral_backward_mut, funct_forward_mut, funct_backward_mut]

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/sample_paths.txt", "r")

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

tree_class_tree = MakeTreeClassTree("/Users/LAB-SCG-125/Documents/Fitness_data/samples_with_at_least_one_mutation.nwk")

for node_with_data in nodes_with_data:
    for node_in_tree in tree_class_tree.all_nodes():
        if node_with_data.node_id == node_in_tree.tag:
            node_in_tree.data = node_with_data

tree_class_tree = tree_to_binary(tree_class_tree)

def DFS(tree_class_tree, start_node, forward_mutation, backward_mutation, table):
    if start_node.data == None or not (backward_mutation in start_node.data.mutations):
        table.append(start_node)
        for node_id in start_node.fpointer:
            if tree_class_tree[node_id].data != None:
                if forward_mutation in tree_class_tree[node_id].data.mutations and tree_class_tree[node_id].tag[0:5] != 'Dummy':
                    raise ValueError('A decendant has the same forward mutation without backward mutation in between')
            DFS(tree_class_tree, tree_class_tree[node_id], forward_mutation, backward_mutation, table)


neutral_trees_table = []
for node in tree_class_tree.all_nodes():
    if node.data != None:
        if neutral_forward_mut in node.data.mutations:
            new_neutral_subtable = []
            DFS(tree_class_tree, node, neutral_forward_mut, neutral_backward_mut, new_neutral_subtable)
            neutral_trees_table.append(new_neutral_subtable)

funct_trees_table = []
for node in tree_class_tree.all_nodes():
    if node.data != None:
        if funct_forward_mut in node.data.mutations:
            new_funct_subtable = []
            DFS(tree_class_tree, node, funct_forward_mut, funct_backward_mut, new_funct_subtable)
            funct_trees_table.append(new_funct_subtable)

# here we put dates on other nodes

def RussTimeToNumber(russ_time):
    time_string = re.split('\ ', russ_time)[0]
    current_time = ciso8601.parse_datetime(time_string)
    time_in_secs = time.mktime(current_time.timetuple())
    return time_in_secs


def TreeClassTreeTableToShishkinTreeTable(tree_table):
    shishkin_tree_table = []
    for tree_subtable in tree_table:
        shishkin_tree_subtable = []
        for node in tree_subtable:
            node_name = re.split('\|', node.tag)[0]
            if node.data != None:
                time = node.data.time
            else:
                time = dict_nodes_times[node_name]
            time = RussTimeToNumber(time)
            if node.data == None:
                is_sample = 1
                is_coal = 0
            else:
                if node.data.type == 'Coalescence':
                    is_sample = 0
                    is_coal = 1
                else:
                    is_sample = 1
                    is_coal = 0

            shishkin_tree_subtable.append([time, is_sample, is_coal, 'Unknown_lineages', 'Unknown if root'])
        shishkin_tree_table.append(shishkin_tree_subtable)

    return shishkin_tree_table

shishkin_neutral_table = TreeClassTreeTableToShishkinTreeTable(neutral_trees_table)
shishkin_funct_table = TreeClassTreeTableToShishkinTreeTable(funct_trees_table)