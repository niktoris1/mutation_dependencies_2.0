#from vgsim import MakeVGsimCoals
#from master import MakeMasterCoals
from make_coal_plots import iterations, maxtime, points
import matplotlib.pyplot as plt
import re

k = 0
n = 100

number_of_bins = len(points) - 1
#vgsim_results = MakeVGsimCoals()
#master_results = MakeMasterCoals()

vgsim_averaged = [0 for _ in range(number_of_bins)]
master_averaged = [0 for _ in range(number_of_bins)]

for i in range(0, 70):
    file = open("/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/coals_distribution_1/" + str(
        i) + " vgsim", "r")
    data = file.read()

    vgsim_result = re.split(' ', data)[0:-1]

    for res_num in range(len(vgsim_result)):
        vgsim_result[res_num] = float(vgsim_result[res_num])

    print("MAX VGSIM", max(vgsim_result))

    for num in range(len(vgsim_result)):
        vgsim_averaged[num] += vgsim_result[num]

    #for result in vgsim_result:
    #    for i in range(number_of_bins):
    #        vgsim_averaged[i] += float(result)

for i in range(number_of_bins):
    vgsim_averaged[i] = vgsim_averaged[i] / n

for i in range(30, 100):
    file = open("/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/coals_distribution_1/" + str(
        i) + " vgsim", "r")
    data = file.read()

    master_result = re.split(' ', data)[0:-1]

    for res_num in range(len(master_result)):
        master_result[res_num] = float(master_result[res_num])

    print("MAX MASTER", max(master_result))


    for num in range(len(master_result)):
        master_averaged[num] += float(master_result[num])

    #for result in master_result:
    #    for i in range(number_of_bins):
    #        master_averaged[i] += float(result)

for i in range(number_of_bins):
    master_averaged[i] = master_averaged[i] / n

#fig1, ax1 = plt.subplots(nrows=1, ncols=2, sharey = 'all')

#for result in vgsim_results:
#    ax1[0].plot(points[1:], result, color='blue')

#for result in master_results:
#    ax1[1].plot(points[1:], result, color='orange', label='MASTER')


#fig1.text(0.3, 0.04, 'VGsim', ha='center', va='center', fontsize = 'large')
#fig1.text(0.74, 0.04, 'Master', ha='center', va='center', fontsize = 'large')
#fig1.savefig('compare_hist.png', dpi = 400)
#fig1.show()

f2, a2 = plt.subplots()

line1 = a2.plot(points[1:], vgsim_averaged, color='red', label = 'VGsim')
line2 = a2.plot(points[1:], master_averaged, color='black', label = 'MASTER')
f2.legend(bbox_to_anchor=(0.88, 0.87))

f2.savefig('compare_averaged.png', dpi = 400)
f2.show()