from paper_check.tree_cutter import cut_tree
from paper_check.ProcessNewick import ProcessNewickFile
from make_coal_plots import points, iterations
import matplotlib.pyplot as plt
import subprocess


def MakeMasterCoals():
    master_results = [[] for _ in range(iterations)]
    i = 41
    while i < 20:
        coal_times_master = []

        filepath = "/Users/LAB-SCG-125/Documents/Master_sim/"
        subprocess.call(["/Applications/BEAST\ 2.6.6/bin/beast -threads 8 FinalModelDist.xml"], shell = True,
                       cwd=filepath)


        newick_tree_file_from_master = '/Users/LAB-SCG-125/Documents/Master_sim/FinalModelDist.newick'
        ProcessNewickFile(newick_tree_file_from_master)
        cutted_tree_from_master = cut_tree(newick_tree_file_from_master, probability_of_drop=0.0)

        for node in cutted_tree_from_master.all_nodes():
            #if node.data.type == 'Coalescence':
                # change to check of number of children >= 2
            if len(node.fpointer) > 1:
                coal_times_master.append(node.data.time)

        if len(coal_times_master) < 1000:
            #print("BADMASTER", i)
            pass
        else:
            print("MASTER", i)
            master_result, bins, patches = plt.hist(coal_times_master, bins=points)

            file = open(
                "/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/coals_distribution_1/" + str(
                    i) + " master", "w")
            for res in master_result:
                file.write(str(res) + ' ')
            file.close()

            i += 1

    return master_results

MakeMasterCoals()