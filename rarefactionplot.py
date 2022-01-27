# (c) Sebastian Hupfauf 2022
#
# Script creates a rarefaction plot out of a given rarefaction file.
#
# USAGE: python rarefactionplot.py calculator fileformat dpi abundance_file
#        calculator: sobs, chao, shannon, simpson, coverage
#        fileformat: eps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff
#        dpi: figure resolution [int]
#        abundance_file: in .shared format

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import matplotlib
import random

matplotlib.use("Agg")

if sys.argv[1] == "sobs":
    infile = "abundance.groups.rarefaction"
    with open(sys.argv[4]) as abf:
        line = abf.readline()
    if "ASV" in line:
        ylabel = "ASVs"
        filename = "asv"
    elif "Zotu" in line:
        ylabel = "ZOTUs"
        filename = "zotu"
    elif "OTU" in line:
        ylabel = "OTUs"
        filename = "otu"
    else:
        ylabel = "Sobs"
        filename = "sobs"
if sys.argv[1] == "chao":
    infile = "abundance.groups.r_chao"
    ylabel = "Chao1 richness"
    filename = sys.argv[1]
if sys.argv[1] == "shannon":
    infile = "abundance.groups.r_shannon"
    ylabel = "H'"
    filename = sys.argv[1]
if sys.argv[1] == "simpson":
    infile = "abundance.groups.r_simpson"
    ylabel = "D"
    filename = sys.argv[1]
if sys.argv[1] == "coverage":
    infile = "abundance.groups.r_coverage"
    ylabel = "Coverage"
    filename = sys.argv[1]

ext = "." + sys.argv[2].lower()
dpi = int(sys.argv[3])

xaxis = []

with open(infile) as inf:
    labels = inf.readline().strip().split("\t")[1:]
    labels_cor = []
    for i in range(0, len(labels), 3):
        labels_cor.append(labels[i][5:]) 
    samples = [[] for x in range(len(labels_cor))]
    for line in inf:
        linelist = line.strip().split("\t")
        xaxis.append(int(linelist[0]))
        for i in range(len(labels_cor)):
            samples[i].append(linelist[1 + i * 3])

interval = np.linspace(0, 0.85, (int(len(samples) / 5) + 1) * 5)
colors = plt.cm.terrain(interval)
colors = [x[:-1]*255 for x in colors]
new_colors = []
for color in colors:
    new_colors.append([int(round(c, 0)) for c in color])
color_list = []
for color in new_colors:
    color_list.append('#%02x%02x%02x' % tuple(color))
chunks = []
for i in range(0, len(color_list), int(len(interval) / 5)):
    chunks.append(color_list[i : i + int(len(interval) / 5)])
color_list = []
for x in range(int(len(interval) / 5)):
    for y in range(len(chunks)):
        color_list.append(chunks[y][x])

for i in range(len(samples)):
    samples[i] = [float(x) for x in samples[i] if x != "NA"]
max_otus = [int(max(x)) for x in samples]
data = list(zip(max_otus, labels_cor, samples))
data.sort(reverse=True)
nlabels = [x[1] for x in data]
nsamples = [x[2] for x in data]
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for i in range(len(samples)):   
    plt.plot(xaxis[:len(nsamples[i])], nsamples[i], color=color_list[i])
locs, labels = plt.yticks()
if locs[2] > 1:
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
else:
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(round(float(x), 4))))
ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0)
plt.xlabel("Reads")
plt.ylabel(ylabel)
plt.xticks(rotation=90)
lgd = plt.legend(nlabels, loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, borderaxespad=0., ncol=int(len(samples) / 20) + 1, frameon=False)
plt.tight_layout()
plt.savefig("rarefactionplot_" + filename + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')           


