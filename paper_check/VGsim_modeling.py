import random
import sys
from csv_to_list import csv_to_list
import VGsim
import matplotlib.pyplot as plt

fig, axs = plt.subplots(nrows=2, ncols=2, sharex = True, sharey = True)
fig.suptitle('Theoretical and practical trajectories')


for i in range(20):
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
    simulator.set_migration_probability(0.1)

    simulator.simulate(1000000, time=700)

    step_num = 500
    timestamps = simulator.get_data_susceptible(population=0, susceptibility_type=0, step_num=step_num)[1]

    S0 = simulator.get_data_susceptible(population=0, susceptibility_type=0, step_num=step_num)[0]
    I00 = simulator.get_data_infectious(population=0, haplotype=0, step_num=step_num)[0]
    I10 = simulator.get_data_infectious(population=0, haplotype=1, step_num=step_num)[0]
    I20 = simulator.get_data_infectious(population=0, haplotype=2, step_num=step_num)[0]
    I30 = simulator.get_data_infectious(population=0, haplotype=3, step_num=step_num)[0]
    R00 = simulator.get_data_susceptible(population=0, susceptibility_type=1, step_num=step_num)[0]
    R10 = simulator.get_data_susceptible(population=0, susceptibility_type=2, step_num=step_num)[0]

    S1 = simulator.get_data_susceptible(population=1, susceptibility_type=0, step_num=step_num)[0]
    I01 = simulator.get_data_infectious(population=1, haplotype=0, step_num=step_num)[0]
    I11 = simulator.get_data_infectious(population=1, haplotype=1, step_num=step_num)[0]
    I21 = simulator.get_data_infectious(population=1, haplotype=2, step_num=step_num)[0]
    I31 = simulator.get_data_infectious(population=1, haplotype=3, step_num=step_num)[0]
    R01 = simulator.get_data_susceptible(population=1, susceptibility_type=1, step_num=step_num)[0]
    R11 = simulator.get_data_susceptible(population=1, susceptibility_type=2, step_num=step_num)[0]

    axs[0, 0].plot(timestamps, S0, color = 'b', linewidth = 0.1)
    axs[0, 0].plot(timestamps, R00, color='g', linewidth=0.1)
    axs[0, 0].plot(timestamps, R10, color='r', linewidth=0.1)

    axs[1, 0].plot(timestamps, I00, color='b', linewidth=0.1)
    axs[1, 0].plot(timestamps, I10, color='g', linewidth=0.1)
    axs[1, 0].plot(timestamps, I20, color='r', linewidth=0.1)
    axs[1, 0].plot(timestamps, I30, color='k', linewidth=0.1)

    axs[0, 1].plot(timestamps, S1, color = 'b', linewidth=0.1)
    axs[0, 1].plot(timestamps, R01, color='g', linewidth=0.1)
    axs[0, 1].plot(timestamps, R11, color='r', linewidth=0.1)

    axs[1, 1].plot(timestamps, I01, color='b', linewidth=0.1)
    axs[1, 1].plot(timestamps, I11, color='g', linewidth=0.1)
    axs[1, 1].plot(timestamps, I21, color='r', linewidth=0.1)
    axs[1, 1].plot(timestamps, I31, color='k', linewidth=0.1)


master_timestamps = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/timestamps.csv')

master_S0 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S0.csv')
master_R00 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R00.csv')
master_R10 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R10.csv')
master_I00 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I00.csv')
master_I10 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I10.csv')
master_I20 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I20.csv')
master_I30 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I30.csv')

master_S1 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S1.csv')
master_R01 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R01.csv')
master_R11 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R11.csv')
master_I01 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I01.csv')
master_I11 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I11.csv')
master_I21 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I21.csv')
master_I31 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I31.csv')

axs[0, 0].plot(master_timestamps, master_S0, color = 'b', linewidth = 1, label = "master_S0")
axs[0, 0].plot(master_timestamps, master_R00, color = 'g', linewidth = 1, label = "master_R00")
axs[0, 0].plot(master_timestamps, master_R10, color = 'r', linewidth = 1, label = "master_R10")
axs[0, 0].legend(loc = 'upper right', fontsize = 'x-small')

axs[1, 0].plot(master_timestamps, master_I00, color = 'b', linewidth = 1, label = "master_I00")
axs[1, 0].plot(master_timestamps, master_I10, color = 'g', linewidth = 1, label = "master_I10")
axs[1, 0].plot(master_timestamps, master_I20, color = 'r', linewidth = 1, label = "master_I20")
axs[1, 0].plot(master_timestamps, master_I30, color = 'k', linewidth = 1, label = "master_I30")
axs[1, 0].legend(loc = 'upper right', fontsize = 'x-small')

axs[0, 1].plot(master_timestamps, master_S1, color = 'b', linewidth = 1, label = "master_S1")
axs[0, 1].plot(master_timestamps, master_R01, color = 'g', linewidth = 1, label = "master_R01")
axs[0, 1].plot(master_timestamps, master_R11, color = 'r', linewidth = 1, label = "master_R11")
axs[0, 1].legend(loc = 'upper right', fontsize = 'x-small')

axs[1, 1].plot(master_timestamps, master_I01, color = 'b', linewidth = 1, label = "master_I01")
axs[1, 1].plot(master_timestamps, master_I11, color = 'g', linewidth = 1, label = "master_I11")
axs[1, 1].plot(master_timestamps, master_I21, color = 'r', linewidth = 1, label = "master_I21")
axs[1, 1].plot(master_timestamps, master_I31, color = 'k', linewidth = 1, label = "master_I31")
axs[1, 1].legend(loc = 'upper right', fontsize = 'x-small')

plt.savefig('plots.png', dpi = 4000)
plt.show()

#simulator.debug()

#simulator.add_plot_infectious(population=0, haplotype=0, step_num=500)
#simulator.add_plot_infectious(population=0, haplotype=1, step_num=500)
#simulator.add_plot_infectious(population=1, haplotype="A", step_num=500)

#simulator.add_plot_susceptible(population=0, susceptibility_type=0, step_num=500)
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

