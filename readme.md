<img
     title="a title"
     alt="Alt text"
     src="https://www2.uibk.ac.at/images/600x-auto/microbiology/services/coma/coma_logo.webp">
</img>
                                                                                             
# CoMA 3.0

Comparative Microbiome Analysis

## DESCRIPTION

Nowadays, modern biological or medical research is scarcely conceivable without the deep insights that are gained from next-generation sequencing (NGS). These technologies have been constantly improved and yield up to 20 billion reads per run today. This allows for studying highly complex environments such as gut, soil or biogas reactor sludge at a high resolution, but also requires an adequate analysis of the huge amount of generated data. A plethora of software packages for NGS data analysis are available today; however, most of them demand extensive knowledge in computer sciences or even need a bioinformatic specialist to be executed.

CoMA is a free pipeline for intuitive and user-friendly analysis of amplicon-sequencing data, available for all common computer platforms. The software package uses various open-source third party tools and combines them with own scripts into a linear analysis workflow in the form of a Bash script, starting with the raw input files (in FASTQ format) and resulting in aesthetically pleasing and publication-ready graphics. In addition, output files in standardized formats, such as a tab-delimited abundance table, an abundance table in BIOM format and a tree file in NEWICK format, are provided. These allow for subsequent secondary analysis using R for example.

The operation of this tool is remarkably intuitive and makes it accessible even for entry-level users. A graphical user interface facilitates the handling, representing a major advantage compared with command-line based applications. Nevertheless, multiple adjustment parameters and the high degree of automation make CoMA also suitable for advanced users who are looking for an efficient and streamlined workflow. The tool is capable of handling data from today’s most important NGS platforms, including Illumina MiSeq, Illumina HiSeq, Illumina NextSeq, and Illumina NovaSeq, but also from the former 454 pyrosequencing technology, which was, in fact, terminated in 2016 but data are still around and analysis tools are still needed.

CoMA can be run on every common computer operating system: Linux, Windows, and macOS. With version 3.0, four different options for installation are available: a virtual appliance (which can be imported with tools like VMware Workstation, Oracle VM Virtualbox or Parallels Desktop for macOS), a Singularity image, a Docker image, and a direct Linux installer (Bash script). Each option provides specific advantages and the user can select the most suitable one in order to meet his needs. CoMA can also be used on high performance computer systems (HPC cluster). In this case, we suggest using the Singularity option. The following graphical summary shall help finding the ideal usage strategy for every user.

<img title="a title" alt="Alt text" src="https://www2.uibk.ac.at/images/600x-auto/microbiology/services/coma/fig1.webp">

CoMA will be updated regularly to ensure an excellent performance also in the future, but also to implement additional features (e.g. a web-based platform for online data analysis). These updates will always include the newest versions of the taxonomic databases at the release date to guarantee the best possible and most current results.

## CITATION

If you use CoMA for any published research, please include the following citation:

Hupfauf S, Etemadi M, Fernández-Delgado Juárez M, Gómez-Brandón M, Insam H, et al. (2020) CoMA – an intuitive and user-friendly pipeline for amplicon-sequencing data analysis. PLOS ONE 15(12): e0243241. https://doi.org/10.1371/journal.pone.0243241

## INSTALL

For installing CoMA, please visit the product webpage: https://www.uibk.ac.at/microbiology/services/coma.html. You can find there severeal options for installation CoMA on any common operating system. Moreover, you have access to olfer versions of the tool in case you need them.

## OUTPUT

This chapter describes the output of the CoMA pipeline in detail and shall help the user to navigate through his/her results. It also tackles files, which were computed during the CoMA run but which are not used by the pipeline directly. However, all files are stored in standardized formats and may be used by advanced users for secondary and more sophisticated analysis (e.g. using R). All result files can be found in the following directory:

__.../Results__

Directories:

|   Directory   |   Description   |
|:--------------|:----------------|
|alpha_diversity|Alpha diversity plot(s) and text file(s) containing the underlying data of the diversity analysis. Moreover, you can find the results of the statistical tests (Kruskal-Wallis H-test, Conover post-hoc test with Benjamini-Hochberg correction) if metadata were used for sample grouping.|
|beta_diversity|Here you can find two sub-directories including all files from the ordination analysis as well as from the hierarchical cluster analysis. In the “ordination” directory, you find the PCoA plot, the distance matrix and a file containing the eigenvalues for all PC axis. Moreover, you can find the results of the statistical tests using ANOSIM and PERMANOVA if metadata were used for sample grouping. In the “cluster_analysis” directory, you find the dendrogram(s).|
|ExtraFiles|Here you can find files summarizing the chimera removal step. Moreover, a file including the multiple sequence alignment of OTUs/ASVs/ZOTUs (“OTU.MSA.fna”) is stored here in FASTA format. Divergent positions are indicated with hyphens (“-“).|
|higherLvl|This directory includes Species, Genus, Family, Class, Order and Phylum abundance matrices.|
|LotuSLogS|Several log files are stored here. These files are usually not needed; however, they may be helpful in case of unexpected results or other problems. For detailed explanation, please refer to the online documentation of LotuS (the software package that is involved in OTU/ASV/ZOTU clustering and taxonomic assignment): http://lotus2.earlham.ac.uk/.|
|primary|Here you can find an option file for the sdm tool, which is responsible for the demultiplexing and quality filtering of sequences. In addition, you can find a copy of the map file, which was constructed in course of the analysis.|
|rarefaction_curves|This directory includes the rarefaction plot(s), a Mothur log file of the rarefaction analysis, and the underlying data files. The number of files as well as their labelling depends on the chosen calculator. “abundance.groups.rarefaction” summarizes for instance all data when otu was the calculator and “abundance.groups.r_shannon” would include the results of a rarefaction analysis based on the Shannon-Wiener diversity.|
|summary_reports|Here you can find all your summary reports including either all detected taxa (key word “Total”) or entries associated only with a specific taxon. Files including the key word “individual” show results for each individual sample whereas files without show results for groups defined by metadata variables.|
|taxa_plots|Here you can find all your taxonomic plots (bar charts, heatmaps).|
|Venn_plots|Here you can find the Venn plots.|

Files:

|   File   |   Description   |
|:---------|:----------------|
|abundance.biom|This is the current abundance table in BIOM format. BIOM (Biological Observation Matrix) was designed in order to represent a widely accepted and supported file format for contingency tables of biological samples. BIOM files can be easily converted to tab-delimited abundance tables and vice versa using the biom-convert tool. For more information, please refer to the BIOM webpage: http://biom-format.org/. Please see also the information provided for “abundance.txt”.|
|abundance.txt|This is the most current abundance file of your analysis (including the identical information as the “abundance.biom” file but stored in a different format). Depending on your settings, this table may include rarefied, subsampled, renamed or grouped samples/replicates/groups. IMPORTANT: it is indispensable to know which steps have been performed during the CoMA analysis if you want to do further analysis based on this file!|
|abundance_original.biom|This is the original abundance table in BIOM format for your analysis, which was constructed immediately after OTU/ASV/ZOTU clustering and taxonomic assignment. It does not include any post-processing steps such as rarefication or subsampling.|
|abundance_original.txt|This is the original abundance table for your analysis, which was constructed immediately after OTU clustering and taxonomic assignment. It does not include any post-processing steps such as subsampling (equal information to “abundance_original.biom”).|
|abundance_without_subsampling.biom|This is the BIOM-converted abundance table after the removal of rare OTUs/ASVs/ZOTUs, but without subsampling or sample renaming.|
|abundance_without_subsampling.txt|This is the abundance table after the removal of rare OTUs/ASVs/ZOTUs, but without subsampling or sample renaming (equal information to “abundance_without_subsampling.biom”).|
|citations.txt|This file contains a summary of all third party software that was used for the current CoMA run. Please keep in mind that a proper citation strategy helps the development teams to maintain and improve their products!|
|hiera_BLAST.txt|This abundance file shows the taxonomic assignments based on BLAST. IMPORTANT: Be aware that this file is missing (and replaced by another, e.g. “hiera_RDP.txt”) when BLAST was not the selected aligner tool for taxonomic assignment!|
|mapping.txt|This file includes all the metadata that were provided by the user. Keep in mind that this file is missing if no metadata were entered (step 31).|
|OTU.fna|This file shows the extended OTU/ASV/ZOTU seed sequences in FASTA format. The sequences given here are identical to those in “ExtraFiles/OTU.MSA.fna”, but without the hyphens.|
|OTU.txt|This file represents an OTU/ASV/ZOTU abundance matrix, showing which OTU/ASV/ZOTU appears in which sample/group and at which number.|
|OTUphylo.nwk|This file represents a taxonomic tree in NEWICK format. It is used for phylogeny-based alpha/beta diversity analyses (Faith’s PD, weighted/unweighted UniFrac distance). Moreover, advanced users may use this for even more-sophisticated secondary analyses based on taxonomic information and the tree structure (e.g. with FastTree, FigTree, GraPhlAn).|
|phyloseq.Rdata|This is a Phyloseq object, which is ready to be loaded directly in R for secondary data analysis.|
|rem_seq.txt|This file summarized the amount of sequences that were dropped/lost in course of the analysis. With this information, the user can estimate the overall loss of reads as well as determine which step removed the most sequences (e.g. quality filtering, chimera removal, phiX contaminants).|

## SOFTWARE LIST

CoMA is a pipeline for NGS data analysis, using various applications, tools and scripts originating from internal and external sources (open-source third party software). Within this section, all external tools are listed. Please follow the web links if you want to get more information on a specific tool. Keep in mind that some of these tools may also be using third party software, for more information consult the prevailing manuals.

* QIIME

* Mothur

* Pandaseq

* Prinseq-lite

* LotuS2

* USEARCH

* BIOM-format-tools

## SUPPORT

If there are any problems with the installation or the use of CoMA please contact coma-mikrobiologie@uibk.ac.at

## UPDATE NOTES

__CoMA 3.0__

|   __CoMA 3.0__   |
|:-----------------|
|A fourth installation option for CoMA was added, allowing the usage of the tool from within a Docker container. This option is available for users working on a Linux, macOS, or Windows system.|
|CoMA can now also construct ASVs and ZOTUs (which can be interpreted as OTUs with a sequence similarity of 100%) in addition to OTUs.|
|CoMA now offers different algorithms for sequence clustering in addition to UPARSE (constructing OTUs): Swarm (OTUs), CD-Hit (OTUs), UNOISE3 (ZOTUs), and DADA2 (ASVs).|
|The sequence identity for clustering OTUs can now be adjusted between 80-100% (previously set to 97%). REMARK: This is currently only possible when using CD-Hit!|
|The user can now also select VSEARCH for the removal of chimeric sequences (previously only USEARCH). REMARK: This is only possible for clustering algorithms other than UPARSE!|
|Two additional aligning tools are now available for taxonomic assignment: USEARCH and VSEARCH (previously only Blast, Lambda and RDP).|
|CoMA can now be used without installing USEARCH! ATTENTION: Keep in mind that doing so limits the options for sequence clustering (UPARSE and UNOISE3 are not available in this case), chimera removal (no USEARCH) and taxonomic assignment (no USEARCH)!|
|A metadata variable is automatically selected if “mapping.txt” includes only a single one. REMARK: This is only relevant for steps in which the user decides to use metadata for structuring the data (summary reports, taxa plots, Venn plots, alpha diversity plots, ordination plots, and dendrograms).|
|CoMA now shows a warning message if summary reports or taxa plots cannot be created because no data were found for the selected taxon.|
|Summary reports are now stored in a dedicated directory (/summary_reports).|
|Summary reports are now labelled based on the used metadata variable. This allows creating multiple summary reports without overwriting the previous ones.|
|Taxa plots are now stored in different directories for each combination of settings (metadata variable, abundance threshold, including/excluding unassigned sequences). This allows creating multiple sets of plots without overwriting the previous ones.|
|Running the step for removing rare OTUs/ASVs/ZOTUs with zero no longer leads to an error and the termination of the workflow.|
|When doing alpha diversity analysis with metadata, underlying data are now stored as means  standard deviation (previously, results were showed only for individual samples).|
|Orientation lines at x=0 and y=0 were added to the PCoA plots.|
|Sample names in dendrograms can now be labelled based on metadata. This shall help identifying structures within the dataset.|
|A file including all used third party software and their references is now provided in order to guarantee a proper citation.|
|All CoMA scripts were generally revised and updated.|
|The CoMA manual was improved and updated.|

__CoMA 2.0__

* Two additional options for installation are provided now: a Singularity image and a direct Linux installer.

* The Ubuntu operating system was updated to version 20.04 LTS (in CoMA 1.0: Ubuntu 16.04 LTS).

* All CoMA source files are now available here on GitHub.

* Support of multithreading. You can assign now multiple CPU cores to CoMA leading to a considerably better performance resulting in shorter computation times.

* Support of USEARCH v11. For more information, please visit the online documentation: https://drive5.com/usearch/manual/whatsnewv11.html.

* All taxonomic databases were updated. This includes also the newest release of the SILVA database (version 138).

* CoMA now offers two log files for each run: a compact log file including the user settings and inputs, and a detailed log file with all the information including potential warnings and error messages.

* Sequences can now be filtered based on the number of ambiguous bases (Ns) in course of the trimming/quality filtering step.

* CoMA now supports the analysis of single-end data or of sequence files that were already merged.

* Sample registration is now a separate step und no longer connected to sequence merging. With that, the merging step can be repeated multiple times without the necessarily to provide the common part of the sample names each time.

* CoMA now checks if input files are missing when analysing paired-end data. Moreover, CoMA now detects wrongly assigned pattern strings in course of the sample registration step.

* Several steps checking for missing dependencies have been implemented in order to help the user locating a problem.

* Rarefaction curves can now be computed based on five different calculators: OTU/ASV/ZOTU count, Chao1 diversity, Shannon-Wiener index, Simpson index, and Good’s coverage for OTU/ASV/ZOTU (compared to only OTU count in CoMA 1.0).

* Samples can now be renamed in order to avoid confusing names, which are often assigned by NGS machines or sequencing companies.

* CoMA now supports metadata, which can be used for grouping samples based on specific parameters.

* CoMA now supports general summary reports (for Archaea, Bacteria, Fungi, Eukaryota, and all data) as well as specific summaries based on a given taxon. The summary reports are provided as tab-delimited text file, where the information can be easily extracted and used for further analysis. In addition, the user can now select the numbers of entries for each taxonomic level (in CoMA 1.0, it was pre-set to 5).

* CoMA now supports general (for Archaea, Bacteria, Fungi, Eukaryota, and all data) and specific taxonomic plots (bar charts, heatmaps) based on a given taxon. In addition, unassigned taxa can now be included or excluded from the depiction.

* CoMA now supports Venn plots for the taxonomic comparison of two or three groups.

* The calculation step for alpha diversity is now improved and the user can choose between various metrics. CoMA supports now also phylogeny-based alpha diversity calculation (Faith’s PD).

* CoMA now offers statistical tests for alpha diversity (Kruskal-Wallis H-test, Conover post-hoc test with Benjamini-Hochberg correction), as long as samples were grouped based on metadata.

* Aside Hierarchical Cluster Analysis (HCA), CoMA now supports ordination (Principal Coordinates Analysis, PCoA) as second option for beta diversity analysis. The user can choose between various metrics, including phylogeny-based weighted/unweighted UniFrac distance.

* CoMA now offers also statistical tests for beta diversity (ANOSIM, PERMANOVA) in order to quantify the strength of clustering determined with PCoA.

* You can now select a file format and, in case of raster graphic formats, the pixel density (DPI) for all CoMA graphics (rarefaction curves, bar charts, heatmaps, Venn plots, alpha diversity plots, PCoA plots, dendrograms). CoMA supports 10 different file formats, including the most popular raster- (e.g. “JPEG”, “PNG”, “TIFF”) and vector- (e.g. “EPS”, “PDF”, “SVG”) graphic formats.

* We established an overall CoMA colour code. All CoMA graphics are now using the same colour palette (ranging from blue to green to yellow to beige). 

* All CoMA 1.0 scripts were revised and optimised where needed.

* CoMA now uses Python 3 (in comparison to Python 2 in CoMA 1.0).

* Any directory can now be used for CoMA projects, allowing much more flexibility and facilitates the usage of CoMA on HPC systems.

* CoMA now shows a warning message if a new project is started using an already existing project name. The user can decide if he wants to keep the old data or overwrite it with the new project.

* The CoMA manual was completely overworked and improved. Moreover, a chapter describing the CoMA output in detail was included.
