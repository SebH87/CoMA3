# (c) Sebastian Hupfauf 20020
#
# Script groups samples in an OTU-table file based on the information from a mapping file.
#
# USAGE: python map_group.py otu_table_file mapping_file output_file_name

import sys
import os
import pandas as pd
import zenipy as zp

otu_table = sys.argv[1]
map_file = sys.argv[2]
outfile = sys.argv[3]

otu_DF = pd.read_csv(otu_table, delimiter="\t", header=1, index_col=0)
samples = list(otu_DF.columns)[0:-1]

map_DF = pd.read_csv(map_file, delimiter="\t", index_col=0)

var = zp.entry(title="CoMA", text="Based on which metadata variable do you want to group your samples?\n\nYou can select between the following variables:\n\n" + ", ".join(map_DF.columns) + "\n")

DF = pd.concat([otu_DF.T, map_DF], axis=1)
DF = DF.reset_index().groupby(var)
pairs = DF.index.value_counts().index.tolist()

unique = list(set([a for (a, b) in pairs]))
unique_dic = {}
for item in unique:
    unique_dic[item] = [b for (a, b) in pairs if item in (a, b)]

#Creation of new dataframe
new_DF = pd.DataFrame()

for key in unique_dic.keys():
    new_DF[key] = otu_DF[unique_dic[key]].mean(axis=1).round(0).astype(int)

new_DF[list(otu_DF.columns)[-1]] = otu_DF[list(otu_DF.columns)[-1]]

new_DF.to_csv("temp.txt", sep="\t")

with open("temp.txt") as t:
    with open(outfile, "w") as outf:
        outf.write("# Constructed from biom file\n")
        outf.write(t.read())

os.remove("temp.txt")
