# (c) Sebastian Hupfauf 20017
#
# Script writes all files contained in the current directory and matching a given
# pattern to an output file (of given name).
#
# USAGE: python filelist.py pattern output_name threads

import sys
import glob
import os

pattern = sys.argv[1]
outfile = sys.argv[2]
cpu = int(sys.argv[3])

filenames = []
for i in range(1, cpu + 1):
    filenames.append("n" + str(i) + ".txt")

filelist = glob.glob("*" + pattern)
filelist.sort()

print("_" * 36)
print("Samples:")
for files in filelist:
        print(files[:-len(pattern)])
print("_" * 36)

with open(outfile, "w") as of:
    for files in filelist:
        of.write(files[:-len(pattern)] + "\n")

eq = int(len(filelist)/cpu)
split_fl = []
if len(filelist) >= cpu:  
    for i in range(cpu):
        split_fl.append(filelist[i * eq : (i+1) * eq])
    rest = filelist[cpu * eq :]
else:
    rest = filelist

for thread in range(cpu):
    with open(filenames[thread], "w") as tf:
        if split_fl == []:
            if rest != []:           
                tf.write(rest[-1][:-len(pattern)] + "\n")
                rest.pop()
        else:
            for x in split_fl[thread]:
                tf.write(x[:-len(pattern)] + "\n")
            if rest != []:           
                tf.write(rest[-1][:-len(pattern)] + "\n")
                rest.pop()

with open("threads.txt", "w") as of:
    for k in filenames[:cpu]:
        of.write(k + "\n")
