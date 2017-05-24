import numpy as np
import matplotlib.pyplot as plt

import Backend

#--- manual setup
wavelengths    = np.arange(360, 831, 1)
birefringences = np.linspace(0, 0.1, 500, endpoint=True)
thicknesses    = np.linspace(0, 50, 200, endpoint=True)
cie_data_filename = "../files/ciexyz31_1.csv"

# --- automatic preparation
cie_data = Backend.load_cie_data(cie_data_filename)
XYZ_interpol = Backend.interpolate_cie_data(cie_data, wavelengths)

#--- calculation
plotimage = np.zeros([len(thicknesses), len(birefringences), 3])
for n, thickness in enumerate(thicknesses):
    for m, biref in enumerate(birefringences):
        Gamma = biref*thickness*1000
        color = Backend.calculate_interference_color(Gamma, wavelengths, XYZ_interpol)
        plotimage[n,m,:] = color

#--- plotting 
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)

xlims = [min(birefringences), max(birefringences)]
ylims = [min(thicknesses), max(thicknesses)]
aspect = 10**-3

ax.imshow(np.flipud(plotimage), origin="upper", extent=xlims+ylims, aspect=aspect,zorder=1) 
ax.set_xlabel("birefringence")
ax.set_ylabel("sample thickness [$\mathrm{\mathrm{\mu m}}$]")

ax.minorticks_on()
ax.grid("on", which="major", ls="-", lw=0.5, alpha=0.5)
ax.grid("on", which="minor", ls="-", lw=0.5, alpha=0.2)
ax.tick_params(which="both", direction="out", right="off", top="off")

plt.show()
