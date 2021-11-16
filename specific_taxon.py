# (c) Sebastian Hupfauf 20017
#
# Script creates an OTU-table file containing only OTUs corresponding to the given taxon
# out of a given OTU-table file.
#
# USAGE: python specific_taxon.py input_file taxon
#        files must be in otu-table format

import sys

infile = sys.argv[1]
taxon = sys.argv[2]
outputfile = taxon + ".txt"
counter = 0

with open(infile) as inf:
    with open(outputfile, "w") as outf:
        outf.write(inf.readline())
        outf.write(inf.readline())
        for line in inf:
            if taxon in line:
                outf.write(line)
                counter += 1
            else:
                continue
