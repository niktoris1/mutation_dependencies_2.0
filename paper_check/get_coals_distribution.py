from tree_class_from_newick import MakeTreeClassTree
from tree_cutter import cutted_tree_from_master
import matplotlib.pyplot as plt

def GetHist(newick_file_name = None, tree_class_tree = None, label = None):
    if newick_file_name != None:
        tree_class_tree = MakeTreeClassTree(newick_file_name)
    else:
        pass


    times_list = []
    for node in tree_class_tree.all_nodes():
        if len(node.fpointer) == 0:
            times_list.append(node.data.time)

    plt.hist(times_list, 100, rwidth = 0.9)
    plt.xlabel(label)
    plt.show()

GetHist(newick_file_name = "example_tree.nwk", label = "VGsim_tree")
GetHist(tree_class_tree = cutted_tree_from_master, label="Master_tree")