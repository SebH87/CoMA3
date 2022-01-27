# (c) Sebastian Hupfauf 2022
#
# Script creates a shared file for creating rarefaction curves using the
# "Mothur" software out of a given OTU-table file.
#
# USAGE: python create_shared_file.py otu_table_file output_name

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

samples = ["Group"]
otus = []
otus_cor = []
label = ["label"]
num_otus = ["numOtus"]

with open(infile) as inf:
    inf.readline()
    samples += inf.readline().strip().split("\t")[1:-1]
    for line in inf:
        otus.append(line.strip().split("\t")[:-1])

for i in range(len(otus)):
        otus_cor.append([otus[i][0]])
        otus_cor[i] += [int(float(x)) for x in otus[i][1:]]

for i in range(len(samples) - 1):
    label.append(0.03)
    num_otus.append(len(otus))

with open(outfile, "w") as of:
    for i in range(len(label)):
        of.write(str(label[i]) + "\t" + samples[i] + "\t" + str(num_otus[i]))
        for j in range(len(otus)):
            of.write("\t" + str(otus_cor[j][i]))
        of.write("\n")
    


