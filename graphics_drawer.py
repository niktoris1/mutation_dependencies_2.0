import matplotlib.pyplot as plt

def MakeHist(data_aray, frequency):
    data_min = min(data_aray)
    data_max = max(data_aray)
    bin_borders = [data_min + i * (data_max - data_min) / frequency for i in range(frequency+1)]
    plt.hist(x=data_aray, bins=bin_borders, alpha=0.7, rwidth=0.85)
    plt.show()

def TimesFromEvents(events_list, event_type):
    def is_sample(event):
        return bool(event[1])

    def is_coal(event):
        return bool(event[2])

    if event_type == 1:
        events_list = list(filter(lambda x: x[1] == 0, events_list))
    else:
        events_list = list(filter(lambda x: x[1] == 1, events_list))
    return [events_list[num][0] for num in range(len(events_list))]
