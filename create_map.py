# (c) Sebastian Hupfauf 20017
#
# Script creates a map file for NGS analysis using the tool "lOTUs" out of a
# given name file.
#
# USAGE: python filelist.py name_file output_name

import sys

infile = sys.argv[1]
outfile = sys.argv[2]
names = ["#SampleID"]
fastq = ["fastqFile"]

with open(infile) as inf:
    for name in inf:
        names.append(name.strip())
        fastq.append(name.strip() + ".fastq")

with open(outfile, "w") as of:
    x = 0
    for pos in range(len(names)):
        if x == 0:
            of.write(names[pos] + "\t" + "BarcodeSequence" + "\t" +
                     "LinkerPrimerSequence" + "\t" + fastq[pos] + "\t" + "SequencingRun" + "\n")
            x += 1
        else:
            of.write(names[pos] + "\t" + "\t" + "\t" + fastq[pos] + "\tA" + "\n")
