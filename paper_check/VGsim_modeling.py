import random
import sys
import pandas as pd

import VGsim
import matplotlib.pyplot as plt

for i in range(10):


    number_of_sites = 1
    populations_number = 2
    number_of_susceptible_groups = 3
    simulator = VGsim.Simulator(number_of_sites, populations_number, number_of_susceptible_groups, seed=random.randint(0, sys.maxsize))
    # Seed 4152420620979014631 produces error

    simulator.set_transmission_rate(0.24)
    simulator.set_transmission_rate(0.4, haplotype="G")

    mutation_rate=0.0001
    substitution_weights=[1,1,1,1] #ATCG
    simulator.set_mutation_rate(mutation_rate, substitution_weights)\

    simulator.set_recovery_rate(0.0)
    simulator.set_sampling_rate(0.1)

    simulator.set_susceptibility_type(0) #default
    simulator.set_susceptibility_type(1, haplotype="A")
    simulator.set_susceptibility_type(1, haplotype="C")
    simulator.set_susceptibility_type(1, haplotype="T")
    simulator.set_susceptibility_type(2, haplotype="G")

    simulator.set_susceptibility(1.0, susceptibility_type=0) # no resist
    simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype="A") # no resist
    simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype="C") # no resist
    simulator.set_susceptibility(0.0, susceptibility_type=1, haplotype="T") # no resist
    simulator.set_susceptibility(0.2*0.4, susceptibility_type=1, haplotype="G") # partial resist
    simulator.set_susceptibility(0.0, susceptibility_type=2) # resist

    simulator.set_immunity_transition(0.01, source=1, target=0)
    simulator.set_immunity_transition(0.01, source=1, target=0)
    simulator.set_immunity_transition(0.01, source=2, target=0)

    simulator.set_population_size(100000, population=0)
    simulator.set_population_size(100000, population=1)
    simulator.set_migration_probability(0.001)

    simulator.simulate(1000000, time=500)

    step_num = 500
    timestamps = simulator.get_data_susceptible(population=0, susceptibility_type=0, step_num=step_num)[1]

    S0 = simulator.get_data_susceptible(population=0, susceptibility_type=0, step_num=step_num)[0]
    I00 = simulator.get_data_infectious(population=0, haplotype="A", step_num=step_num)[0]
    I10 = simulator.get_data_infectious(population=0, haplotype="C", step_num=step_num)[0]
    I20 = simulator.get_data_infectious(population=0, haplotype="T", step_num=step_num)[0]
    I30 = simulator.get_data_infectious(population=0, haplotype="G", step_num=step_num)[0]
    R00 = simulator.get_data_susceptible(population=0, susceptibility_type=1, step_num=step_num)[0]
    R10 = simulator.get_data_susceptible(population=0, susceptibility_type=2, step_num=step_num)[0]

    S1 = simulator.get_data_susceptible(population=1, susceptibility_type=0, step_num=step_num)[0]
    I01 = simulator.get_data_infectious(population=1, haplotype="A", step_num=step_num)[0]
    I11 = simulator.get_data_infectious(population=1, haplotype="C", step_num=step_num)[0]
    I21 = simulator.get_data_infectious(population=1, haplotype="T", step_num=step_num)[0]
    I31 = simulator.get_data_infectious(population=1, haplotype="G", step_num=step_num)[0]
    R01 = simulator.get_data_susceptible(population=1, susceptibility_type=1, step_num=step_num)[0]
    R11 = simulator.get_data_susceptible(population=1, susceptibility_type=2, step_num=step_num)[0]

    plt.plot(timestamps, S0, color = 'b', linewidth = 0.1)

master_timestamps = pd.read_csv('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/timestamps.csv').values.tolist()
master_S0 = pd.read_csv('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S0.csv')
plt.plot(master_timestamps, master_S0, color = 'b', linewidth = 1)

plt.show()
#simulator.debug()

#simulator.add_plot_infectious(population=0, haplotype=0, step_num=500)
#simulator.add_plot_infectious(population=0, haplotype=1, step_num=500)
#simulator.add_plot_infectious(population=1, haplotype="A", step_num=500)

simulator.add_plot_susceptible(population=0, susceptibility_type=0, step_num=500)
#simulator.add_plot_susceptible(population=0, susceptibility_type=1, step_num=500)
#simulator.add_plot_susceptible(population=0, susceptibility_type=2, step_num=500)
#simulator.add_plot_susceptible(population=1, susceptibility_type=0, step_num=500)
#simulator.add_plot_susceptible(population=1, susceptibility_type=1, step_num=500)
#simulator.add_plot_susceptible(population=1, susceptibility_type=2, step_num=500)
#simulator.add_title(name="Plot")
#simulator.add_legend()
#simulator.plot()

#simulator.genealogy()

#file_path = "/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check"
#file_name = "example"

#simulator.output_newick(file_name, file_path)
#simulator.output_mutations(file_name, file_path)
#simulator.output_migrations(file_name, file_path)

#simulator.print_basic_parameters()
#simulator.print_immunity_model()
#simulator.print_populations()

