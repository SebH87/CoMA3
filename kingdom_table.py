# (c) Sebastian Hupfauf 20017
#
# Script creates an OTU-table file containing only OTUs corresponding to a given kingdom
# out of a given OTU-table file.
#
# USAGE: python kingdom_table.py input_file output_file kingdom
#        files must be in otu-table format
#        kingdom must be: Archaea, Bacteria, Fungi, Eukaryota, or Total

import sys

infile = sys.argv[1]
outfile = sys.argv[2]
kingdom = "k__" + sys.argv[3]

with open(infile) as inf:
    with open(outfile, "w") as outf:
        outf.write(inf.readline())
        outf.write(inf.readline())
        counter = 0
        if kingdom == "k__Total":
            for line in inf:
                outf.write(line)
                counter += 1
        else:
            for line in inf:
                if kingdom in line:
                    outf.write(line)
                    counter += 1
                else:
                    continue
                    
if counter == 0:
    print("\nATTENTION: No sequences were found for '%s'!"%(sys.argv[3]))
