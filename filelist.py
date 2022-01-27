# (c) Sebastian Hupfauf 2022
#
# Script writes all files contained in the current directory and matching a given
# pattern to an output file (of given name).
#
# USAGE: python filelist.py pattern output_name threads

import sys
import glob
import os
import time
import signal

start = time.time()

pattern = sys.argv[1]
outfile = sys.argv[2]
cpu = int(sys.argv[3])
try:
    revpattern = sys.argv[4]
    if pattern == revpattern:
        print("ATTENTION: You have entered the same pattern for your forward and reverse files - CoMA3 run terminated!\n")
        os.kill(os.getppid(),signal.SIGTERM)
except:
    revpattern = pattern

filenames = []
for i in range(1, cpu + 1):
    filenames.append("n" + str(i) + ".txt")

filelist = glob.glob("*" + pattern)
filelist.sort()

revlist = glob.glob("*" + revpattern)
revlist.sort()

if [x[:-len(pattern)] for x in filelist] == [y[:-len(revpattern)] for y in revlist] and len(filelist) != 0:

    print("_" * 45)
    print("The following " + str(len(filelist)) + " samples have been registered:")
    for files in filelist:
            print(files[:-len(pattern)])
    print("_" * 45)

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

    end = time.time()
    duration = end - start

    print("\nUsed CPUs: " + str(cpu))
    if pattern != revpattern:
        print("\nCommon part of forward sequences: " + pattern)
        print("Common part of reverse sequences: " + revpattern)
    else:
        print("\nCommon part of all sequences: " + pattern)
    print("\nDONE! Samples are registered. (Duration: " + str(int(round(duration, 0))) + " s)")
    print("\n________________________________________________________________________________\n")

else:
    print("There was an error during sample registration, please check your input and rerun this step! In case of paired-end data, please also check if all paired-end files are available in the Data directory of the project!\n\nUser input:")
    if pattern != revpattern:
        print("\nCommon part of forward sequences: " + pattern)
        print("Common part of reverse sequences: " + revpattern)
    else:
        print("\nCommon part of all sequences: " + pattern)
    os.kill(os.getppid(),signal.SIGTERM)
