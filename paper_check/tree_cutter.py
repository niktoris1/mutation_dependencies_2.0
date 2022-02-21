import re
from  ProcessNewick import newick_tree_file_from_master

from tree_class_from_newick import MakeTreeClassTree
import random


def cut_tree(newick_tree_file, probability_of_drop):
    tree = MakeTreeClassTree(newick_tree_file, extrenal_dicts_exist=0)

    for node in tree.all_nodes():
        if node.is_leaf() == True:
            if random.random() < probability_of_drop:
                tree.remove_node(node.identifier)
    print("Leafs dropped")

    # we check all nodes on having just one child and terminate while loop if there is no such vertices
    finished = 0
    while finished == 0:
        finished = 1
        for node in tree.all_nodes():
            if len(node.fpointer) == 1:
                tree.link_past_node(node.identifier)
                finished = 0

    print("Newick tree cut")

    return tree

cutted_tree_from_master = cut_tree(newick_tree_file_from_master, probability_of_drop=0.0)

