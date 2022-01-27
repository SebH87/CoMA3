# (c) Sebastian Hupfauf 2022
#
# Script chamges samples names within a given OTU-table file and sorts samples
# in alphabetical order.
#
# USAGE: python rename.py otu_table_file

import pandas as pd
import os
import sys

infile = sys.argv[1]
outfile = "new_otu_table.txt"
outfile2 = "sorted_otu_table.txt"
new_names = []

with open(infile) as inf:
    inf.readline()
    samples = inf.readline().strip().split("\t")[1:-1]
    print("Please enter the new name for each sample:\n\nATTENTION: Keep in mind that sample names must not include any special character\nthan underscore ('_')! Furthermore, it is not possible to have a number on the\nfirst position!\n")
    for sample in samples:
        print(sample + ": ")
        new_names.append(input())

with open(infile) as inf:
    with open(outfile, "w") as outf:
        outf.write(inf.readline())
        inf.readline()
        outf.write("#OTU ID\t" + "\t".join(new_names) + "\ttaxonomy\n")
        for line in inf:
            outf.write(line)
        
df = pd.read_csv(outfile, sep="\t", header=1)
cols = df.columns.tolist()[1:-1]
cols.sort()
cols = ["#OTU ID"] + cols
cols.append("taxonomy")
df = df[cols]

with open(outfile2, "w") as outf:
    outf.write("# Constructed from biom file\n")
    df.to_csv(outf, sep="\t", index=False)

os.remove(infile)
os.rename(outfile2, infile)
os.remove(outfile)
