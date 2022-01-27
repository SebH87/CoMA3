# (c) Sebastian Hupfauf 2022
#
# Script for creating a report file of the sequence processing steps in CoMA3.
#
# USAGE: python report.py

import pandas as pd
import os
import glob

name_file = "/".join(os.getcwd().split("/")[:-1]) + "/Data/name.txt"

names = []
with open(name_file) as nf:
    for line in nf:
        names.append(line.strip())

start = []
for name in names:
    with open("/".join(os.getcwd().split("/")[:-1]) + "/Data/processed_reads/" + name + ".fastq") as inf:
        n = 0
        for line in inf:
            n += 1
        start.append(int(n / 4))

before_sdm = []
after_sdm = []
for file in glob.glob(os.getcwd() + "/LotuSLogS/SDMperFile/*"):
    with open(file) as f:
        for line in f:
            if line.startswith("Reads processed:"):
                before_sdm.append(int(line.strip().split(" ")[-1].replace(",", "")))
            if line.startswith("Accepted (High qual):"):
                after_sdm.append(int(line.strip().split(" ")[3].replace(",", "")))

chimeras = []
chim_DF = pd.read_csv(os.getcwd() + "/ExtraFiles/otu_mat.chim.txt", delimiter="\t", index_col=0)
for name in names:
    chimeras.append(chim_DF[name].sum())

end = []
for n in range(len(chimeras)):
    end.append(after_sdm[n] - chimeras[n])

qf = []
for n in range(len(start)):
    qf.append(start[n] - before_sdm[n])

sdm = []
for n in range(len(before_sdm)):
    sdm.append(before_sdm[n] - after_sdm[n])

data = []
data.append(start)
data.append(qf)
data.append(sdm)
data.append(chimeras)
data.append(end)

DF = pd.DataFrame(data, index=["Original reads", "Rejected during quality filtering", "Rejected during SDM", "Chimeric sequences / phiX contaminants", "Remaining reads"], columns=names)

DF.to_csv("rem_seq.txt", sep="\t")
