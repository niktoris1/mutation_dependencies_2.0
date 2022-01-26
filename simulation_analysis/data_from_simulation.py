from tree_class_from_newick import MakeTreeClassTree
import csv
import re

newick_file_name = "example_tree.nwk"


dict_name_muts = {}
dict_name_times = {}
dict_name_types = {}

tsv_file = open("example.tsv", "r")
read_tsv = csv.reader(tsv_file, delimiter="\t")

for line in read_tsv:
    if len(line) > 1:
        node_name = line[0]
        muts = re.split('\|', line[1])
        dict_name_muts.update({node_name:muts})

tree_class_tree = MakeTreeClassTree(newick_file_name,
                                    dict_name_muts = None, dict_name_times = None, dict_name_types = None, data_type = 1)
