# (c) Sebastian Hupfauf 20020
#
# Script creates a CoMA mapping file, attaching mapping variables to the samples in an OTU-table file.
#
# USAGE: python mapping.py otu_table_file output_file_name

import zenipy as zp
import sys
import os
import subprocess

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile) as inf:
    inf.readline()
    samples = inf.readline().split("\t")[1:-1]

variables = zp.entry(title="CoMA", text="Please type in the variable names you want to add, seperated with ',' (e.g. season,body_site,year)")

with open(outfile, "w") as outf:
    outf.write("\t" + "\t".join(variables.split(",")) + "\n")
    for sample in samples:
        outf.write(sample + len(variables.split(",")) * "\t" + "\n")

zp.message(title="CoMA", text="Please fill in all missing data in the map file; save then as tab-delimited text file. When you are finished, a quick check will be done to prove your input.\n\nClick now OK to start entering your metadata!", height=100)

os.system("libreoffice --calc %s" %(outfile))

with open(outfile) as outf:
    outf.readline()
    if len(outf.readline().strip().split("\t")) == 1:
        zp.error(title="CoMA", text="ATTENTION: Your map file is not tab-delimited! Please repeat this step and save the text file correctly using 'tab' as separator.")
        print("\nProcess terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(0)
    errors = 0
    for line in outf:
        if len([x for x in line.strip().split("\t") if x != "\t"]) <= len(variables.split(",")):
            zp.error(title="CoMA", text="ATTENTION: This line includes empty cells:\n\n" + line)
            errors += 1

if errors == 0:
    zp.message(title="CoMA", text="Data check succeeded, all your mapping variables were entered correctly!")
else:
    zp.error(title="CoMA", text="Please repeat this step and fill up the entire mapping matrix!")
