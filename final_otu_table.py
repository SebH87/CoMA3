# (c) Sebastian Hupfauf 20017
#
# Script converts a given OTU-table file (e.g. .txt or .csv) for better
# readability and further calculations by splitting up the taxonomy column.
#
# USAGE: python final_otu_table.py input_file output_file

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

taxa = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
tax_abr = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
   
with open(outfile, "w") as of:
    with open(infile) as inf:
        l = inf.readline()
        of.write(l)
        l = inf.readline()
        of.write(l.strip()[:-8].strip())
        for tax in taxa:
            of.write("\t" + tax)
        of.write("\n")
        for line in inf:
            of.write(line.split("\t")[0])
            for i in range(1, len(line.split("\t")) - 1):
                of.write("\t" + line.split("\t")[i])
            for i in range(7):
                of.write("\t" + line.split("\t")[-1].strip().split(";")[i].strip().strip(tax_abr[i]))
            of.write("\n")


