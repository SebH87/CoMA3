# (c) Sebastian Hupfauf 20020
#
# Script creates alpha diversity plots out of a provided OTU-table file using a
# given metric. Optionally, a tree file can be provided in order to calculate
# Faith's phylogenetic diversity.
#
# USAGE: python alphadiversity.py otu_table metric tree_file(optional)
#        metric: OTU, Shannon, Simpson, Pielou, Goods_coverage, Chao1, Faith_PD
#        tree_file: in NEWICK format (solely used for Faith_PD)

import sys
import matplotlib
import time
from skbio.diversity import alpha_diversity, get_alpha_diversity_metrics
from skbio.stats.ordination import pcoa
from skbio import TreeNode
import pandas as pd
import seaborn as sns
import zenipy as zp
import matplotlib.pyplot as plt

matplotlib.use("Agg")

table = sys.argv[1]
metric = sys.argv[2]
if metric == "OTU":
    metric = "observed_otus"
    label = "OTU"
    mname = "OTU"
if metric == "Shannon":
    metric = "shannon"
    label = "H'"
    mname = "shannon"
if metric == "Simpson":
    metric = "simpson"
    label = "D"
    mname = "simpson"
if metric == "Pielou":
    metric = "pielou_e"
    label = "J'"
    mname = "pielou_evenness"
if metric == "Goods_coverage":
    metric = "goods_coverage"
    label = "Good's coverage"
    mname = "goods_coverage"
if metric == "Chao1":
    metric = "chao1"
    label = "Chao1"
    mname = "chao1"
if metric == "Faith_PD":
    try:
        tree_file = sys.argv[3]
    except:
        zp.error(title="CoMA", text="A tree file is required for the calculation of Faith's phylogenetic diversity!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    metric = "faith_pd"
    label = "Faith's PD"
    mname = "faith_pd"

ftype = zp.entry(title="CoMA", text="Which fileformat do you prefer?\n\neps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff\n")
if ftype == None:
    print("\nProcess terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)
elif ftype not in ["eps", "jpeg", "pdf", "png", "ps", "raw", "rgba", "svg", "svgz", "tiff"]:
    zp.error(title="CoMA", text="Invalid Input, process terminated!")
    print("\nProcess terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)
else:
    figname = "alphadiversity_" + mname + "." + ftype 

if ftype in ["jpeg", "png", "raw", "rgba", "tiff"]:
    dpi = zp.entry(title="CoMA", text="Please enter the resolution [dpi]:")
    if dpi == None:
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    try:
        dpi = int(dpi)
    except:
        zp.error(title="CoMA", text="Invalid Input, process terminated!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
else:
    dpi = 200

col = zp.color_selection(title="CoMA")
col = [float(x) / 255 for x in col[4:-1].split(",")]

start = time.time()
print("\nCreation of alpha diversity plot proceeding ...")

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

if metric == "faith_pd":       
    tree = TreeNode.read(tree_file)
    div = alpha_diversity(metric, df.T, ids=names, otu_ids=otus, tree=tree, validate=False)
else:
    div = alpha_diversity(metric, df.T, names)
div_df = pd.DataFrame(div, columns=[metric])

div_df.to_csv("alphadiversity_" + mname + ".txt", sep="\t")

sns.set_style("ticks", {"ytick.major.size": "2.0"})
ax = sns.barplot(data=div_df.T, color=col)
sns.despine(right=True)
plt.ylabel(label)

plt.savefig(figname, dpi=dpi)

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Your plot is created now!"%dur)
print("\n________________________________________________________________________________\n")
