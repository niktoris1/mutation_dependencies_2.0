import subprocess
import matplotlib.pyplot as plt
from paper_check.csv_to_list import csv_to_list

from make_plots import fig1, fig2, ax1, ax2, number_of_plots, lighten_color


def make_master_plots():
    for i in range(number_of_plots):
        filepath = "/Users/LAB-SCG-125/Documents/Master_sim"
        subprocess.call(["/Applications/BEAST\ 2.6.6/bin/beast -threads 8 FinalModelStochastic.xml"], shell=True,
                        cwd=filepath)

        filepath = "/Users/LAB-SCG-125/Documents"
        subprocess.call(["Rscript /Users/LAB-SCG-125/Documents/StochasticSimulation.R"], shell=True, cwd=filepath)

        master_timestamps = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/timestamps.csv')

        master_S0 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S0.csv')
        master_R00 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R00.csv')
        master_R10 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R10.csv')
        master_I00 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I00.csv')
        master_I10 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I10.csv')
        master_I20 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I20.csv')
        master_I30 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I30.csv')

        master_S1 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S1.csv')
        master_R01 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R01.csv')
        master_R11 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/R11.csv')
        master_I01 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I01.csv')
        master_I11 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I11.csv')
        master_I21 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I21.csv')
        master_I31 = csv_to_list(
            '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/I31.csv')

        ax1[0, 1].plot(master_timestamps, master_S0, color='b', alpha = 0.5, linewidth=0.2, label='S0')
        ax1[0, 1].plot(master_timestamps, master_R00, color='g', alpha = 0.5, linewidth=0.2, label='S1')
        ax1[0, 1].plot(master_timestamps, master_R10, color='r', alpha = 0.5, linewidth=0.2, label='S2')
        if i == 0:
            ax1[0, 1].legend(loc='upper right', fontsize='x-small')

        ax2[0, 1].plot(master_timestamps, master_I00, color='b', alpha = 0.5, linewidth=0.2, label='A')
        ax2[0, 1].plot(master_timestamps, master_I10, color='g', alpha = 0.5, linewidth=0.2, label='C')
        ax2[0, 1].plot(master_timestamps, master_I20, color='r', alpha = 0.5, linewidth=0.2, label='T')
        ax2[0, 1].plot(master_timestamps, master_I30, color='m', alpha = 0.5, linewidth=0.2, label='G')
        if i == 0:
            ax2[0, 1].legend(loc='upper right', fontsize='x-small')

        ax1[1, 1].plot(master_timestamps, master_S1, color='b', alpha = 0.5, linewidth=0.2)
        ax1[1, 1].plot(master_timestamps, master_R01, color='g', alpha = 0.5, linewidth=0.2)
        ax1[1, 1].plot(master_timestamps, master_R11, color='r', alpha = 0.5, linewidth=0.2)

        ax2[1, 1].plot(master_timestamps, master_I01, color='b', alpha = 0.5, linewidth=0.2)
        ax2[1, 1].plot(master_timestamps, master_I11, color='g', alpha = 0.5, linewidth=0.2)
        ax2[1, 1].plot(master_timestamps, master_I21, color='r', alpha = 0.5, linewidth=0.2)
        ax2[1, 1].plot(master_timestamps, master_I31, color='m', alpha = 0.5, linewidth=0.2)