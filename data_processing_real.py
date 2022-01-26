import re
import csv
from data_preparation_real import neutral_forward_mut, funct_forward_mut


# backward muts have the same number, but the origin and mutated nucleotyde swap places
neutral_backward_mut = neutral_forward_mut[-1] + neutral_forward_mut[1:-1]+neutral_forward_mut[0]
funct_backward_mut = funct_forward_mut[-1] + funct_forward_mut[1:-1]+funct_forward_mut[0]
muts_list = [neutral_forward_mut, neutral_backward_mut, funct_forward_mut, funct_backward_mut]

dict_name_muts = {}
dict_name_types = {}
dict_name_times = {}

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/sample_paths.txt", "r")

for line in file:
    word_list = re.split(': |,|\n', line)
    node_name = word_list[0]
    node_name = re.split('\|', node_name)[0]
    node_muts = word_list[1:-1]

    chosen_muts = []

    for mut in node_muts:
        if mut in muts_list:
            chosen_muts.append(mut)

    dict_name_muts.update({node_name: chosen_muts})

    if node_name[0:3] == 'EPI':
        dict_name_types.update({node_name: 'Sample'})
    else:
        dict_name_types.update({node_name: 'Coalescence'})

file.close()

file = open("/Users/LAB-SCG-125/Documents/Fitness_data/chron_dates_out.tsv", "r")

read_tsv = csv.reader(file, delimiter="\t")

for line in read_tsv:
    dict_name_times.update({line[0]: line [1]}) # adds a new node-time pair
dict_name_times.pop('strain')

file.close()


