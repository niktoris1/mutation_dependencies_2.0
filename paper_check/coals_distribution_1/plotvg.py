from make_coal_plots import iterations, maxtime, points
import matplotlib.pyplot as plt
import re


k=0
n=100

for i in range(k, n):
    file = open("/Users/LAB-SCG-125/PycharmProjects/mutation_dependencies_2.0/paper_check/coals_distribution_1/" + str(
        i) + " vgsim", "r")
    data = file.read()

    vgsim_result = re.split(' ', data)[0:-1]

    for res_num in range(len(vgsim_result)):
        vgsim_result[res_num] = float(vgsim_result[res_num])

    line1 = plt.plot(points[1:], vgsim_result, color='red', linewidth = 0.1)
#line2 = a2.plot(points[1:], master_averaged, color='black', label = 'MASTER')
#f2.legend(bbox_to_anchor=(0.88, 0.87))

plt.savefig('vghists.png', dpi = 400)
plt.show()