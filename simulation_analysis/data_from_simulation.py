from tree_class_from_newick import MakeTreeClassTree

newick_file_name = "example_tree.nwk"

dict_name_muts = None
dict_name_times = None
dict_name_types = None

tree_class_tree = MakeTreeClassTree(newick_file_name,
                                    dict_name_muts = None, dict_name_times = None, dict_name_types = None, data_type = 1)
