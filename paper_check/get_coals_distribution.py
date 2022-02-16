from tree_class_from_newick import MakeTreeClassTree
import matplotlib.pyplot as plt

def GetHist(newick_file_name):
    tree_class_tree = MakeTreeClassTree(newick_file_name)

    times_list = []
    for node in tree_class_tree.all_nodes():
        if len(node.fpointer) == 0:
            times_list.append(node.data.time)

    plt.hist(times_list, 20, rwidth = 0.9)
    plt.show()

GetHist("example_tree.nwk")