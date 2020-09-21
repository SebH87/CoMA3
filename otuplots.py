# (c) Sebastian Hupfauf 20017
#
# Script creates a heatmap as well as a bar chart of taxa for each taxonomic
# level out of a given OTU-table file. Taxa with an abundance below the threshold
# are not considered (threshold in percent of total reads of each sample).
#
# USAGE: python otuplots.py input_file threshold fileformat dpi unassigned
#        Input file in OTU-table format
#        Threshold must be in range [0, 100]
#        fileformat: eps, jpeg, pdf, png, ps, raw, rgba, svg, svgz, tiff
#        dpi: figure resolution [int]
#        unassigned: Yes or No

from collections import defaultdict
from matplotlib.font_manager import FontProperties
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
import sys

matplotlib.use("Agg")

infile = sys.argv[1]
threshold = float(sys.argv[2]) / 100
ext = "." + sys.argv[3].lower()
dpi = int(sys.argv[4])
unassigned = sys.argv[5]
kingdom = []
phylum = []
classes = []
order = []
family = []
genus = []
species = []

with open(infile) as inf:
        inf.readline()
        samples = inf.readline().strip().split("\t")[1:-1]
        if inf.readline() == "":
            print("\n'" + infile + "' is empty! No plots are created for this taxon!")
            sys.exit()

for sample in range(len(samples)):
    sk = defaultdict(list)
    sp = defaultdict(list)
    sc = defaultdict(list)
    so = defaultdict(list)
    sf = defaultdict(list)
    sg = defaultdict(list)
    ss = defaultdict(list)
    
    with open(infile) as inf:
        inf.readline()
        inf.readline()
        for line in inf:
            sk[line.strip().split("\t")[-1].split(";")[0].strip().strip("k__")].append(int(float(line.strip().split("\t")[sample + 1])))
            sp[line.strip().split("\t")[-1].split(";")[1].strip().strip("p__")].append(int(float(line.strip().split("\t")[sample + 1])))
            sc[line.strip().split("\t")[-1].split(";")[2].strip().strip("c__")].append(int(float(line.strip().split("\t")[sample + 1])))
            so[line.strip().split("\t")[-1].split(";")[3].strip().strip("o__")].append(int(float(line.strip().split("\t")[sample + 1])))
            sf[line.strip().split("\t")[-1].split(";")[4].strip().strip("f__")].append(int(float(line.strip().split("\t")[sample + 1])))
            sg[line.strip().split("\t")[-1].split(";")[5].strip().strip("g__")].append(int(float(line.strip().split("\t")[sample + 1])))
            ss[line.strip().split("\t")[-1].split(";")[6].strip().strip("s__")].append(int(float(line.strip().split("\t")[sample + 1])))

    for key in list(sk.keys()):
        sk[key] = sum(sk[key])
    for key in list(sp.keys()):
        sp[key] = sum(sp[key])
    for key in list(sc.keys()):
        sc[key] = sum(sc[key])
    for key in list(so.keys()):
        so[key] = sum(so[key])
    for key in list(sf.keys()):
        sf[key] = sum(sf[key])
    for key in list(sg.keys()):
        sg[key] = sum(sg[key])
    for key in list(ss.keys()):
        ss[key] = sum(ss[key])

    if unassigned == "No":
        try:
            del(sk["?"])
        except:
            sk = sk  
        try:
            del(sp["?"])
        except:
            sp = sp
        try:
            del(so["?"])
        except:
            so = so
        try:
            del(sc["?"])
        except:
            sc = sc
        try:
            del(sf["?"])
        except:
            sf = sf
        try:
            del(sg["?"])
        except:
            sg = sg
        try:
            del(ss["?"])
        except:
            ss = ss

        try:
            del(sk["Unknown Kingdom"])
        except:
            sk = sk  
        try:
            del(sp["Unknown Phylum"])
        except:
            sp = sp
        try:
            del(so["Unknown Order"])
        except:
            so = so
        try:
            del(sc["Unknown Class"])
        except:
            sc = sc
        try:
            del(sf["Unknown Family"])
        except:
            sf = sf
        try:
            del(sg["Unknown Genus"])
        except:
            sg = sg
        try:
            del(ss["Unknown Species"])
        except:
            ss = ss

        try:
            del(sk["unclassified"])
        except:
            sk = sk  
        try:
            del(sp["unclassified"])
        except:
            sp = sp
        try:
            del(so["unclassified"])
        except:
            so = so
        try:
            del(sc["unclassified"])
        except:
            sc = sc
        try:
            del(sf["unclassified"])
        except:
            sf = sf
        try:
            del(sg["unclassified"])
        except:
            sg = sg
        try:
            del(ss["unclassified"])
        except:
            ss = ss
        
    kingdom.append(sk)
    phylum.append(sp)
    classes.append(sc)
    order.append(so)
    family.append(sf)
    genus.append(sg)
    species.append(ss)

dfk = pd.DataFrame(kingdom, index=samples)
dfk = dfk.reindex(columns=sorted(list(dfk)))
dfp = pd.DataFrame(phylum, index=samples)
dfp = dfp.reindex(columns=sorted(list(dfp)))
dfc = pd.DataFrame(classes, index=samples)
dfc = dfc.reindex(columns=sorted(list(dfc)))
dfo = pd.DataFrame(order, index=samples)
dfo = dfo.reindex(columns=sorted(list(dfo)))
dff = pd.DataFrame(family, index=samples)
dff = dff.reindex(columns=sorted(list(dff)))
dfg = pd.DataFrame(genus, index=samples)
dfg = dfg.reindex(columns=sorted(list(dfg)))
dfs = pd.DataFrame(species, index=samples)
dfs = dfs.reindex(columns=sorted(list(dfs)))

if len(samples) < 10:
    scale = 0.5
if len(samples) >= 10 and len(samples) < 30:
    scale = 1
if len(samples) >= 30 and len(samples) < 50:
    scale = 1.5
if len(samples) >= 50:
    scale = 2

interval = np.linspace(0, 0.85, 200)
colors = plt.cm.terrain(interval)
cmap = LinearSegmentedColormap.from_list('name', colors)

#KINGDOM

dfk = dfk.transpose()
dfk[dfk<dfk.sum()*threshold] = 0
dfk = dfk.transpose()
dfk = dfk.loc[:, (dfk != 0).any(axis=0)]
dfk = dfk.div(dfk.sum(1), axis=0)

if not dfk.empty:
    sns.set_style("white")
    fig = dfk.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.7, figsize=(12 * scale, 9), width=(1 - scale * 0.2))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("kingdom_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#PHYLUM

dfp = dfp.transpose()
dfp[dfp<dfp.sum()*threshold] = 0
dfp = dfp.transpose()
dfp = dfp.loc[:, (dfp != 0).any(axis=0)]
dfp = dfp.div(dfp.sum(1), axis=0)

if not dfp.empty:
    sns.set_style("white")
    fig = dfp.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, figsize=(12 * scale, 9), width=(1 - scale * 0.2))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("phylum_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#CLASS

dfc = dfc.transpose()
dfc[dfc<dfc.sum()*threshold] = 0
dfc = dfc.transpose()
dfc = dfc.loc[:, (dfc != 0).any(axis=0)]
dfc = dfc.div(dfc.sum(1), axis=0)

if not dfc.empty:
    sns.set_style("white")
    fig = dfc.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, figsize=(12 * scale, 9), width=(1 - scale * 0.2))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("class_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#ORDER

dfo = dfo.transpose()
dfo[dfo<dfo.sum()*threshold] = 0
dfo = dfo.transpose()
dfo = dfo.loc[:, (dfo != 0).any(axis=0)]
dfo = dfo.div(dfo.sum(1), axis=0)

if not dfo.empty:
    sns.set_style("white")
    fig = dfo.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, width=(1 - scale * 0.2), figsize=(12 * scale, 9))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("order_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#FAMILY

dff = dff.transpose()
dff[dff<dff.sum()*threshold] = 0
dff = dff.transpose()
dff = dff.loc[:, (dff != 0).any(axis=0)]
dff = dff.div(dff.sum(1), axis=0)

if not dff.empty:
    sns.set_style("white")
    fig = dff.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, figsize=(12 * scale, 9), width=(1 - scale * 0.2))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), frameon=False, fontsize=10, borderaxespad=0.)
    plt.savefig("family_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#GENUS

dfg = dfg.transpose()
dfg[dfg<dfg.sum()*threshold] = 0
dfg = dfg.transpose()
dfg = dfg.loc[:, (dfg != 0).any(axis=0)]
dfg = dfg.div(dfg.sum(1), axis=0)

if not dfg.empty:
    sns.set_style("white")
    fig = dfg.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, figsize=(12 * scale, 9), width=(1 - scale * 0.2))
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("genus_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

#SPECIES

if not dfs.empty:
    dfs = dfs.transpose()
    dfs[dfs<dfs.sum()*threshold] = 0
    dfs = dfs.transpose()
    dfs = dfs.loc[:, (dfs != 0).any(axis=0)]
    dfs = dfs.div(dfs.sum(1), axis=0)

if not dfs.empty:
    sns.set_style("white")
    fig = dfs.plot(kind="bar", stacked=True, colormap=cmap, alpha=0.8, figsize=(12 * scale, 9), width=(1 - scale * 0.2)) #sns.cubehelix_palette(20, start=.1, rot=-5, as_cmap=True)
    plt.ylabel("Frequency")
    plt.ylim(0, 1)
    #plt.tight_layout()
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    handles, labels = fig.get_legend_handles_labels()
    lgd = plt.legend(handles[::-1], labels[::-1], loc=2, bbox_to_anchor=(1.05, 1), fontsize=10, frameon=False, borderaxespad=0.)
    plt.savefig("species_bar" + ext, dpi=dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.clf()

dfk = dfk.transpose()
dfp = dfp.transpose()
dfc = dfc.transpose()
dfo = dfo.transpose()
dff = dff.transpose()
dfg = dfg.transpose()
dfs = dfs.transpose()

if not dfk.empty:
    fs = -0.07 * dfk.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfk, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    ax.set_yticklabels(reversed(list(dfk.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("kingdom_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dfp.empty:
    fs = -0.07 * dfp.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfp, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    ax.set_yticklabels(reversed(list(dfp.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("phylum_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dfc.empty:
    fs = -0.07 * dfc.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfc, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    ax.set_yticklabels(reversed(list(dfc.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("class_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dfo.empty:
    fs = -0.07 * dfo.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfo, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    plt.axes()
    ax.set_yticklabels(reversed(list(dfo.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("order_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dff.empty:
    fs = -0.07 * dff.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dff, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90) #ha="right"
    ax.set_yticklabels(reversed(list(dff.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("family_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dfg.empty:
    fs = -0.07 * dfg.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfg, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    ax.set_yticklabels(reversed(list(dfg.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("genus_heatmap" + ext, dpi=dpi, bbox_inches='tight')
    plt.clf()

if not dfs.empty:
    fs = -0.07 * dfs.shape[0] + 12.7
    if fs > 12:
        fs = 12
    ax = sns.heatmap(dfs, annot=False, fmt="f", cmap=sns.cubehelix_palette(8, start=.1, rot=-.75, as_cmap=True), linewidths=.2 / scale, xticklabels=samples, yticklabels=True)
    plt.xticks(rotation=90)
    ax.set_yticklabels(reversed(list(dfs.index[::-1])), rotation=0, fontsize=fs)
    plt.savefig("species_heatmap" + ext, dpi=dpi, bbox_inches='tight')


