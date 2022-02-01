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
sample_list = []
mut_list = []

muts_to_samples = {}
muts_to_01_arrs = {}

for sample in samples_for_usher:
    sample_list.append(sample.tag)
    for mut in sample.data.mutations:
        if not (mut in mut_list):
            mut_list.append(mut)
        if mut in muts_to_samples:
            muts_to_samples[mut].append(sample.tag)
        else:
            muts_to_samples.update({mut:[sample.tag]})

for mut in mut_list:
    muts_to_01_arrs.update({mut:[0 for _ in range(len(sample_list))]})

for sample_num in range(len(sample_list)):
    sample = sample_list[sample_num]
    for mut in muts_to_samples:
        if sample in muts_to_samples[mut]:
            muts_to_01_arrs[mut][sample_num] = 1


f = open('/Users/LAB-SCG-125/Documents/Fitness_data/test/test_new_samples.csv', 'w', newline='')

writer = csv.writer(f)
writer.writerow(['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + sample_list)
for mut_name in muts_to_01_arrs:
    mut_pos = mut_name[1:-1]
    writer.writerow(['some_chrom', mut_pos, mut_name, mut_name[0], mut_name[-1], '.', 'PASS', 'some_info', 'GT:CLADE'] + muts_to_01_arrs[mut])


f.close()

tree_class_tree.show()