import subprocess
import matplotlib.pyplot as plt
from csv_to_list import csv_to_list

fig, axs = plt.subplots(nrows=2, ncols=2, sharex = True, sharey = True)
fig.suptitle('MASTER dispersion')

for i in range(20):
    filepath = "/Users/LAB-SCG-125/Documents/Master_sim"
    subprocess.call(["/Applications/BEAST\ 2.6.6/bin/beast -threads 8 FinalModelStochastic.xml"], shell = True, cwd=filepath)

    filepath = "/Users/LAB-SCG-125"
    subprocess.call(["Rscript /Users/LAB-SCG-125/StochasticSimulation.R"], shell = True, cwd=filepath)

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

    axs[0, 0].plot(master_timestamps, master_S0, color = 'b', linewidth = 0.1)
    axs[0, 0].plot(master_timestamps, master_R00, color = 'g', linewidth = 0.1)
    axs[0, 0].plot(master_timestamps, master_R10, color = 'r', linewidth = 0.1)

    axs[1, 0].plot(master_timestamps, master_I00, color = 'b', linewidth = 0.1)
    axs[1, 0].plot(master_timestamps, master_I10, color = 'g', linewidth = 0.1)
    axs[1, 0].plot(master_timestamps, master_I20, color = 'r', linewidth = 0.1)
    axs[1, 0].plot(master_timestamps, master_I30, color = 'k', linewidth = 0.1)

    axs[0, 1].plot(master_timestamps, master_S1, color = 'b', linewidth = 0.1)
    axs[0, 1].plot(master_timestamps, master_R01, color = 'g', linewidth = 0.1)
    axs[0, 1].plot(master_timestamps, master_R11, color = 'r', linewidth = 0.1)

    axs[1, 1].plot(master_timestamps, master_I01, color = 'b', linewidth = 0.1)
    axs[1, 1].plot(master_timestamps, master_I11, color = 'g', linewidth = 0.1)
    axs[1, 1].plot(master_timestamps, master_I21, color = 'r', linewidth = 0.1)
    axs[1, 1].plot(master_timestamps, master_I31, color = 'k', linewidth = 0.1)

filepath = "/Users/LAB-SCG-125/Documents/Master_sim"
subprocess.call(["/Applications/BEAST\ 2.6.6/bin/beast -threads 8 FinalModel.xml"], shell = True, cwd=filepath)

filepath = "/Users/LAB-SCG-125"
subprocess.call(["Rscript /Users/LAB-SCG-125/MasterSimulation.R"], shell = True, cwd=filepath)

master_timestamps = csv_to_list(
    '/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/timestamps.csv')

master_S0 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S0.csv')
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

master_S1 = csv_to_list('/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/master_plots/S1.csv')
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

axs[0, 0].plot(master_timestamps, master_S0, color = 'b', linewidth = 1, label = "S0")
axs[0, 0].plot(master_timestamps, master_R00, color = 'g', linewidth = 1, label = "R00")
axs[0, 0].plot(master_timestamps, master_R10, color = 'r', linewidth = 1, label = "R10")
axs[0, 0].legend(loc = 'upper right', fontsize = 'x-small')

axs[1, 0].plot(master_timestamps, master_I00, color = 'b', linewidth = 1, label = "I00")
axs[1, 0].plot(master_timestamps, master_I10, color = 'g', linewidth = 1, label = "I10")
axs[1, 0].plot(master_timestamps, master_I20, color = 'r', linewidth = 1, label = "I20")
axs[1, 0].plot(master_timestamps, master_I30, color = 'k', linewidth = 1, label = "I30")
axs[1, 0].legend(loc = 'upper right', fontsize = 'x-small')

axs[0, 1].plot(master_timestamps, master_S1, color = 'b', linewidth = 1, label = "S1")
axs[0, 1].plot(master_timestamps, master_R01, color = 'g', linewidth = 1, label = "R01")
axs[0, 1].plot(master_timestamps, master_R11, color = 'r', linewidth = 1, label = "R11")
axs[0, 1].legend(loc = 'upper right', fontsize = 'x-small')

axs[1, 1].plot(master_timestamps, master_I01, color = 'b', linewidth = 1, label = "I01")
axs[1, 1].plot(master_timestamps, master_I11, color = 'g', linewidth = 1, label = "I11")
axs[1, 1].plot(master_timestamps, master_I21, color = 'r', linewidth = 1, label = "I21")
axs[1, 1].plot(master_timestamps, master_I31, color = 'k', linewidth = 1, label = "I31")
axs[1, 1].legend(loc = 'upper right', fontsize = 'x-small')


plt.savefig('master_plots.png', dpi = 4000)
plt.show()