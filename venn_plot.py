# (c) Sebastian Hupfauf 2022
#
# Script creates Venn diagrams for comparison of two or three groups. Plots are
# created for each taxonomic level and are showing overlapping and unique taxa.
#
# USAGE: python venn_plot.py input_file map_file(optional)
#        Input file in OTU-table format

import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib_venn import venn2
from matplotlib_venn import venn2_circles
from matplotlib_venn import venn3
from matplotlib_venn import venn3_circles
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import zenipy as pz

matplotlib.use("Agg")

def TaxLvlList(infile, spls):
    tax_list = []
    for i in range(7):
        tax_list.append(set())
    with open(infile) as inf:
        inf.readline()
        inf.readline()
        for line in inf:
            taxa = line.strip().split("\t")[-1].strip().split(";")
            reads = [int(float(j)) for j in line.strip().split("\t")[1:-1]]
            if taxa[0].strip() == "k__?":
                continue
            grp_sum = 0
            for z in spls.split(","):
                grp_sum += reads[int(z) - 1]
            if grp_sum == 0:
                continue
            for j in range(7):
                tax_list[j].add(taxa[j].strip())
    return tax_list

input_file = sys.argv[1]

mapping = pz.question(title="CoMA3", text="Do you want to use the information in the mapping file to group your samples?")
if mapping == True:
    try:
        map_file = sys.argv[2]
    except:
        pz.error(title="CoMA3", text="No mapping file provided, process terminated!")
        print("\nNo mapping file provided, process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    map_DF = pd.read_csv(map_file, delimiter="\t", index_col=0)
    if len(map_DF.columns) > 1:
        var = pz.entry(title="CoMA3", text="Based on which metadata variable do you want to group your samples?\n\nYou can select between the following variables:\n\n" + ", ".join(map_DF.columns) + "\n")
    else:
        var = map_DF.columns[0]
        print("Only 1 metadata variable detected, variable '%s' was selected!"%(var))
    
    if not var in map_DF.columns:
        pz.error(title="CoMA3", text="ATTENTION: Metadata variable '%s' could not be found! No Venn plots are created!"%(var))
        sys.exit(1)
        
    if len(map_DF[var].value_counts()) > 3:
        pz.error(title="CoMA3", text="You can only create Venn plots for the comparison of 2 or 3 groups! You provided %s groups, process terminated!")
        print("\nYou can only create Venn plots for the comparison of 2 or 3 groups! You provided %s groups, process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    elif len(map_DF[var].value_counts()) == 1:
        pz.error(title="CoMA3", text="You can only create Venn plots for the comparison of 2 or 3 groups! You provided only 1 group, process terminated!")
        print("\nYou can only create Venn plots for the comparison of 2 or 3 groups! You provided only 1 group, process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    else:
        dim = len(map_DF[var].value_counts())
        
elif mapping == False:
    dim = pz.entry(title="CoMA3", text="How many groups do you want to compare?\n\npossibilities: 2 or 3\n")
    if dim == None:
            print("\nProcess terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
    elif dim in ["2", "3"]:
        dim = int(dim)
    else:
        pz.error(title="CoMA3", text="Invalid Input, process terminated!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
else:
    pz.error(title="CoMA3", text="Process terminated!")
    print("\nProcess terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)

ftype = pz.entry(title="CoMA3", text="Which fileformat do you prefer?\n\neps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff\n")
if ftype == None:
    print("\nProcess terminated")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)
elif ftype not in ["eps", "jpeg", "pdf", "png", "ps", "raw", "rgba", "svg", "svgz", "tiff"]:
    pz.error(title="CoMA3", text="Invalid Input, process terminated!")
    print("\nProcess terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(1)
else:
    if mapping == True:
        figname = "Venn_" + var + "." + ftype
    else:
        figname = "Venn." + ftype 

if ftype in ["jpeg", "png", "raw", "rgba", "tiff"]:
    dpi = pz.entry(title="CoMA3", text="Please enter the resolution [dpi]:")
    if dpi == None:
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    try:
        dpi = int(dpi)
    except:
        pz.error(title="CoMA3", text="Invalid Input, process terminated!")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
else:
    dpi = 200

interval = np.linspace(0, 0.85, 29)
colors = plt.cm.terrain(interval)
colors = [x[:-1]*255 for x in colors]
color_list = []
for color in colors:
    color = [hex(int(round(x, 0)))[2:] for x in color]
    color_list.append("#" + "".join(color))

with open(input_file) as inf:
    inf.readline()
    samples = [str(a.strip()) + "\n" for a in inf.readline().strip().split("\t")[1:-1]]
num = [str(b) + "\t" for b in range(1, len(samples) + 1)]
samples = [c + d for (c, d) in zip(num, samples)]

if mapping == True:
    map_DF = map_DF.reset_index()
    labels = []
    groups = []
    for k in map_DF[var].unique():
        t = ",".join([str(a + 1) for a in list(map_DF.loc[map_DF[var] == k].index.values)])
        groups.append(t)
        labels.append(k)

if mapping == False:
    count = 0
    groups = []
    labels = []
    num = set([z.strip("\t") for z in num])
    while count < dim:
        rem_samples = [k for k in samples if k != ""]
        question = 'Please Enter the samplenumbers of group %s,\nseparated with ","(e.g. 1,2,3,4):\n\n'%(count + 1) + "".join(rem_samples)
        entry = pz.entry(title="CoMA3", text=question)
        if entry == None:
            print("\nGrouping process terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
        if entry == []:
            print("\nGrouping process terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
        for el in entry.strip().strip(",").strip().split(","):
            if el not in num:
                pz.error(title="CoMA3", text="Invalid Input, process terminated!")
                print("\nGrouping process terminated!")
                print("\n________________________________________________________________________________\n")
                sys.exit(2)
        entry = ",".join(sorted(list(set(entry.strip().strip(",").strip().split(",")))))
        groups.append(entry)
        for s_num in entry.split(","):
            samples[int(s_num) - 1] = ""
            num.remove(s_num)
        grp_name = pz.entry(title="CoMA3", text="Please enter the name for group %s:"%(count + 1))
        if grp_name == None:
            print("\nGrouping process terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
        if grp_name == []:
            print("\nGrouping process terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(1)
        labels.append(grp_name)
        count += 1

lab = pz.question(title="CoMA3", text="Do you want to label all areas with the exact number of taxa? In some cases, this might lead to overlapping issues.")

start = time.time()
print("\nCreation of Venn plots proceeding ...")

data_list = []
for group in groups:
    data_list.append(TaxLvlList(input_file, group))

plt.figure(figsize=(18, 8))
gs1 = gridspec.GridSpec(2, 4)
gs1.update(wspace=0.001, hspace=0.1)

sub = [0, 1, 2, 4, 5, 6, 7]
tax_lvl = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
colors = [sns.color_palette("deep")[2]] + [sns.color_palette("deep")[0]] + [sns.color_palette("deep")[1]]
colors *= 3

if dim == 2:
    for x in range(len(sub)):
        plt.subplot(gs1[sub[x]])
        plt.title(tax_lvl[x], fontdict=dict(weight='bold'))
        ax1 = venn2([data_list[0][x], data_list[1][x]], set_labels = ("", ""))
        if lab == False:
            for idx, subset in enumerate(ax1.subset_labels):
                ax1.subset_labels[idx].set_visible(False)
        venn2_circles([data_list[0][x], data_list[1][x]], linestyle = "dashed",
                      linewidth = 0.8, color = "grey")
        ax1.get_patch_by_id('10').set_color(color_list[2])
        ax1.get_patch_by_id('10').set_alpha(0.7)
        ax1.get_patch_by_id('01').set_color(color_list[18])
        ax1.get_patch_by_id('01').set_alpha(0.7)
        ax1.get_patch_by_id('11').set_color(color_list[9])
        ax1.get_patch_by_id('11').set_alpha(0.7)
    plt.subplot(gs1[3])
    plt.axis("off")
    c1 = mpatches.Patch(facecolor=color_list[2], label=labels[0], edgecolor="grey", linestyle = "dashed", linewidth = 0.8, alpha=0.7)
    c2 = mpatches.Patch(facecolor=color_list[18], label=labels[1], edgecolor="grey", linestyle = "dashed", linewidth = 0.8, alpha=0.7)
    if mapping == False:
        legend1 = plt.legend(handles=[c1, c2], edgecolor="w", bbox_to_anchor=(0.75, 0.75), prop={"size": 15})
    else:
        legend1 = plt.legend(title=var, handles=[c1, c2], edgecolor="w", bbox_to_anchor=(0.75, 0.75), prop={"size": 15})
        plt.setp(legend1.get_title(), fontsize=17)
    plt.savefig(figname, dpi=dpi, bbox_inches='tight')

if dim == 3:
    for x in range(len(sub)):
        plt.subplot(gs1[sub[x]])
        plt.title(tax_lvl[x], fontdict=dict(weight='bold'))
        ax1 = venn3([data_list[0][x], data_list[1][x], data_list[2][x]], set_labels = ("", "", ""))
        if lab == False:
            for idx, subset in enumerate(ax1.subset_labels):
                try:
                    ax1.subset_labels[idx].set_visible(False)
                except:
                    continue
        venn3_circles([data_list[0][x], data_list[1][x], data_list[2][x]], linestyle = "dashed",
                      linewidth = 0.8, color = "grey")
        if ax1.get_patch_by_id('100') is not None:
            ax1.get_patch_by_id('100').set_color(color_list[2])
            ax1.get_patch_by_id('100').set_alpha(0.7)
        if ax1.get_patch_by_id('010') is not None:
            ax1.get_patch_by_id('010').set_color(color_list[18])
            ax1.get_patch_by_id('010').set_alpha(0.7)
        if ax1.get_patch_by_id('001') is not None:
            ax1.get_patch_by_id('001').set_color(color_list[9])
            ax1.get_patch_by_id('001').set_alpha(0.7)
        if ax1.get_patch_by_id('110') is not None:
            ax1.get_patch_by_id('110').set_color("#849FA7")
            ax1.get_patch_by_id('110').set_alpha(0.7)
        if ax1.get_patch_by_id('101') is not None:
            ax1.get_patch_by_id('101').set_color("#1A9696")
            ax1.get_patch_by_id('101').set_alpha(0.7)
        if ax1.get_patch_by_id('011') is not None:
            ax1.get_patch_by_id('011').set_color("#7FD97C")
            ax1.get_patch_by_id('011').set_alpha(0.7)
        if ax1.get_patch_by_id('111') is not None:
            ax1.get_patch_by_id('111').set_color(color_list[-1])
            ax1.get_patch_by_id('111').set_alpha(0.7)
    plt.subplot(gs1[3])
    plt.axis("off")
    c1 = mpatches.Patch(facecolor=color_list[2], alpha=0.7, label=labels[0], edgecolor="grey", linestyle = "dashed", linewidth = 0.8)
    c2 = mpatches.Patch(facecolor=color_list[18], alpha=0.7, label=labels[1], edgecolor="grey", linestyle = "dashed", linewidth = 0.8)
    c3 = mpatches.Patch(facecolor=color_list[9], alpha=0.7, label=labels[2], edgecolor="grey", linestyle = "dashed", linewidth = 0.8)
    if mapping == False:
        legend1 = plt.legend(handles=[c1, c2, c3], edgecolor="w", bbox_to_anchor=(0.75, 0.75), prop={"size": 15})
    else:
        legend1 = plt.legend(title=var, handles=[c1, c2, c3], edgecolor="w", bbox_to_anchor=(0.75, 0.75), prop={"size": 15})
        plt.setp(legend1.get_title(), fontsize=17)
    plt.savefig(figname, dpi=dpi, bbox_inches='tight')

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Your plots are created now!"%dur)
print("\n________________________________________________________________________________\n")

