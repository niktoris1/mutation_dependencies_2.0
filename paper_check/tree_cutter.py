from tree_class_from_newick import MakeTreeClassTree
import random

newick_tree_file = '/Users/LAB-SCG-125/Documents/Fitness_data/samples_with_at_least_one_mutation.nwk'

tree_class_tree = MakeTreeClassTree(newick_tree_file, extrenal_dicts_exist=0)

def cut_tree(tree, probability_of_drop):
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

cutted_tree = cut_tree(tree_class_tree, 0.5)
pass
