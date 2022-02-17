import re

from tree_class_from_newick import MakeTreeClassTree
import random


def cut_tree(newick_tree_file, probability_of_drop):
    tree = MakeTreeClassTree(newick_tree_file, extrenal_dicts_exist=0)

    for node in tree.all_nodes():
        if node.is_leaf() == True:
            if random.random() < probability_of_drop:
                tree.link_past_node(node.identifier)

    # we check all nodes on having just one child and terminate while loop if there is no such vertices
    finished = 0
    while finished == 0:
        finished = 1
        for node in tree.all_nodes():
            if len(node.fpointer) == 1:
                tree.link_past_node(node.identifier)
                finished = 0

    return tree

def ProcessNewickFile(newick_tree_file): #removes all the E-4 and similar things
    with open(newick_tree_file, "r") as file:
        text_newick = file.read()
        elements = re.split(",|:|\(|\)", text_newick)
        for element in elements:
            if 'E' in element:
                degree = int(element[-1])
                newelement = element[:-3]
                newelement = '0' + '.' + (degree-1)*'0' + newelement[0] + newelement[2:]
                text_newick = text_newick.replace(element, newelement)

    with open(newick_tree_file, "w") as file:
        file.write(text_newick)



newick_tree_file_from_master = '/Users/LAB-SCG-125/Documents/Master_sim/FinalModel.newick'
ProcessNewickFile(newick_tree_file_from_master)

cutted_tree_from_master = cut_tree(newick_tree_file_from_master, 0.001)

