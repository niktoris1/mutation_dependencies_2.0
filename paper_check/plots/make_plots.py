import matplotlib.pyplot as plt

number_of_plots = 100

fig1, ax1 = plt.subplots(nrows=2, ncols=2, sharex = 'all', sharey = 'all')
fig2, ax2 = plt.subplots(nrows=2, ncols=2, sharex = 'all', sharey = 'all')

fig1.subplots_adjust(left=0.15,
                    bottom=0.15,
                    right=0.9,
                    top=0.9,
                    wspace=0.1,
                    hspace=0.3)

fig2.subplots_adjust(left=0.15,
                    bottom=0.15,
                    right=0.9,
                    top=0.9,
                    wspace=0.1,
                    hspace=0.3)


fig1.text(0.52, 0.94, 'Population 1', ha='center', va='center', fontsize = 'large')
fig1.text(0.52, 0.52, 'Population 2', ha='center', va='center', fontsize = 'large')
fig2.text(0.52, 0.94, 'Population 1', ha='center', va='center', fontsize = 'large')
fig2.text(0.52, 0.52, 'Population 2', ha='center', va='center', fontsize = 'large')
fig1.text(0.52, 0.05, 'Time', ha='center', va='center')
fig1.text(0.05, 0.53, 'Counts', ha='center', va='center', rotation='vertical')
fig2.text(0.52, 0.05, 'Time', ha='center', va='center')
fig2.text(0.05, 0.53, 'Counts', ha='center', va='center', rotation='vertical')

fig1.text(0.34, 0.04, 'VGsim', ha='center', va='center', fontsize = 'large')
fig1.text(0.74, 0.04, 'Master', ha='center', va='center', fontsize = 'large')

fig2.text(0.34, 0.04, 'VGsim', ha='center', va='center', fontsize = 'large')
fig2.text(0.74, 0.04, 'Master', ha='center', va='center', fontsize = 'large')

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])