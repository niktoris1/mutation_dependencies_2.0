import os
import matplotlib.pyplot as plt
import data_preparation_real

from pb_to_event_table import shishkin_funct_table, shishkin_neutral_table
from likelyhood_estimation import LikelyhoodEstimationDismembered

frequency = 100

arr = [0 for i in range(frequency)]

for i in range(frequency):

    nub = i+1

    LED = LikelyhoodEstimationDismembered(event_table_funct=shishkin_funct_table,
                                              event_table_neutral=shishkin_neutral_table,
                                              number_of_brackets=nub,
                                          remove_stochastics=False,
                                          cutoff_for_stochastics=0.0)

    optimum = LED.OptimiseLLH()
    rho = optimum.x
    LLH_observed = optimum.fun
    #LED.PlotLLH(precision=20)
    print("Rho equals:", rho)
    arr[i] = rho

plt.plot(arr)
plt.show()

#LED.ComputeConfidenceIntervals(rho, 0.05)
os.system('say "your program has finished"')

