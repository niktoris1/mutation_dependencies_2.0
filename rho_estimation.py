import os

from pb_to_event_table import shishkin_funct_table, shishkin_neutral_table
from likelyhood_estimation import LikelyhoodEstimationDismembered

frequency = 1

LED = LikelyhoodEstimationDismembered(event_table_funct=shishkin_funct_table,
                                          event_table_neutral=shishkin_neutral_table,
                                          number_of_brackets=frequency,
                                      remove_stochastics=True,
                                      cutoff_for_stochastics=0.0)

optimum = LED.OptimiseLLH()
rho = optimum.x
LLH_observed = optimum.fun
LED.PlotLLH(precision=20)
print("Rho equals:", rho)

LED.ComuteConfidenceIntervals(rho, 0.05)
#os.system('say "your program has finished"')

