# (c) Sebastian Hupfauf 20020
#
# Script creates alpha diversity plots out of a provided OTU-table file using a
# given metric. Optionally, a tree file can be provided in order to calculate
# Faith's phylogenetic diversity.
#
# USAGE: python alphadiversity.py otu_table metric map_file tree_file(optional)
#        metric: OTU, Shannon, Simpson, Pielou, Goods_coverage, Chao1, Faith_PD
#        map_file: in the format used by CoMA
#        tree_file: in NEWICK format (solely used for Faith_PD)

import sys
import matplotlib
import time
from skbio.diversity import alpha_diversity, get_alpha_diversity_metrics
from skbio import TreeNode
import scipy.stats as ss
import scikit_posthocs as sp
import pandas as pd
import seaborn as sns
import zenipy as zp
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use("Agg")

table = sys.argv[1]
metric = sys.argv[2]
try:
    map_file = sys.argv[3]
except:
    zp.error(title="CoMA", text="You are missing a map file, process terminated!")
    print("\nYou are missing a map file, process terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)
map_df = pd.read_csv(map_file, delimiter="\t", index_col=0)
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
        tree_file = sys.argv[4]
    except:
        zp.error(title="CoMA", text="A tree file is required for the calculation of Faith's phylogenetic diversity!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    metric = "faith_pd"
    label = "Faith's PD"
    mname = "faith_pd"

if len(map_df.columns) > 1:
    var = zp.entry(title="CoMA", text="Based on which metadata variable do you want to group your samples?\n\nYou can select between the following variables:\n\n" + ", ".join(map_df.columns) + "\n")
else:
    var = map_df.columns[0]
    print("Only 1 metadata variable detected, variable '%s' was selected!"%(var))

if not var in map_df.columns:
    zp.error(title="CoMA", text="ATTENTION: Metadata variable '%s' could not be found! Alpha diversity cannot be calculated and no plot is created!"%(var))
    sys.exit(1)

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
    figname = "alphadiversity_" + mname + "_" + var + "." + ftype 

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

div_df.reset_index(drop=True, inplace=True)
map_df.reset_index(drop=True, inplace=True)

combined_df = pd.concat([div_df, map_df], axis=1)
combined_df.rename(columns={'index':'sample'}, inplace=True)
combined_df = combined_df.sort_values(by=[var])

output_df = pd.concat([combined_df.groupby(var).mean(), combined_df.groupby(var).std()], axis=1)
output_df.columns = ["Mean", "Std"]
output_df = output_df.replace(np.nan, '', regex=True)
output_df.to_csv("alphadiversity_" + mname + "_" + var + ".txt", sep="\t")

#Kruskal-Wallis test
cat_dict = {}
for upar in getattr(combined_df, var).unique():
    cat_dict[str(upar)] = list(combined_df[combined_df[var] == upar][metric])
H, p = ss.kruskal(*cat_dict.values())

#Post-hoc test with Benjamini-Hochberg correction
con = sp.posthoc_conover(combined_df, val_col=metric, group_col=var, p_adjust = 'fdr_bh')
with open("statistics_" + mname + "_" + var + ".txt", "w") as st:
    st.write("Kruskal-Wallis H-test:\n\n")
    st.write("H\t" + str(H) + "\n")
    st.write("p-value\t" + str(p) + "\n\n\n")
    st.write("Conover post-hoc test with Benjamini/Hochberg correction:\n\n")
    st.write(con.to_string())

sns.set_style("ticks", {"ytick.major.size": "2.0"})
ax = sns.barplot(data=combined_df, x=var, y=metric, color=col, ci="sd", errwidth=0.6, capsize=0.1)
sns.despine(right=True)
plt.ylabel(label)
plt.xticks(rotation=90)

plt.savefig(figname, dpi=dpi)

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Your plot is created now!"%dur)
print("\n________________________________________________________________________________\n")
