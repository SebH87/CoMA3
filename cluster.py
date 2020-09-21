# (c) Sebastian Hupfauf 20017
#
# Script computes a hierarchical clustering of samples given in a OTU-table
# file (in shared format) and saves a dendrogram plot.
#
# USAGE: python cluster.py otu_table_file method metric annotation fileformat dpi color_threshold(optional)
#       -> method: single, complete, average, centroid, weighted, median, ward
#       -> metric: euclidean, cityblock, cosine, correlation, jaccard, braycurtis, dice, ...
#       -> annotation: True, False
#       -> fileformat: eps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff
#       -> dpi: figure resolution [int]
#       -> color_threshold [0, 100]: Enter percent similarity, before a new color is assigned

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, set_link_color_palette
from scipy.spatial.distance import pdist
import sys

matplotlib.use("Agg")

infile = sys.argv[1]
method = sys.argv[2]
metric = sys.argv[3]
try:
        perc = float(sys.argv[7])/100
except:
        perc = 0.7
if sys.argv[4] == "Yes": 
        annotate = "True"
else:
        annotate = "False"
if method in ["centroid", "median", "ward"]:
    if metric != "euclidean":
        print("\nATTENTION: centroid, median and ward methods REQUIRE the euclidean metric!")
        print("No files are created!")
        sys.exit()
ext = "." + sys.argv[5].lower()
dpi = int(sys.argv[6])

datamatrix = []
samples = []

with open(infile) as inf:
    otus = inf.readline().strip().split("\t")[3:]
    for line in inf:
        datamatrix.append([int(x) for x in line.strip().split("\t")[3:]])
        samples.append(line.strip().split("\t")[1])

datamatrix = np.array(datamatrix)
lmatrix = linkage(datamatrix, method=method, metric=metric)

groups = 4
interval = np.linspace(0, 0.85, groups)
colors = plt.cm.terrain(interval)
colors = [tuple(x) for x in colors]

color_list = []
for color in colors:
    hexcode = "#"
    for val in color:
        hexcode += hex(int(val*255))[2:]
    color_list.append(hexcode)
set_link_color_palette(color_list)

max_dist = max(lmatrix[:,2])

plt.figure(figsize=(20, 10))
matplotlib.rcParams.update({'font.size': 20})
plt.title('Hierarchical Clustering Dendrogram')
plt.ylabel('distance')
x = dendrogram(lmatrix, leaf_font_size=20., labels=samples, leaf_rotation=90.,
                        color_threshold=max_dist*perc, above_threshold_color='black')
if annotate == "True":
    for i, d, c in zip(x['icoord'], x['dcoord'], x['color_list']):
                x = 0.5 * sum(i[1:3])
                y = d[1]
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                    textcoords='offset points',
                    va='top', ha='center')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.ylabel(metric + " distance")
plt.tight_layout()
plt.savefig("dendrogram_%s_%s"%(method, metric) + ext, dpi=dpi)
