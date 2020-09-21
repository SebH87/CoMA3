# (c) Sebastian Hupfauf 20017
#
# Script creates OTU-table files containing only OTUs corresponding to Archaea
# and Bacteria, respectively out of a given OTU-table file.
#
# USAGE: python archaea.py input_file archaea_file bacteria_file
#        files must be in OTU-table format

import sys

infile = sys.argv[1]
archaea = sys.argv[2]
bacteria = sys.argv[3]

with open(infile) as inf:
    with open(archaea, "w") as af:
        with open(bacteria, "w") as bf:
            first = inf.readline()
            sec = inf.readline()
            af.write(first)
            af.write(sec)
            bf.write(first)
            bf.write(sec)
            for line in inf:
                if "k__Archaea" in line:
                    af.write(line)
                if "k__Bacteria" in line:
                    bf.write(line)
                if "k__?" in line:
                    continue
                
