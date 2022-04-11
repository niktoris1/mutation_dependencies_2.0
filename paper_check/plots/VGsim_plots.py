import random
import sys
from paper_check.csv_to_list import csv_to_list
import VGsim
import matplotlib.pyplot as plt

from make_plots import fig1, fig2, ax1, ax2, number_of_plots, lighten_color

def make_vgsim_plots():
    i = 0
    while i < number_of_plots:
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

        simulator.simulate(iterations=2000000, time=200)

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

        if max(I00) < 100:
            pass
        else:
            ax1[0, 0].plot(timestamps, S0, color = 'b', alpha = 0.5, linewidth = 0.2)
            ax1[0, 0].plot(timestamps, R00, color='g', alpha = 0.5, linewidth=0.2)
            ax1[0, 0].plot(timestamps, R10, color='r', alpha = 0.5, linewidth=0.2)

            ax2[0, 0].plot(timestamps, I00, color='b', alpha = 0.5, linewidth=0.2)
            ax2[0, 0].plot(timestamps, I10, color='g', alpha = 0.5, linewidth=0.2)
            ax2[0, 0].plot(timestamps, I20, color='r', alpha = 0.5, linewidth=0.2)
            ax2[0, 0].plot(timestamps, I30, color='m', alpha = 0.5, linewidth=0.2)

            ax1[1, 0].plot(timestamps, S1, color = 'b', alpha = 0.5, linewidth=0.2)
            ax1[1, 0].plot(timestamps, R01, color='g', alpha = 0.5, linewidth=0.2)
            ax1[1, 0].plot(timestamps, R11, color='r', alpha = 0.5, linewidth=0.2)

            ax2[1, 0].plot(timestamps, I01, color='b', alpha = 0.5, linewidth=0.2)
            ax2[1, 0].plot(timestamps, I11, color='g', alpha = 0.5, linewidth=0.2)
            ax2[1, 0].plot(timestamps, I21, color='r', alpha = 0.5, linewidth=0.2)
            ax2[1, 0].plot(timestamps, I31, color='m', alpha = 0.5, linewidth=0.2)
            i += 1

