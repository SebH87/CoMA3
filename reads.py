# (c) Sebastian Hupfauf 2022
#
# Script counts the reads for each sample in an OTU-table file und prints the 
# result in decreasing order.
#
# USAGE: python reads.py otu_table_file

import sys

infile = sys.argv[1]

with open(infile) as inf:
    inf.readline()
    samples = inf.readline().strip().split("\t")[1:-1]
    samples = [[x, 0] for x in samples]
    for line in inf:
        for i in range(len(samples)):
           samples[i][1] += int(float(line.strip().split("\t")[i + 1]))
    samples.sort(key=lambda x: x[1], reverse=True)

print("")
print("SAMPLES - sorted by number of reads:")
print("_" * 36)
for sample in samples:
    print(sample[0] + ": " + str(sample[1]))
print("")
    

