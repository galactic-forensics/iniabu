"""Create figure for internal normalization background information."""

import matplotlib.pyplot as plt

from iniabu import ini

# Create Ni abundances
ni_isos = ini.iso[["Ni-58", "Ni-60", "Ni-61", "Ni-62", "Ni-64"]]
ni_abu = ni_isos.abu_solar

# create a mass dependent fractionation of 10 per mille per amu
mf_facs = (ni_isos.mass / ini.iso["Ni-58"].mass) ** 0.6

# mass fractionated nickel abundances
ni_abu_mf = ni_abu * mf_facs

# now add another 10 per mille to Ni60
ni_abu_mf[1] *= 1.01

# ### REGULAR NORMALIZATION ###

# calculate delta value with respect to Ni58
ni_delta = ini.iso_delta("Ni", "Ni-58", ni_abu_mf / ini.iso["Ni-58"].abu_solar)
# plot the abundance vs the mass number
fig, ax = plt.subplots(1, 2, figsize=(8, 4))
ax[0].plot(
    ni_isos.mass,
    ni_delta,
    "-o",
    mfc="w",
    mew=2.0,
    linewidth=1,
    ms=8,
    label=r"$\delta$-values",
)
# define x limit
xlim = (57.5, 64.5)
# horizontal line
ax[0].hlines(0, xlim[0], xlim[1], linestyles="--", colors="k", linewidth=0.5)
# calculate fractionation trend line
xfrac = [ini.iso["Ni-58"].mass, ini.iso["Ni-64"].mass]
yfrac = [0.0, (mf_facs[-1] - 1) * 1000]
ax[0].plot(xfrac, yfrac, "tab:red", linestyle=":", label="Mass dependent fractionation")
# set styles
ax[0].set_xlim(xlim)
ax[0].legend(loc="upper left")
ax[0].set_title("Normalized to $^{58}$Ni")
ax[0].set_xlabel("Mass of isotope $^{i}$Ni")
ax[0].set_ylabel("$\\delta\\left(^{i}\\mathrm{Ni}/^{58}\\mathrm{Ni} \\right)$   (‰)")

# ### INTERNAL NORMALIZATION ###
ni_int_norm = ini.iso_int_norm(
    "Ni",
    ("Ni-58", "Ni-62"),
    ni_abu_mf,
    (ni_abu_mf[0], ni_abu_mf[3]),
    delta_factor=1000,
    law="exp",
)
# # make the plot
ax[1].plot(
    ni_isos.mass,
    ni_int_norm,
    "-o",
    mfc="w",
    mew=2.0,
    linewidth=1,
    ms=8,
    label=r"$\Delta$-values",
)
# horizontal line
ax[1].hlines(0, xlim[0], xlim[1], linestyles="--", colors="k", linewidth=0.5)
# set styles
ax[1].set_xlim(xlim)
ax[1].legend()
ax[1].set_title("Normalized internally to $^{58}$Ni and $^{62}$Ni")
ax[1].set_xlabel("Mass of isotope $^{i}$Ni")
ax[1].set_ylabel("$\\Delta^{i}\\mathrm{Ni}_{62/58}$   (‰)")

fig.tight_layout()
# fig.show()
fig.savefig("int_norm.png")
