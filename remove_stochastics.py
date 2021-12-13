import math

def RemoveStochastics(table, share): # share indicated how much of a time perioud we remove in the beginning
    times = [0 for _ in range(len(table))]
    for event_num in range(len(table)):
        times[event_num] = table[event_num][0]

    times.sort()
    cutout_time = times[math.floor(len(times) * share)]

    for event in table: # can be fastened for the presorted table
        if event[0] < cutout_time:
            table.remove(event)

    return table
