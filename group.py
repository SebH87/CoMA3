# (c) Sebastian Hupfauf 20018
#
# Script groups samples/replicates together and sort the newly defined groups
# in alphabetical order.
#
# USAGE: python group.py otu_table_file

import zenipy as pz
import sys
import os
import statistics
import time

method = pz.entry(title="CoMA", text="Please choose the method for grouping:\n\nSum: sum of all reads\nMean: mean of all reads\nMedian: median of all reads\n")
if method == None:
    print("\nGrouping process terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(3)
if method not in ["Sum", "Mean", "Median"]:
    pz.error(title="CoMA", text="Invalid Input, process terminated!")
    print("\nGrouping process terminated!")
    print("\n________________________________________________________________________________\n")
    sys.exit(3)

input_file = "otu_table.txt"
output_file = "otu_table_out.txt"

with open(input_file) as inf:
    inf.readline()
    samples = [str(a.strip()) + "\n" for a in inf.readline().strip().split("\t")[1:-1]]
num = [str(b) + "\t" for b in range(1, len(samples) + 1)]
samples = [c + d for (c, d) in zip(num, samples)]

count = 0
groups = []
labels = []
rem_samples = samples
num = set([z.strip("\t") for z in num])
entry = "_init_"

while rem_samples != []:
    question = 'Please Enter the samplenumbers of group %s,\nseparated with ","(e.g. 1,2,3,4):\n\n'%(count + 1) + "".join(rem_samples)
    entry = pz.entry(title="CoMA", text=question)
    if entry == None:
        print("\nGrouping process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(1)
    if entry == "":
        pz.error(title="CoMA", text="Invalid Input, process terminated!")
        print("\nGrouping process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(2)
    for el in entry.strip().strip(",").strip().split(","):
        if el not in num:
            pz.error(title="CoMA", text="Invalid Input, process terminated!")
            print("\nGrouping process terminated!")
            print("\n________________________________________________________________________________\n")
            sys.exit(2)
    entry = ",".join(sorted(list(set(entry.strip().strip(",").strip().split(",")))))
    groups.append(entry)
    for s_num in entry.split(","):
        samples[int(s_num) - 1] = ""
        num.remove(s_num)
    grp_name = pz.entry(title="CoMA", text="Please enter the name for group %s:"%(count + 1))
    if grp_name == None:
        print("\nGrouping process terminated!")
        print("\n________________________________________________________________________________\n")
        sys.exit(2)
    labels.append(grp_name)
    rem_samples = [k for k in samples if k != ""]
    count += 1

start = time.time()
print("\nGrouping of samples/replicates in progress ...")

with open(input_file) as inf:
    with open(output_file, "w") as outf:
        outf.write(inf.readline())
        header = "#OTU ID\t" + "\t".join(labels) + "\ttaxonomy\n"
        outf.write(header)
        inf.readline()
        for line in inf:
            outf.write(line.strip().split("\t")[0].strip() + "\t")
            reads = [int(float(x)) for x in line.strip().split("\t")[1:-1]]
            for group in groups:
                if method == "Sum":
                    read_sum = 0
                    for j in [int(float(y.strip())) for y in group.split(",")]:
                        read_sum += reads[j - 1]
                    outf.write(str(read_sum) + "\t")
                if method == "Mean":
                    read_list = []
                    for j in [int(float(y.strip())) for y in group.split(",")]:
                        read_list.append(reads[j - 1])
                    mean = int(round(statistics.mean(read_list), 0))
                    outf.write(str(mean) + "\t")
                if method == "Median":
                    read_list = []
                    for j in [int(float(y.strip())) for y in group.split(",")]:
                        read_list.append(reads[j - 1])
                    median = int(round(statistics.median(read_list), 0))
                    outf.write(str(median) + "\t")
            outf.write(line.strip().split("\t")[-1].strip() + "\n")

os.rename(input_file, "otu_table_without_groups.txt")
os.rename(output_file, "otu_table.txt")

end = time.time()
dur = str(int(round(end - start, 0)))

print("\nProcess succeeded! (Duration: %s) Your samples/replicates are grouped now!"%dur)
print("\n________________________________________________________________________________\n")
