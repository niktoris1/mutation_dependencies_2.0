from vgsim import MakeVGsimCoals
from master import MakeMasterCoals
from make_coal_plots import iterations, maxtime, points
import matplotlib.pyplot as plt

number_of_bins = len(points) - 1
vgsim_results = MakeVGsimCoals()
master_results = MakeMasterCoals()

vgsim_averaged = [0 for _ in range(number_of_bins)]
master_averaged = [0 for _ in range(number_of_bins)]

for result in vgsim_results:
    for i in range(number_of_bins):
        vgsim_averaged[i] += result[i]

for i in range(number_of_bins):
    vgsim_averaged[i] = vgsim_averaged[i] / iterations

for result in master_results:
    for i in range(number_of_bins):
        master_averaged[i] += result[i]

for i in range(number_of_bins):
    master_averaged[i] = master_averaged[i] / iterations

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