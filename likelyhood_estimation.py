import math
import sys

import scipy
import numpy as np
import scipy.stats
from scipy.stats.distributions import chi2
import statistics

from scipy import optimize
from scipy.optimize import Bounds
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from remove_stochastics import RemoveStochastics

import logging # a workaround to kill warnings
logging.captureWarnings(True)

class LikelyhoodEstimationDismembered:
    def __init__(self, event_table_funct=None, event_table_neutral=None, number_of_brackets=None, remove_stochastics=False, cutoff_for_stochastics=0.3):
        # here we have not tree, but tables

        def TakeEventTime(event):
            return event[0]

        def SetRoots(event_table):
            roots = []
            for event_tree in event_table:
                event_tree.sort(key=TakeEventTime)
                event_tree[0][4] = 'Root'
                for i in range(1, len(event_tree)):
                    event_tree[i][4] = 'Not root'
                roots.append(event_tree[0])

        SetRoots(event_table_neutral)
        SetRoots(event_table_funct)

        all_events = []
        all_neutral_events = []
        all_funct_events = []
        for event_table in event_table_neutral:
            for event in event_table:
                all_neutral_events.append(event)
                all_events.append(event)
        for event_table in event_table_funct:
            for event in event_table:
                all_funct_events.append(event)
                all_events.append(event)

        all_events.sort(key=TakeEventTime)
        all_funct_events.sort(key=TakeEventTime)
        all_neutral_events.sort(key=TakeEventTime)

        min_time = sys.maxsize
        max_time = -sys.maxsize

        def UpdateTimes(table, min_time, max_time):
            for subtable in table:
                for event in subtable:
                    if event[0] < min_time:
                        min_time = event[0]
                    if event[0] > max_time:
                        max_time = event[0]
            return min_time, max_time

        min_time, max_time = UpdateTimes(event_table_neutral, min_time, max_time)
        min_time, max_time = UpdateTimes(event_table_funct, min_time, max_time)

        timestamps = [_ for _ in np.linspace(min_time, max_time, number_of_brackets + 1, endpoint=True)]
        self.number_of_brackets = number_of_brackets

        #format of data is [left timestamp, number of samples, number_of coals, fraction]

        # bracket_data is a list of brackets Each corresponds to a timeframe
        # each bracket is a list of 4 values
        # 0) list of times
        # 1) list of indicators if the event is sample
        # 2) list of indicators if the event is coalescence
        # 3) Number of distinct lineages

        def SetLineages(sorted_events_list):
            current_lineages = 0
            for event_num in range(len(sorted_events_list)):
                if (sorted_events_list[event_num][2] == 1) and (sorted_events_list[event_num][4] == 'Root'): # is_coal and root
                    sorted_events_list[event_num][3] = current_lineages + 2
                elif (sorted_events_list[event_num][2] == 1) and (sorted_events_list[event_num][4] == 'Not root'): # is_coal and not root:
                    sorted_events_list[event_num][3] = current_lineages + 1
                elif (sorted_events_list[event_num][1] == 1) and (sorted_events_list[event_num][4] == 'Root'): # is_sample and root:
                    sorted_events_list[event_num][3] = current_lineages
                elif (sorted_events_list[event_num][1] == 1) and (sorted_events_list[event_num][4] == 'Not root'): # is_sample and not root:
                    sorted_events_list[event_num][3] = current_lineages - 1
                else:
                    raise ValueError
                current_lineages = sorted_events_list[event_num][3]

        SetLineages(all_funct_events)
        SetLineages(all_neutral_events)

        def CheckNegativity(event_table):
            for event in event_table:
                if event[3] < 0:
                    raise ValueError

        CheckNegativity(all_neutral_events)
        CheckNegativity(all_funct_events)

        if remove_stochastics:
            RemoveStochastics(all_neutral_events, cutoff_for_stochastics)
            RemoveStochastics(all_funct_events, cutoff_for_stochastics)

        def MapTimeToBracket(time, brackets, bracket_start_num, bracket_finish_num):
            test_bracket_num = (bracket_start_num + bracket_finish_num) // 2
            if (time < brackets[test_bracket_num][0]):
                return MapTimeToBracket(time, brackets, bracket_start_num, test_bracket_num - 1)
            elif (time > brackets[test_bracket_num][1]):
                return MapTimeToBracket(time, brackets, test_bracket_num + 1, bracket_finish_num)
            else:
                return test_bracket_num

        self.bracket_data_neutral = [[] for _ in range(self.number_of_brackets)]
        self.bracket_data_funct = [[] for _ in range(self.number_of_brackets)]

        brackets_borders = []
        for bracket_num in range(self.number_of_brackets):
            time_start, time_finish = timestamps[bracket_num], timestamps[bracket_num + 1]
            brackets_borders.append([time_start, time_finish])

        def PutEventsOnBrackets(event_list, brackets_borders, bracket_data):
            for event in event_list:
                bracket_num = MapTimeToBracket(event[0], brackets_borders, 0,
                                               len(brackets_borders))
                bracket_data[bracket_num].append(event)

        PutEventsOnBrackets(all_neutral_events, brackets_borders, self.bracket_data_neutral)
        PutEventsOnBrackets(all_funct_events, brackets_borders, self.bracket_data_funct)

        def SortEventsInBracketedData(bracket_data):
            for bracket in bracket_data:
                bracket.sort(key=TakeEventTime)

        SortEventsInBracketedData(self.bracket_data_neutral)
        SortEventsInBracketedData(self.bracket_data_funct)

        # we do a preprocessing of values for LLH
        # LLH = -coal_rate*coal_rate_multiplier + sum_of_logs

        # sums_of_logs equals number of coalescent events

        def SumEvents(dataEvents, sample_or_coal): # 0 stands for sample and 1 stands for coal
            number_of_events = 0
            if sample_or_coal == 0:
                for i in range(len(dataEvents)):
                    number_of_events += dataEvents[i][1]
            else:
                for i in range(len(dataEvents)):
                    number_of_events += dataEvents[i][2]
            return number_of_events

        def DetermineNumbersOfCoalsAndSamples(bracket_data):
            numbers_of_coals = [0 for _ in range(number_of_brackets)]
            numbers_of_samples = [0 for _ in range(number_of_brackets)]
            for bracket_num in range(len(bracket_data)):
                if bracket_data[bracket_num] == []:
                    numbers_of_coals[bracket_num] = 0
                    numbers_of_samples[bracket_num] = 0
                else:
                    numbers_of_coals[bracket_num] = SumEvents(bracket_data[bracket_num], 1)
                    numbers_of_samples[bracket_num] = SumEvents(bracket_data[bracket_num], 0)
            return numbers_of_coals, numbers_of_samples

        self.numbers_of_coals_neutral, self.numbers_of_samples_neutral = DetermineNumbersOfCoalsAndSamples(self.bracket_data_neutral)
        self.numbers_of_coals_funct, self.numbers_of_samples_funct = DetermineNumbersOfCoalsAndSamples(self.bracket_data_funct)

        overall_number_of_neutral_vertices = sum(self.numbers_of_coals_neutral) + sum(self.numbers_of_samples_neutral)
        overall_number_of_funct_vertices = sum(self.numbers_of_coals_funct) + sum(self.numbers_of_samples_funct)
        overall_number_of_sample_vertices = sum(self.numbers_of_samples_neutral) + sum(self.numbers_of_samples_funct)
        overall_number_of_coal_vertices = sum(self.numbers_of_coals_neutral) + sum(self.numbers_of_coals_funct)

        overall_number_of_vertices = overall_number_of_neutral_vertices + overall_number_of_funct_vertices

        print("There are", overall_number_of_neutral_vertices, "vertices with a neutral haplotype out of",
              overall_number_of_vertices)
        print("Overall", overall_number_of_sample_vertices, "vertices were sampled out of", overall_number_of_vertices)



    def GetEstimationConstants(self): # returns an estimation of the s_i with respect to rho

        # here we define constants in the LLH_1 and LLH_2 as follows
        # the LLH results in the formula for neutral and funct cases
        # c_1 * \lambda - number_of_coals_neutral * log \lambda + c_2
        # c_3 * (\rho * \lambda) - number_of_coals_funct * log (\lambda * \rho) + c_4

        c1s = [0 for _ in range(self.number_of_brackets)]
        c3s = [0 for _ in range(self.number_of_brackets)]

        current_neutral_lineages = 0
        current_neutral_time = 0
        for timestamp_num in range(self.number_of_brackets):
            if len(self.bracket_data_neutral[timestamp_num]) > 0:
                if timestamp_num == 0:
                    for j in range(1, len(self.bracket_data_neutral[timestamp_num])):
                        c1s[timestamp_num] += (self.bracket_data_neutral[timestamp_num][j][0] -
                                               self.bracket_data_neutral[timestamp_num][j - 1][0]) * \
                                              math.comb(self.bracket_data_neutral[timestamp_num][j - 1][3], 2)
                else:
                    c1s[timestamp_num] += (self.bracket_data_neutral[timestamp_num][0][0] -
                                               current_neutral_time) * \
                                              math.comb(current_neutral_lineages, 2)
                    for j in range(1, len(self.bracket_data_neutral[timestamp_num])):
                        c1s[timestamp_num] += (self.bracket_data_neutral[timestamp_num][j][0] -
                                               self.bracket_data_neutral[timestamp_num][j - 1][0]) * \
                                              math.comb(self.bracket_data_neutral[timestamp_num][j - 1][3], 2)

                current_neutral_time = self.bracket_data_neutral[timestamp_num][-1][0]
                current_neutral_lineages = self.bracket_data_neutral[timestamp_num][-1][3]
            else:
                continue

        current_funct_lineages = 0
        current_funct_time = 0
        for timestamp_num in range(self.number_of_brackets):
            if len(self.bracket_data_funct[timestamp_num]) > 0:
                if timestamp_num == 0:
                    for j in range(1, len(self.bracket_data_funct[timestamp_num])):
                        c3s[timestamp_num] += (self.bracket_data_funct[timestamp_num][j][0] -
                                               self.bracket_data_funct[timestamp_num][j - 1][0]) * \
                                              math.comb(self.bracket_data_funct[timestamp_num][j - 1][3], 2)
                else:
                    c3s[timestamp_num] += (self.bracket_data_funct[timestamp_num][0][0] -
                                               current_funct_time) * \
                                              math.comb(current_funct_lineages, 2)
                    for j in range(1, len(self.bracket_data_funct[timestamp_num])):
                        c3s[timestamp_num] += (self.bracket_data_funct[timestamp_num][j][0] -
                                               self.bracket_data_funct[timestamp_num][j - 1][0]) * \
                                              math.comb(self.bracket_data_funct[timestamp_num][j - 1][3], 2)

                current_funct_time = self.bracket_data_funct[timestamp_num][-1][0]
                current_funct_lineages = self.bracket_data_funct[timestamp_num][-1][3]
            else:
                continue

        return c1s, c3s


    def GetLLHOptimumTotal(self, rho):

        #returns estimations for lambdas and for the sum

        c1s, c3s = self.GetEstimationConstants()

        self.lambdas = [0 for _ in range(self.number_of_brackets)]
        LLHOptimumResultsNoConstantTerm = [0 for _ in range(self.number_of_brackets)]
        self.estimated_infected_ratio = [0 for _ in range(self.number_of_brackets)]

        for timestamp_num in range(self.number_of_brackets):
            if (self.numbers_of_coals_neutral[timestamp_num] + self.numbers_of_coals_funct[timestamp_num] == 0) \
                or (self.numbers_of_samples_funct[timestamp_num] == 0):
                LLHOptimumResultsNoConstantTerm[timestamp_num] = 0
                # since we don't know enough, it doesn't influence the LLH
            else:
                self.estimated_infected_ratio[timestamp_num] = self.numbers_of_samples_neutral[timestamp_num] / self.numbers_of_samples_funct[timestamp_num]
                self.lambdas[timestamp_num] = (self.numbers_of_coals_neutral[timestamp_num] + self.numbers_of_coals_funct[timestamp_num]) / \
                                         (c1s[timestamp_num] + c3s[timestamp_num] * self.estimated_infected_ratio[timestamp_num] * rho)
                #experimental - we eliminate a constant term (c1s[timestamp_num] + c3s[timestamp_num] * estimated_infected_ratio[timestamp_num] * rho) * lambdas[timestamp_num]
                LLHOptimumResultsNoConstantTerm[timestamp_num] = - (self.numbers_of_coals_neutral[timestamp_num] + self.numbers_of_coals_funct[timestamp_num]) * math.log(self.lambdas[timestamp_num]) - \
                    self.numbers_of_coals_funct[timestamp_num] * math.log(rho)

        result = sum(LLHOptimumResultsNoConstantTerm)
        # we use an addition, since we work with the logarithms

        return result

    def OptimiseLLH(self):
        overall_optimizer = lambda rho: self.GetLLHOptimumTotal(rho)
        optimum = scipy.optimize.minimize_scalar(fun=overall_optimizer, bracket=(0.2, 5), bounds=(0.001, 1000000), method='Bounded', tol=0.0001)
        #optimum = scipy.optimize.minimize(fun=overall_optimizer, x0=1, method='Nelder-Mead')
        plt.show()
        return optimum

    def PlotLLH(self, precision):
        results = [0 for _ in range(precision)]
        input_data = [0.1*i for i in range(1, precision+1)]
        # we need a minimum here

        for i in range(precision):
            results[i] = - self.GetLLHOptimumTotal(input_data[i])

        plt.plot(input_data, results)
        plt.show()
        return 0

    def ConductLikelyhoodRatioTest(self, optimal_parameter, current_parameter):

        optimal_LLH = self.GetLLHOptimumTotal(optimal_parameter)
        current_LLH = self.GetLLHOptimumTotal(current_parameter)

        lr = 2 * (current_LLH - optimal_LLH)
        p = chi2.cdf(lr, 1)

        #if p < 0.05:
        #    print("Likelyhood ratio test has passed")
        #else:
        #    print("WARNING, likelyhood ratio test has failed")

        return p

    def ComuteConfidenceIntervals(self, optimal_parameter, p):
        min_border = optimal_parameter
        max_border = optimal_parameter
        while (self.ConductLikelyhoodRatioTest(optimal_parameter, min_border) < p):
            min_border -= 0.001
        while (self.ConductLikelyhoodRatioTest(optimal_parameter, max_border) < p):
            max_border += 0.001
        print('Confidence interval for value', optimal_parameter, 'is [', min_border, ',', max_border, ']')
        return [min_border, max_border]



