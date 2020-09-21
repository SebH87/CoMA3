# (c) Sebastian Hupfauf 20017
#
# Script plots the data of a diversity file.
#
# USAGE: python diversity.py input_file fileformat dpi
#        fileformat: eps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff
#        dpi: figure resolution [int]

import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

matplotlib.use("Agg")

infile = sys.argv[1]
ext = "." + sys.argv[2].lower()
dpi = int(sys.argv[3])

samples = []
otus = []
shannon = []
chao = []
simpson = []

with open(infile) as inf:
    inf.readline()
    for line in inf:
        samples.append(line.strip().split("\t")[0])
        otus.append(float(line.strip().split("\t")[1]))
        shannon.append(float(line.strip().split("\t")[2]))
        chao.append(float(line.strip().split("\t")[3]))
        simpson.append(float(line.strip().split("\t")[4]))

if len(samples) < 20:
    size = 10
if len(samples) >=20 and len(samples) < 30:
    size = 8
if len(samples) >=30 and len(samples) < 40:
    size = 6
if len(samples) >=40 and len(samples) < 60:
    size = 4
if len(samples) >= 60:
    size = 2


sns.set_style("white", {"ytick.major.size": "3.0", "axes.edgecolor": ".15"})
colors=sns.color_palette("muted")
plt.subplot(2, 2, 1)
sns.despine()
sns.barplot(np.arange(len(otus)), otus, color=colors[0])
plt.xticks(np.arange(len(otus)), samples, rotation=90, fontsize=size)
plt.yticks(fontsize=size)
plt.title("OTUs")

plt.subplot(2, 2, 2)
sns.despine()
sns.barplot(np.arange(len(otus)), shannon, color=colors[1])
plt.xticks(np.arange(len(otus)), samples, rotation=90, fontsize=size)
plt.yticks(fontsize=size)
plt.title("Shannon Index")

plt.subplot(2, 2, 3)
sns.despine()
sns.barplot(np.arange(len(otus)), chao, color=colors[2])
plt.xticks(np.arange(len(otus)), samples, rotation=90, fontsize=size)
plt.yticks(fontsize=size)
plt.title("Chao1 Index")

plt.subplot(2, 2, 4)
sns.despine()
sns.barplot(np.arange(len(otus)), simpson, color=colors[3])
plt.xticks(np.arange(len(otus)), samples, rotation=90, fontsize=size)
plt.yticks(fontsize=size)
plt.title("Simpson Index")

plt.tight_layout()
plt.savefig("diversity" + ext, dpi=dpi)


