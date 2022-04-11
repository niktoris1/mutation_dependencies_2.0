import time

def ProcessNewickFile(newick_tree_file): #removes all the E-4 and similar things
    with open(newick_tree_file, "r") as file:
        t1 = time.time()
        text_newick = file.read()
        print("Length of newick file", len(text_newick))
        if 'E' in text_newick:
            i = 0
            while i < len(text_newick):
                if text_newick[i] == 'E':
                    e_position = i
                    degree = int(text_newick[e_position+2])
                    while text_newick[i] != '.':
                        i = i - 1
                    dot_position = i
                    string_beg = text_newick[:dot_position-1]
                    string_end =  text_newick[e_position + 3:]
                    string_mid = '0.' + (degree-1)*'0' + text_newick[dot_position+1:e_position]
                    text_newick = string_beg + string_mid + string_end
                    i = e_position + degree - 1 + 5 # we can safely add 5, without fear of missing an E
                else:
                    i = i + 1

        with open(newick_tree_file, "w") as file:
            file.write(text_newick)

        t2 = time.time()
        print("File processed in", t2-t1, "seconds")



#newick_tree_file_from_master = '/Users/LAB-SCG-125/Documents/Master_sim/FinalModelDist.newick'
#print("Retrieved newick")
#ProcessNewickFile(newick_tree_file_from_master)
#print("Newick file processed")