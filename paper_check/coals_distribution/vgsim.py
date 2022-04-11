import matplotlib.pyplot as plt
import random
import sys
import VGsim
from make_coal_plots import points, iterations


def MakeVGsimCoals():
    vgsim_results = [[] for _ in range(iterations)]
    i = 0
    while i < 5:
        number_of_sites = 1
        populations_number = 2
        number_of_susceptible_groups = 3
        simulator = VGsim.Simulator(number_of_sites, populations_number, number_of_susceptible_groups,
                                    seed=random.randint(0, sys.maxsize))

        simulator.set_transmission_rate(0.25)
        simulator.set_transmission_rate(0.4, haplotype="G")

        mutation_rate = 0.003
        substitution_weights = [1, 1, 1, 1]  # ATCG
        simulator.set_mutation_rate(mutation_rate, substitution_weights)

        simulator.set_recovery_rate(0.0)
        simulator.set_sampling_rate(0.1)

        simulator.set_susceptibility_type(0)  # default
        simulator.set_susceptibility_type(1, haplotype="A")
        simulator.set_susceptibility_type(1, haplotype="C")
        simulator.set_susceptibility_type(1, haplotype="T")
        simulator.set_susceptibility_type(2, haplotype="G")

        simulator.set_susceptibility(1.0, susceptibility_type=0)  # no resist
        simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=0)  # resist
        simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=1)  # resist
        simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype=2)  # resist
        simulator.set_susceptibility(0.2, susceptibility_type=1, haplotype=3)  # partial resist
        simulator.set_susceptibility(0.0, susceptibility_type=2)  # resist

        simulator.set_immunity_transition(0.01, source=1, target=0)
        simulator.set_immunity_transition(0.01, source=2, target=0)

        simulator.set_population_size(100000, population=0)
        simulator.set_population_size(100000, population=1)
        simulator.set_migration_probability(0.01)

        simulator.simulate(iterations=2000000, time=200)
        simulator.genealogy()

        tree, times_vgsim = simulator.get_tree()

        coal_times_vgsim = []
        tree_parents = list(set(tree))
        for parent in tree_parents:
            coal_times_vgsim.append(times_vgsim[parent])

        if len(coal_times_vgsim) < 1000:
            pass
        else:
            vgsim_result, bins, patches = plt.hist(coal_times_vgsim, bins=points)

            file = open("/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/coals_distribution/" + str(i) +" vgsim", "w")
            for res in vgsim_result:
                file.write(str(res) + ' ')
            file.close()
            print("VGSIM", i)

            i += 1


    return vgsim_results

MakeVGsimCoals()

