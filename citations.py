# (c) Sebastian Hupfauf 2022
#
# Script for creating a file containing all used software including each reference.
#
# USAGE: python citations.py

import shutil
import os

cits = "\n======== CoMA3 pipeline ========\nCoMA 3.0: Hupfauf S, Etemadi M, Fernández-Delgado Juárez M, Gómez-Brandón M, Insam H, Podmirseg SM. 2020. CoMA–an intuitive and user-friendly pipeline for amplicon-sequencing data analysis. PloS one. 15: e0243241.\nbiom-format 2.1.9 (Conversion of BIOM files): McDonald D, Clemente JC, Kuczynski J, Rideout JR, Stombaugh J, Wendel D, et al. 2012. The Biological Observation Matrix (BIOM) format or: how I learned to stop worrying and love the ome-ome. GigaScience. 1: 7.\nmothur v.1.42.1 (Rarefaction curves): Schloss PD, Westcott SL, Ryabin T, Hall JR, Hartmann M, Hollister EB, et al. 2009. Introducing mothur: open-source, platform-independent, community-supported software for describing and comparing microbial communities. Appl. Environ. Microb. 75: 7537–7541. pmid:19801464.\nPANDAseq 2.11 (Merging of paired-end sequences): Masella AP, Bartram AK, Truszkowski JM, Brown DG, Neufeld JD. 2012. PANDAseq: paired-end assembler for illumina sequences. BMC Bioinformatics. 13: 31. pmid:22333067.\nPRINSEQ 0.20.4 (Quality check of FASTQ files, Trimming, Quality filtering): Schmieder R, Edwards R. 2011. Quality control and preprocessing of metagenomic datasets. Bioinformatics. 27: 863–864. pmid:21278185.\nQIIME (Removal of rare OTUs/ASVs/ZOTUs, Sequence subsampling): Caporaso JG, Kuczynski J, Stombaugh J, Bittinger K, Bushman FD, Costello EK, et al. 2010. QIIME allows analysis of high-throughput community sequencing data. Nat. Methods. 7: 335–336. pmid:20383131.\n======== Python packages ========\nMatplotlib 2.2.5: Hunter JD. 2007. Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering. 9: 90-95.\nNumPy 1.16.6: Harris CR, Millman KJ, van der Walt SJ, Gommers R, Virtanen P, Cournapeau D, et al. 2020. Array programming with NumPy. Nature. 585: 357–362.\npandas 0.24.2: McKinney W. 2010. Data structures for statistical computing in python. Proceedings of the 9th Python in Science Conference. 445: 51-56.\nscikit-bio 0.2.3: Rideout JR, Caporaso G, Bolyen E, McDonald D, Baeza YV, Alastuey JC, et al. 2018. biocore/scikit-bio: scikit-bio 0.5.5: More compositional methods added. doi:10.5281/zenodo.2254379.\nScikit_posthocs 0.6.7: Terpilowski MA. 2019. scikit-posthocs: pairwise multiple comparison tests in Python. Journal of Open Source Software. 4: 1169.\nSciPy 1.2.3: Virtanen P, Gommers R, Oliphant TE, Haberland M, Reddy T, Cournapeau D, et al. 2020. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature methods. 17: 261-272.\nseaborn 0.11.2: Waskom ML. 2021. Seaborn: statistical data visualization. Journal of Open Source Software. 6: 3021.\nZenipy 0.1.2: https://github.com/poulp/zenipy"


#Python Packages

cwd = os.getcwd()
shutil.copyfile(cwd + "/LotuSLogS/citations.txt", cwd + "/citations.txt")

with open("citations.txt", "a") as cf:
    cf.write(cits)
