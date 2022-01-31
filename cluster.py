# (c) Sebastian Hupfauf 2022
#
# Script computes a hierarchical clustering of samples given in a OTU-table
# file (in shared format) and saves a dendrogram plot.
#
# USAGE: python cluster.py otu_table_file method metric annotation fileformat dpi color_threshold(optional)
#       -> method: single, complete, average, centroid, weighted, median, ward
#       -> metric: euclidean, cityblock, cosine, correlation, jaccard, braycurtis, dice, ...
#       -> annotation: Yes, No
#       -> fileformat: eps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff
#       -> dpi: figure resolution [int]
#       -> color_threshold [0, 100]: Enter percent similarity, before a new color is assigned

import matplotlib
import sys
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import zenipy as zp
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, set_link_color_palette
from scipy.spatial.distance import pdist
from matplotlib.lines import Line2D

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

#Color-coding of samples

answer = zp.question(title="CoMA3", text="Do you want to use metadata to colour your sample names?")

if answer == True:

    map_file = "mapping.txt"
    try:
        map_df = pd.read_csv(map_file, delimiter="\t", index_col=0)
    except:
        print("ATTENTION: Mapping file ('mapping.txt') could not be found! Process is terminated and no dendrogram is created!")
        sys.exit(1)

    if len(map_df.columns) > 1:
        var = zp.entry(title="CoMA3", text="Based on which metadata variable do you want to colour your sample names?\n\nYou can select between the following variables:\n\n" + ", ".join(map_df.columns) + "\n")
    else:
        var = map_df.columns[0]
        print("Only 1 metadata variable detected, variable '%s' was selected!"%(var))
    
    if not var in map_df.columns:
        zp.error(title="CoMA3", text="ATTENTION: Metadata variable '%s' could not be found! Cluster analysis cannot be calculated and no plot is created!"%(var))
        sys.exit(1)

    start = time.time()
  
    if map_df[var].nunique() > 5:
        interv = np.linspace(0, 0.7, map_df[var].nunique())
    elif map_df[var].nunique() == 2:
        interv = np.linspace(0, 0.3, 2)
    else:
        interv = np.linspace(0, 0.55, map_df[var].nunique())  
    colors = plt.cm.terrain(interv)
    colors = [x[:-1]*255 for x in colors]
    color_list = []
    for color in colors:
        color = [hex(int(round(x, 0)))[2:] for x in color]
        color_list.append("#" + "".join(color))
    random.shuffle(color_list)
  
    meta_groups = []
    legend_elements = []
    for v in range(len(map_df[var].unique())):
        meta_groups.append(list(map_df[map_df[var] == map_df[var].unique()[v]].index))
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label=map_df[var].unique()[v], markerfacecolor=color_list[v], markersize=15))

    for tick in ax.get_xticklabels():
        sname = tick.get_text()
        for i in range(len(meta_groups)):
            if sname in meta_groups[i]:
                tick.set_color(color_list[i])
            
    ax.legend(handles=legend_elements, loc='right', frameon=False)
    plt.ylabel(metric + " distance")
    plt.tight_layout()
    plt.savefig("dendrogram_%s_%s_%s"%(method, metric, var) + ext, dpi=dpi)
else:
    start = time.time()
    
    plt.ylabel(metric + " distance")
    plt.tight_layout()
    plt.savefig("dendrogram_%s_%s"%(method, metric) + ext, dpi=dpi)
    
end = time.time()
print("\nProcess succeeded! Dendrogram created! (Duration: %is)\n"%(int(round((end - start), 0))))
