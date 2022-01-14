import subprocess

mut1, mut2 = "C501T", "C501T"

# These lines generate nesssesary data
# First line creates a pb file of needed subtree with two mutations
# Second line creates a newick file of said subtree
# Third line provides us with the list of nodes in the subtree together with mutations on them

subprocess.run(["matUtils", "extract", "-i", "GISAID-2021-11-05.masked.dated.pb", "-m", mut1+","+mut2, "-o", "samples_with_at_least_one_mutation.pb"], cwd="/Users/LAB-SCG-125/Documents/Fitness_data")
subprocess.run(["matUtils", "extract", "-i", "samples_with_at_least_one_mutation.pb", "-t", "samples_with_at_least_one_mutation.nwk"], cwd="/Users/LAB-SCG-125/Documents/Fitness_data")
subprocess.run(["matUtils", "extract", "-i", "samples_with_at_least_one_mutation.pb", "-A", "sample_paths.txt"], cwd="/Users/LAB-SCG-125/Documents/Fitness_data")

