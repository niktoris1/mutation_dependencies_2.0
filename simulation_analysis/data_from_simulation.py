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
    node_name = line[0]
    if len(line) > 1:
        muts = re.split('\|', line[1])
        dict_name_muts.update({node_name:muts})
    else:
        dict_name_muts.update({node_name:[]})


tree_class_tree = MakeTreeClassTree(newick_file_name,
                                    dict_name_muts = dict_name_muts, dict_name_times = None, dict_name_types = None, data_type = 1)

samples_for_usher = []

for node in tree_class_tree.all_nodes():
    if node.data.type == 'Sample':
        samples_for_usher.append(node)

samples_for_usher_to_csv = []
for sample in samples_for_usher:
    pass

f = open('/Users/LAB-SCG-125/Documents/Fitness_data/test/test.csv', 'w', newline='')

writer = csv.writer(f)
writer.writerow(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'])

f.close()

tree_class_tree.show()