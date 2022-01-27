# (c) Sebastian Hupfauf 2022
#
# Script creates ordination (beta diversity) plots out of a provided OTU-table
# file using a given metric. Optionally, a tree file can be provided in order to
# calculate the weithed- or unweighted unifrac distance.
#
# USAGE: python ordination_mapped.py otu_table metric mapping_file tree_file/p-norm(optional)
#        metric: Weighted_unifrac, Unweighted_unifrac, Minkowski, Euclidean, 
#                Manhattan, Cosine, Jaccard, Canberra, Chebyshev, Braycurtis, Dice
#        mapping_file: CoMA3 formatted mapping file (tab-delimited TXT format)
#        tree_file: in NEWICK format (solely used for Weighted/Unweighted_unifrac)
#        p-norm: integer > 2 (solely used for Minkowski)

import sys
import matplotlib
import time
import random
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
from skbio.diversity import beta_diversity, get_beta_diversity_metrics
from skbio.stats.ordination import pcoa
from skbio.stats.distance import anosim, permanova
from skbio import TreeNode
import pandas as pd
import seaborn as sns
import zenipy as zp
import numpy as np
import matplotlib.pyplot as plt

table = sys.argv[1]
metric = sys.argv[2]
if metric == "Weighted_unifrac":
    metric = "weighted_unifrac"
    mname = "weighted_unifrac"
if metric == "Unweighted_unifrac":
    metric = "unweighted_unifrac"
    mname = "unweighted_unifrac"
if metric == "Euclidean":
    metric = "euclidean"
    mname = "euclidean"
if metric == "Manhattan":
    metric = "cityblock"
    mname = "manhattan"
if metric == "Cosine":
    metric = "cosine"
    mname = "cosine"
if metric == "Jaccard":
    metric = "jaccard"
    mname = "jaccard"
if metric == "Canberra":
    metric = "canberra"
    mname = "canberra"
if metric == "Chebyshev":
    metric = "chebyshev"
    mname = "chebyshev"
if metric == "Braycurtis":
    metric = "braycurtis"
    mname = "braycurtis"
if metric == "Dice":
    metric = "dice"
    mname = "dice"

map_file = sys.argv[3]
map_DF = pd.read_csv(map_file, delimiter="\t", index_col=0)

if metric == "weighted_unifrac" or metric == "unweighted_unifrac":
    try:
        tree_file = sys.argv[4]
    except:
        zp.error(title="CoMA3", text="A tree file is required for the calculation of the Unifrac distance!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)

if metric == "Minkowski":
    try:
        p = int(sys.argv[4])
    except:
        zp.error(title="CoMA3", text="P-norm must be a positive integer!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    if p < 1:
        zp.error(title="CoMA3", text="P-norm must be a positive integer!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    metric = "minkowski"
    mname = "minkowski"      

if len(map_DF.columns) > 1:
    var = zp.entry(title="CoMA3", text="Based on which metadata variable do you want to color your samples?\n\nYou can select between the following variables:\n\n" + ", ".join(map_DF.columns) + "\n")
else:
    var = map_DF.columns[0]
    print("Only 1 metadata variable detected, variable '%s' was selected!"%(var))
 
if not var in map_DF.columns:
    zp.error(title="CoMA3", text="ATTENTION: Metadata variable '%s' could not be found! Beta diversity cannot be calculated and no plots are created!"%(var))
    sys.exit(1)    
    
three = zp.question(title="CoMA3", text="Do you want to see a 3D illustration of your ordination?")
two = zp.question(title="CoMA3", text="Do you want to create a two-dimensional plot of your ordination?")

if two == True:
    ftype = zp.entry(title="CoMA3", text="Which fileformat do you prefer?\n\neps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff\n")
    if ftype == None:
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    elif ftype not in ["eps", "jpeg", "pdf", "png", "ps", "raw", "rgba", "svg", "svgz", "tiff"]:
        zp.error(title="CoMA3", text="Invalid Input, process terminated!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    else:
        if mname == "minkowski":
            figname = "PCoA_" + mname + "_p" + str(p) + "_" + var + "." + ftype 
        else:
            figname = "PCoA_" + mname + "_" + var + "." + ftype 

    if ftype in ["jpeg", "png", "raw", "rgba", "tiff"]:
        dpi = zp.entry(title="CoMA3", text="Please enter the resolution [dpi]:")
        if dpi == None:
            print("\nProcess terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
        try:
            dpi = int(dpi)
        except:
            zp.error(title="CoMA3", text="Invalid Input, process terminated!")
            print("\nProcess terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
    else:
        dpi = 200

start = time.time()
print("\nBeta diversity calculation proceeding ...")

data = []
otus = []

with open(table) as inf:
    inf.readline()
    names = inf.readline().split("\t")[1:-1]
    for line in inf:
        data.append([int(float(x)) for x in line.split("\t")[1:-1]])
        otus.append(line.split("\t")[0])

otus = [x.replace("_", " ") for x in otus]
df = pd.DataFrame(data, index=otus, columns=names)

if metric == "weighted_unifrac" or metric == "unweighted_unifrac":       
    tree = TreeNode.read(tree_file)
    div = beta_diversity(metric, df.T, ids=names, otu_ids=otus, tree=tree, validate=False) 
elif metric == "minkowski":
    div = beta_diversity(metric, df.T, names, p=p)
else:
    div = beta_diversity(metric, df.T, names)

div_df = div.to_data_frame()
if metric == "minkowski":
    div_df.to_csv("distancematrix_" + mname + "_p" + str(p) + ".txt", sep="\t")
else:
    div_df.to_csv("distancematrix_" + mname + ".txt", sep="\t")

pc = pcoa(div)

map_DF.index = pc.samples.index

warn = 0
for ev in pc.eigvals:
    if ev < 0:
        warn += 1
if warn > 0:
    zp.error(title="CoMA3", text="ATTENTION: At least 1 of your eigenvalues is negative, potentially leading to problems! You may want to choose another metric for distance calculation or apply data transformation on the distance matrix (e.g. square root) to get rid of this problem.")

eig_dm = pd.DataFrame(pc.eigvals, columns=["Eigenvalue"])
eig_dm["Explained"] = pc.proportion_explained
eig_dm["Summed_explanation"] = pc.proportion_explained.cumsum()
if metric == "minkowski":
    eig_dm.to_csv("eigenvalues_" + mname + "_p" + str(p) + ".txt", sep="\t")
else:
    eig_dm.to_csv("eigenvalues_" + mname + ".txt", sep="\t")

#Statistics

anos = anosim(div, map_DF, column=var, permutations=999)
perm = permanova(div, map_DF, column=var, permutations=999)

if metric == "minkowski":
    stat_file = "statistics_" + mname + "_p" + str(p) + "_" + var + ".txt"
else:
    stat_file = "statistics_" + mname + "_" + var + ".txt"

with open(stat_file, "w") as st:
    st.write("ANOSIM\tPermutations: 999\n\n")
    st.write("R\t" + str(anos["test statistic"]) + "\n")
    st.write("p-value\t" + str(anos["p-value"]) + "\n\n")
    st.write("PERMANOVA\tPermutations: 999\n\n")
    st.write("F\t" + str(perm["test statistic"]) + "\n")
    st.write("p-value\t" + str(perm["p-value"]) + "\n\n")

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Beta diversity calculations are finished!"%dur)
print("")
print("Distance metric: " + mname[0].upper() + mname[1:])
if mname == "minkowski":
    print("P-norm: " + str(p))
print("\n________________________________________________________________________________\n")

if map_DF[var].nunique() > 5:
    interval = np.linspace(0, 0.7, map_DF[var].nunique())
elif map_DF[var].nunique() == 2:
    interval = np.linspace(0, 0.3, 2)
else:
    interval = np.linspace(0, 0.55, map_DF[var].nunique())
colors = plt.cm.terrain(interval)
colors = [x[:-1]*255 for x in colors]
color_list = []
for color in colors:
    color = [hex(int(round(x, 0)))[2:] for x in color]
    color_list.append("#" + "".join(color))
random.shuffle(color_list)
sns.set_palette(sns.color_palette(color_list))
my_cmap = ListedColormap(sns.color_palette(color_list))

if three == True:
    fig = pc.plot(map_DF, var, axis_labels=('PC 1', 'PC 2', 'PC 3'), cmap=my_cmap, s=50)
    plt.show()

if two == True:
    matplotlib.use("Agg")
    sns.set_style("ticks")
    DF = pd.concat([pc.samples, map_DF], axis=1)
    ax = sns.scatterplot(data=DF, x="PC1", y="PC2", hue=var)
    plt.legend(frameon=False, loc='upper left', bbox_to_anchor=(1.04, 1), ncol=1)
    plt.xlabel("PC 1 (" + str(round(pc.proportion_explained[0] * 100, 2)) + "%)")
    plt.ylabel("PC 2 (" + str(round(pc.proportion_explained[1] * 100, 2)) + "%)")
    plt.savefig(figname, dpi=dpi, bbox_inches='tight')
