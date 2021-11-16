# (c) Sebastian Hupfauf 20017
#
# Script creates a summary file containing the x (entries) most recurrent results 
# in each taxonomic level for each sample out of a given OTU-table file.
#
# USAGE: otu_summary.py input_file output_file entries


from collections import defaultdict
import sys

infile = sys.argv[1]
outfile = sys.argv[2]
try:
    entries = int(sys.argv[3])
except:
    print("\n'" + sys.argv[3] + "' is an invalid input! Must be a number! No summary files are created!")
    sys.exit()
if entries < 1:
    print("\n'" + sys.argv[3] + "' is an invalid input! Must be a number > 0! No summary files are created!")
    sys.exit()

with open(infile) as inf:
    inf.readline()
    label = inf.readline()
    if inf.readline() == "":
        print("\n'" + infile + "' is empty! No summary report file is created for this taxon!")
        sys.exit()

samples = label.strip().split("\t")[1:-1]

with open(outfile, "w") as of:
    of.write("SAMPLE\tREADS\tPERCENT\n\n")
    for sample in range(len(samples)):
        sk = defaultdict(list)
        sp = defaultdict(list)
        sc = defaultdict(list)
        so = defaultdict(list)
        sf = defaultdict(list)
        sg = defaultdict(list)
        ss = defaultdict(list)
        
        with open(infile) as inf:
            inf.readline()
            inf.readline()
            for line in inf:
                sk[line.strip().split("\t")[len(samples) + 1].split(";")[0].strip().strip("k__")].append(line.strip().split("\t")[sample + 1])
                sp[line.strip().split("\t")[len(samples) + 1].split(";")[1].strip().strip("p__")].append(line.strip().split("\t")[sample + 1])
                sc[line.strip().split("\t")[len(samples) + 1].split(";")[2].strip().strip("c__")].append(line.strip().split("\t")[sample + 1])
                so[line.strip().split("\t")[len(samples) + 1].split(";")[3].strip().strip("o__")].append(line.strip().split("\t")[sample + 1])
                sf[line.strip().split("\t")[len(samples) + 1].split(";")[4].strip().strip("f__")].append(line.strip().split("\t")[sample + 1])
                sg[line.strip().split("\t")[len(samples) + 1].split(";")[5].strip().strip("g__")].append(line.strip().split("\t")[sample + 1])
                ss[line.strip().split("\t")[len(samples) + 1].split(";")[6].strip().strip("s__")].append(line.strip().split("\t")[sample + 1])

        for x in list(sk.keys()):
            sk[x] = int(sum([float(n) for n in sk[x]]))
            k = list(sk.items())
        k.sort(key=lambda x: x[1], reverse=True)
        for x in list(sp.keys()):
            sp[x] = int(sum([float(n) for n in sp[x]]))
            p = list(sp.items())
        p.sort(key=lambda x: x[1], reverse=True)
        for x in list(sc.keys()):
            sc[x] = int(sum([float(n) for n in sc[x]]))
            c = list(sc.items())
        c.sort(key=lambda x: x[1], reverse=True)
        for x in list(so.keys()):
            so[x] = int(sum([float(n) for n in so[x]]))
            o = list(so.items())
        o.sort(key=lambda x: x[1], reverse=True)
        for x in list(sf.keys()):
            sf[x] = int(sum([float(n) for n in sf[x]]))
            f = list(sf.items())
        f.sort(key=lambda x: x[1], reverse=True)
        for x in list(sg.keys()):
            sg[x] = int(sum([float(n) for n in sg[x]]))
            g = list(sg.items())
        g.sort(key=lambda x: x[1], reverse=True)
        for x in list(ss.keys()):
            ss[x] = int(sum([float(n) for n in ss[x]]))
            s = list(ss.items())
        s.sort(key=lambda x: x[1], reverse=True)

        otu_sum = 0
        for i in range(len(k)):
            otu_sum += k[i][1]
            
        of.write("Sample: " + samples[sample] + "\n")
        of.write("\nKINGDOM:" + "\n")
        for i in range(entries):
            try:
                of.write(str(k[i][0]) + "\t" + str(k[i][1]) + "\t" + str(round((k[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nPHYLUM:" + "\n")
        for i in range(entries):
            try:
                of.write(str(p[i][0]) + "\t" + str(p[i][1]) + "\t" + str(round((p[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nCLASS:" + "\n")
        for i in range(entries):
            try:
                of.write(str(c[i][0]) + "\t" + str(c[i][1]) + "\t" + str(round((c[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nORDER:" + "\n")
        for i in range(entries):
            try:
                of.write(str(o[i][0]) + "\t" + str(o[i][1]) + "\t" + str(round((o[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nFAMILY:" + "\n")
        for i in range(entries):
            try:
                of.write(str(f[i][0]) + "\t" + str(f[i][1]) + "\t" + str(round((f[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nGENUS:" + "\n")
        for i in range(entries):
            try:
                of.write(str(g[i][0]) + "\t" + str(g[i][1]) + "\t" + str(round((g[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\nSPECIES:" + "\n")
        for i in range(entries):
            try:
                of.write(str(s[i][0]) + "\t" + str(s[i][1]) + "\t" + str(round((s[i][1] / float(otu_sum)), 2)) + "\n")
            except:
                break
        of.write("\n\n")



