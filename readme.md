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

## USAGE:

DeViVa is a Python script that can be run on any operating system. Please ensure that you are using Python 3.x! To start a DeViVa analysis, go to a terminal and type in:

_python DeViVa.py -d \<data file\>_

You can add additional arguments if needed, but -d is always needed!

## DEPENDENCIES:

DeViVa needs some additional Python packages to be installed. You can install them manually or use the DeViVa.install file when working on Linux. Here is a full list of all required Python packages:

* Bio

* matplotlib

* numpy

* pandas

* scikit-bio

* scikit-learn

* scipy

* seaborn

## OPTIONS:

With the following options, you can adjust your DeViVa run. All parameters are optional except for -d, which needs to be always provided! Here is a list of all available options:
