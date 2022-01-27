# (c) Sebastian Hupfauf 2022
#
# Script creates ordination (beta diversity) plots out of a provided OTU-table
# file using a given metric. Optionally, a tree file can be provided in order to
# calculate the weithed- or unweighted unifrac distance.
#
# USAGE: python ordination.py otu_table metric tree_file/p-norm(optional)
#        metric: Weighted_unifrac, Unweighted_unifrac, Minkowski, Euclidean, 
#        Manhattan, Cosine, Jaccard, Canberra, Chebyshev, Braycurtis, Dice
#        tree_file: in NEWICK format (solely used for Weighted/Unweighted_unifrac)
#        p-norm: integer > 2 (solely used for Minkowski)

import sys
import matplotlib
import time
from skbio.diversity import beta_diversity, get_beta_diversity_metrics
from skbio.stats.ordination import pcoa
from skbio import TreeNode
import pandas as pd
import seaborn as sns
import zenipy as zp
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

if metric == "weighted_unifrac" or metric == "unweighted_unifrac":
    try:
        tree_file = sys.argv[3]
    except:
        zp.error(title="CoMA3", text="A tree file is required for the calculation of the Unifrac distance!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)

if metric == "Minkowski":
    try:
        p = int(sys.argv[3])
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
            figname = "PCoA_" + mname + "_p" + str(p) + "." + ftype 
        else:
            figname = "PCoA_" + mname + "." + ftype 

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

    col = zp.color_selection(title="CoMA3")
    col = [float(x) / 255 for x in col[4:-1].split(",")]

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

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Beta diversity calculations are finished!"%dur)
print("")
print("Distance metric: " + mname[0].upper() + mname[1:])
if mname == "minkowski":
    print("P-norm: " + str(p))
print("\n________________________________________________________________________________\n")

if three == True:
    fig = pc.plot()
    plt.show()

if two == True:
    matplotlib.use("Agg")
    sns.set_style("ticks")
    sns.scatterplot(data=pc.samples, x="PC1", y="PC2", color=col)
    plt.legend(frameon=False, loc='upper left', bbox_to_anchor=(1.04, 1), ncol=1)
    plt.xlabel("PC 1 (" + str(round(pc.proportion_explained[0] * 100, 2)) + "%)")
    plt.ylabel("PC 2 (" + str(round(pc.proportion_explained[1] * 100, 2)) + "%)")
    plt.savefig(figname, dpi=dpi)
