from tree_class_from_newick import MakeTreeClassTree
from paper_check.coals_distribution.make_coal_plots import maxtime
import random


def cut_tree(newick_tree_file, probability_of_drop):
    tree = MakeTreeClassTree(newick_tree_file, extrenal_dicts_exist=0)

    for node in tree.all_nodes():
    #    if len(node.fpointer) == 0 and node.data.type != 'Sample':
    #        raise ValueError
    #    if len(node.fpointer) != 0 and node.data.type == 'Sample':
    #        raise ValueError
        if len(node.fpointer) == 0:
            node.data.type = 'Sample'
        else:
            node.data.type = 'Coalescence'



    overall = 0
    for node in tree.all_nodes():
        if node.data.type == 'Sample':
            if random.random() < probability_of_drop:
                tree.remove_node(node.identifier)
                overall = overall + 1
    print(overall, "leafs dropped")

    #removing end node for correct coals distribution
    counter = 0
    for node in tree.all_nodes():
        if node.data.time == maxtime:
            counter += 1
            tree.remove_node(node.identifier)
    print(counter, "leafs dropped with time", maxtime)

    # we check all nodes on having just one child and terminate while loop if there is no such vertices

    finished = 0
    while finished == 0:
        finished = 1
        counter
        for node in tree.all_nodes():
            #if len(node.fpointer) == 1 and (node.is_root() == False):
            #    tree.link_past_node(node.identifier)
            if len(node.fpointer) == 0 and node.data.type == 'Coalescence':
                tree.remove_node(node.identifier)
                finished = 0

    print("Newick tree cut")

    return tree
