import matplotlib.pyplot as plt

from make_plots import fig1, fig2, ax1, ax2
from master_plots import make_master_plots
from VGsim_plots import make_vgsim_plots

make_master_plots()
make_vgsim_plots()

fig1.savefig('f1', dpi = 400)
fig2.savefig('f2', dpi = 400)

plt.show()