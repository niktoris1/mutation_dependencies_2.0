import re
import csv
from tree_class_from_newick import MakeTreeClassTree
import ciso8601

import time

from tree_class_tree_to_binary import tree_to_binary
from data_preparation import neutral_forward_mut, funct_forward_mut
from data_processing import neutral_backward_mut, funct_backward_mut
from data_processing import dict_name_muts, dict_name_times, dict_name_types

import datetime

tree_class_tree = MakeTreeClassTree("/Users/LAB-SCG-125/Documents/Fitness_data/samples_with_at_least_one_mutation.nwk",
                                    dict_name_muts=dict_name_muts, dict_name_times=dict_name_times, dict_name_types=dict_name_types)
tree_class_tree.show()
print('Tree class tree is built')

class NodeData:
    def __init__(self, mutations, time, type):
        self.mutations = mutations
        self.time = time
        self.type = type

 # This slows everything down, it is quadratical
for node_in_tree in tree_class_tree.all_nodes():
    if node_in_tree.tag in dict_name_muts.keys():
        node_in_tree.data = NodeData(dict_name_muts[node_in_tree.tag], dict_name_times[node_in_tree.tag], dict_name_types[node_in_tree.tag])
print("Data added on node")

tree_class_tree = tree_to_binary(tree_class_tree)
print("Tree transformed to binary")

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

print("Binary tree transformed into tree table")

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
                time = dict_name_times[node_name]
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
    print("Tree transformed into Shishkin class table")
    return shishkin_tree_table

shishkin_neutral_table = TreeClassTreeTableToShishkinTreeTable(neutral_trees_table)
shishkin_funct_table = TreeClassTreeTableToShishkinTreeTable(funct_trees_table)