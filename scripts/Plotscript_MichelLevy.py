import numpy as np
import matplotlib.pyplot as plt

import Backend

# --- manual setup 
wavelengths    = np.arange(360, 831, 1)
birefringences = np.linspace(0, 0.05, 500, endpoint=True)
thicknesses    = np.linspace(0, 50, 200, endpoint=True)

cie_data_filename = "../files/ciexyz31_1.csv"

# --- automatic preparation
thickness = max(thicknesses)*1000
cie_data = Backend.load_cie_data(cie_data_filename)
XYZ_interpol = Backend.interpolate_cie_data(cie_data, wavelengths)
RGB = np.zeros([len(birefringences),3])

# --- automatic calculation
for i, biref in enumerate(birefringences):
    Gamma = biref*thickness
    color = Backend.calculate_interference_color(Gamma, wavelengths, XYZ_interpol)
    RGB[i,:] = color.ravel()
RGB = np.array(RGB)

plotimage = np.zeros([len(thicknesses),len(birefringences),3])
plotimage[:,:,0] = RGB[:,0]
plotimage[:,:,1] = RGB[:,1]
plotimage[:,:,2] = RGB[:,2]

#--------------------------------------------------------
#  PLOT
#--------------------------------------------------------

# --- setup
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
textprops = {"zorder":200, "size":9}
aspect = 30

# --- define axis limits
xlims = [min(thicknesses)*1000*min(birefringences),
         max(thicknesses)*1000*max(birefringences)]
ylims = [min(thicknesses), max(thicknesses)]

# --- plot image
ax.imshow(plotimage, origin="upper", 
          extent=xlims+ylims,
          zorder=1, aspect=aspect)

#--- adding lines of constant birefringence (and labels)
biref_label = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03,
              0.035, 0.04, 0.045, 0.05, 0.06, 0.07,
              0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.2]
minx = np.min(birefringences)
maxx = np.max(birefringences)
miny = np.min(thicknesses)

xscaler = (xlims[1]-xlims[0])/(max(birefringences)-min(birefringences))

for i,bl in enumerate(biref_label):
    xval = bl*xscaler
    lw = 0.5
    alpha = 0.5
    ax.plot((xlims[0], xval), ylims, zorder=100, color="black",lw=lw, alpha=alpha)
    
    #--- add text
    textrot = 180/np.pi*np.arctan(aspect*(ylims[1]-ylims[0])/(xval-xlims[0]))
    if xval <= xlims[1]:
        ax.text(xval, ylims[1], "  "+str(bl), ha="left", va="bottom", rotation=textrot, **textprops)
    else:
        ytext = ylims[0] + ( (xlims[1]-xlims[0])*((ylims[1]-ylims[0])/(xscaler*bl)) )
        ax.text(xlims[1], ytext, "  "+str(bl), ha="left", va="bottom", rotation=textrot, **textprops)

#--- adding lines and text for color orders
orders = np.arange(550, xlims[1]+550, 550)
orders_letters = ["I", "II", "III", "IV", "V", "VI", "VII", "IIX", "IX", "X"]

for order, letter in zip(orders, orders_letters):
    if order <= xlims[1]:
        ax.vlines(order, ylims[0], ylims[0]-8, clip_on=False, alpha=0.5, zorder=0, 
                  color="red", lw=2)
    ax.text(order-225, -8, letter, color="red", ha="center", va="bottom", clip_on=False)

#--- finalize plot (ticks, grid-lines) 
yticks =  list(np.arange(ylims[0], ylims[1]+5, 5))
xticks =  np.arange(xlims[0], xlims[1]+400, 400)
ax.set_xticklabels(["{:.0f}".format(_) for _ in xticks], rotation=90)

for yt in yticks:
    lw = 0.5
    alpha = 0.5
    ax.axhline(yt, zorder=100, color="black", lw=lw, alpha=alpha)
    
ax.set_yticks(yticks)
ax.set_xticks(xticks)

xminorticks =  np.arange(xlims[0], xlims[1], 100)
ax.set_xticks(xminorticks, minor=True)

ax.tick_params(axis="both", which="both",direction="out", top="off", right="off")

#--- finalize plot (labels, title)
ax.text(xlims[0], ylims[1]+1, "birefringence\n"+r"$\longrightarrow$", ha="center", va="bottom", **textprops)
ax.text(xlims[0], ylims[0]-3, r"path difference [nm]"+"\n"r"$\longrightarrow$", ha="center", va="top", **textprops)
ax.text(xlims[0], ylims[0]-8, r"color order", ha="center", va="bottom", color="red")
ax.set_ylabel(r"sample thickness [$\mathrm{\mu m}$]", **textprops)
plt.title("Calclulated Michel-Lévy color chart", y=1.15)

#--- finalize plot (set limits)
ax.set_xlim(*xlims)
ax.set_ylim(*ylims)

plt.show()
