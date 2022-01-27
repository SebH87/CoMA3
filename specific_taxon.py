# (c) Sebastian Hupfauf 2022
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

with open(infile) as inf:
    with open(outputfile, "w") as outf:
        outf.write(inf.readline())
        outf.write(inf.readline())
        for line in inf:
            if "__" + taxon + ";" in line:
                outf.write(line)
            else:
                continue
