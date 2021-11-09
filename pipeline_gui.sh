#!/bin/bash

# CoMA Pipeline
# Copyright (C) 2020 Sebastian Hupfauf, Mohammad Etemadi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# contact
# ------
# coma-mikrobiologie@uibk.ac.at

project=$(echo $wd | rev | cut -d"/" -f1 | rev)

echo -e "\n********************************************************************************"
echo "      Welcome to CoMA, the pipeline for amplicon sequencing data analysis!           "
echo -e "********************************************************************************\n"
echo -e "Project: "$project"\n"
echo -e "________________________________________________________________________________\n"

cd $wd/Data
proc=$(head -n 1 $wd/Data/proc.txt 2>> $wd/${date}_detailed.log) || proc=$(cat /proc/cpuinfo | grep processor | wc -l)

#Sample description

(zenity --no-wrap --question --title $project --text "Do you want to assign your files and choose the number of CPUs?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

max_proc=$(cat /proc/cpuinfo | grep processor | wc -l)
if [ $max_proc = 1 ]
then

echo "Only 1 CPU detected! All analyses will be done with a single core."
proc=1
echo $proc > proc.txt

else
proc=$(zenity --scale --text "How many CPUs du you want to use?" --title $project --value=1 --min-value=1 --max-value=$max_proc --step=1 2>> $wd/${date}_detailed.log)
echo $proc > proc.txt
fi

(zenity --no-wrap --question --title $project --text "Are you using paired-end reads (a forward and reverse file per sample)?
Click 'No' if you have single-end reads (only a single file per sample)." &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

sequence=$(zenity --forms --title=$project --text='Please describe your samples' --add-entry="What is the common file name ending of your forward files? 
e.g. _R1_001.fastq.gz or _FW_001.fastq.gz:" --add-entry="What is the common file name ending ending of your reverse files? 
e.g. _R2_001.fastq.gz or _REV_001.fastq.gz:" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

f=$(awk -F '[|]' '{print $1}' <<<$sequence)
r=$(awk -F '[|]' '{print $2}' <<<$sequence)
echo $f > pattern.txt
echo $r >> pattern.txt

cp /usr/local/Pipeline/filelist.py ./
python3 filelist.py $f name.txt $proc $r 2>> $wd/${date}_detailed.log
rm filelist.py

fi

else

pat=$(zenity --forms --title=$project --text='Please describe your samples' --add-entry="What is the common file name ending of your files? 
e.g. _001.fastq.gz or .fastq.gz:" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo $pat > pattern.txt

cp /usr/local/Pipeline/filelist.py ./
python3 filelist.py $pat name.txt $proc 2>> $wd/${date}_detailed.log
rm filelist.py

mkdir -p processed_reads

for file in $(<name.txt)
do
cp ${file}$pat processed_reads/ 2>> $wd/${date}_detailed.log
mv processed_reads/${file}$pat processed_reads/${file}.fastq.gz 2>> $wd/${date}_detailed.log
gunzip --force processed_reads/${file}.fastq.gz 2>> $wd/${date}_detailed.log
done

fi
fi
fi

#Merging

if ! [[ -f "pattern.txt" ]]
then
echo "" > pattern.txt
fi

if [[ $(wc -l </$wd/Data/pattern.txt) = 2 ]]
then

(zenity --no-wrap --question --title $project --text "Do you want to merge your files?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

if ! [[ -f "threads.txt" ]]
then
echo -e "\nATTENTION: Your threads.txt file is empty, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

start=$(date +%s)
echo -e "\nMerging process proceeding ..."

cd $wd/Data

mkdir -p processed_reads

f=$(head -n 1 pattern.txt)
r=$(tail -n 1 pattern.txt)

for thread in $(<threads.txt)
do

if ! [[ -f $thread ]]
then
echo -e "\nATTENTION: One of your n*.txt files is missing, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for file in $(<${thread})
do

pandaseq -f ${file}$f -r ${file}$r -F -w processed_reads/${file}.fastq -g processed_reads/${file}.log &>> $wd/${date}_detailed.log &

done
done
wait

for thread in $(<threads.txt)
do
for file in $(<${thread})
do

if ! [ -s processed_reads/${file}.fastq ]
then
echo -e "\nATTENTION: There was an error detected during the merging process, at least one of your files containing merged reads is empty! Check the pattern.txt file and if all paired-end files are provided. CoMA run terminated!"
xargs kill
fi

done
done

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nMerging completed! (Duration: "$dur"s)"
echo -e "\n________________________________________________________________________________\n"

fi
fi

#Quality Check of input files


(zenity --no-wrap --question --title $project --text "Do you want to check the quality of the input files?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

start=$(date +%s)

cd $wd/Data

mkdir -p quality_reports
cd quality_reports
mkdir -p quality_before_filtering
cd ..

echo -e "\nQuality check of input files proceeding ..."

if ! [[ -f "threads.txt" ]]
then
echo -e "\nATTENTION: Your threads.txt file is empty, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for thread in $(<threads.txt)
do

if ! [[ -f $thread ]]
then
echo -e "\nATTENTION: One of your n*.txt files is missing, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for file in $(<${thread})
do
prinseq-lite -fastq processed_reads/${file}.fastq -graph_data quality_reports/quality_before_filtering/${file}.gd -out_good null -out_bad null &>> $wd/${date}_detailed.log &

done
done
wait

for thread in $(<threads.txt)
do
for file in $(<${thread})
do
prinseq-graphs-noPCA -i quality_reports/quality_before_filtering/${file}.gd -html_all -o quality_reports/quality_before_filtering/${file} &>> $wd/${date}_detailed.log &
done
done
wait

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nQuality report created! (Duration: '$dur's) 
Open the .html files to view the detailed quality report in your browser.'
echo -e "\n________________________________________________________________________________\n"

fi

#Trimming

(zenity --no-wrap --question --title $project --text "Do you want to trim your files (e.g. barcode, primers etc.) and/or apply quality filtering?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then
           
cd $wd/Data

out=$(zenity --forms --title=$project --text="Please provide the parameters for the trimming/quality filtering process:" --add-entry="Trim from forward side (5' end):" --add-entry="Trim from reverse side (3' end):" --add-entry="Maximum fragment length:" --add-entry="Minimum fragment length:" --add-entry="Minimum average PHRED quality score:" --add-entry="Maximum number of ambiguous bases:" 2>> $wd/${date}_detailed.log)
if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nTrimming process proceeding ..."
echo

tl=$(awk -F '[|]' '{print $1}' <<<$out)
tr=$(awk -F '[|]' '{print $2}' <<<$out)
maxl=$(awk -F '[|]' '{print $3}' <<<$out)
minl=$(awk -F '[|]' '{print $4}' <<<$out)
mq=$(awk -F '[|]' '{print $5}' <<<$out)
amb=$(awk -F '[|]' '{print $6}' <<<$out)

mkdir -p filtered_reads
cd filtered_reads
mkdir -p good_sequences
mkdir -p discarded_sequences
cd ..

if ! [[ -f "threads.txt" ]]
then
echo -e "\nATTENTION: Your threads.txt file is empty, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for thread in $(<threads.txt)
do

if ! [[ -f $thread ]]
then
echo -e "\nATTENTION: One of your n*.txt files is missing, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for file in $(<${thread})
do
prinseq-lite -fastq processed_reads/${file}.fastq -out_good filtered_reads/good_sequences/${file} -out_bad filtered_reads/discarded_sequences/${file} -trim_left $tl -trim_right $tr -max_len $maxl -min_len $minl  -min_qual_mean $mq -ns_max_n $amb -out_format 5 -log &>> $wd/${date}_detailed.log &

done
done
wait

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nDone! (Duration: "$dur"s) Your files were trimmed/quality filtered using the following settings:"
echo
echo "Trim from forward side (5' end): " $tl
echo "Trim from reverse side (3' end): " $tr
echo "Maximum fragment length: " $maxl
echo "Minimum fragment length: " $minl
echo "Minimum average PHRED quality score: " $mq
echo "Maximum number of ambiguous bases: " $amb
echo -e "\n________________________________________________________________________________\n"

fi
fi

#Quality good seq

(zenity --no-wrap --question --title $project --text "Do you want to check the quality of your trimmed/quality filtered files?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

start=$(date +%s)
             
cd $wd/Data
mkdir -p quality_reports
cd quality_reports
mkdir -p good_sequences
mkdir -p discarded_sequences
cd ..

echo -e "\nQuality control of trimmed reads proceeding ..."

if ! [[ -f "threads.txt" ]]
then
echo -e "\nATTENTION: Your threads.txt file is empty, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for thread in $(<threads.txt)
do

if ! [[ -f $thread ]]
then
echo -e "\nATTENTION: One of your n*.txt files is missing, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

for file in $(<${thread})
do
prinseq-lite -fastq filtered_reads/good_sequences/${file}.fastq -graph_data quality_reports/good_sequences/${file}.gd -out_good null -out_bad null &>> $wd/${date}_detailed.log &
done
done
wait

for thread in $(<threads.txt)
do
for file in $(<${thread})
do
prinseq-graphs-noPCA -i quality_reports/good_sequences/${file}.gd -html_all -o quality_reports/good_sequences/${file} &>> $wd/${date}_detailed.log &
done
done
wait

#Quality bad seq

for thread in $(<threads.txt)
do
for file in $(<${thread})
do
prinseq-lite -fastq filtered_reads/discarded_sequences/${file}.fastq -graph_data quality_reports/discarded_sequences/${file}.gd -out_good null -out_bad null &>> $wd/${date}_detailed.log &
done
done
wait

for thread in $(<threads.txt)
do
for file in $(<${thread})
do
prinseq-graphs-noPCA -i quality_reports/discarded_sequences/${file}.gd -html_all -o quality_reports/discarded_sequences/${file} &>> $wd/${date}_detailed.log &
done
done
wait

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nQuality report created! (Duration: '$dur's) 
Open the .html files to view the detailed quality report of the good sequences 
in your browser.'
echo -e "\n________________________________________________________________________________\n"

fi

#Blasting using lotus: http://psbweb05.psb.ugent.be/lotus/tutorial_R.html

(zenity --no-wrap --question --title $project --text "Do you want to align your sequences and make a taxonomic assignment?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

if ! [[ -f "name.txt" ]]
then
echo -e "\nATTENTION: Your name.txt file is empty, please rerun sample registration! - CoMA run terminated!"
xargs kill
fi

cd $wd/Data

cp /usr/local/Pipeline/create_map.py ./
python3 create_map.py name.txt map.txt &>> $wd/${date}_detailed.log
rm create_map.py

sim=$(zenity --text "Please choose an aligner tool:" --title $project --list --column "Aligner" --column "Database" "RDP" "search against the RDP database" "blast" "you can choose between various databases (including custom DB)" "lambda" "you can choose between various databases (including custom DB)" --separator="," --height=250 --width=600 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $sim = "RDP" ]
then

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

ref="RDP"

elif [ $sim = "blast" ]
then

ref=$(zenity --text "Please choose a reference database:

Databases can be combined, with the first having the highest prioirty (e.g. PR2,SLV would 
first use PR2 to assign OTUs/ASVs/ZOTUs and all unassigned OTUs/ASVs/ZOTUs would be searched for with SILVA).

For detailed information on custom databases and how they need to be formatted, please visit:
http://psbweb05.psb.ugent.be/lotus/images/CustomDB_LotuS.pdf 

ATTENTION: A custom database cannot be combined with any other database!

- SLV: Silva LSU (23/28S) or SSU (16/18S)
- GG: Greengenes (only 16S available)
- UNITE: ITS focused on fungi
- PR2: SSU focused on Protists
- HITdb: database specialized only on human gut microbiota
- beetax: bee gut specific database
- CD: custom database
" --title $project --height=250 --width=600 --entry 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

if [ $ref = "CD" ]
then

customdb=$(zenity --title "Please choose your database file (in fasta format):" --file-selection 2>> $wd/${date}_detailed.log)

cd
cd $( dirname $customdb)

if [[ $? -ne 1 ]]
then 

customtax=$(zenity --title "Please choose your taxonomy file:" --file-selection 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

cd

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $customdb  -tax4refDB $customtax -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi
fi

elif [[ $ref == *"SLV"* ]]
then

type=$(zenity --text "Which Silva database do you want to use?" --title $project --list --column "" --column "" "LSU" "Database for large ribosomal subunit (23/28S)" "SSU" "Database for small ribosomal subunit (16/18S)" --height=250 --width=600 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $ref -amplicon_type $type -greengenesSpecies 0 -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi

else

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $ref -greengenesSpecies 0 -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi
fi

elif [ $sim = "lambda" ]
then

cd $wd

ref=$(zenity --text "Please choose a reference database:

Databases can be combined, with the first having the highest prioirty (e.g. PR2,SLV would 
first use PR2 to assign OTUs/ASVs/ZOTUs and all unassigned OTUs/ASVs/ZOTUs would be searched for with SILVA).

For detailed information on custom databases and how they need to be formatted, please visit:
http://psbweb05.psb.ugent.be/lotus/images/CustomDB_LotuS.pdf 

ATTENTION: A custom database cannot be combined with any other database!

- SLV: Silva LSU (23/28S) or SSU (16/18S)
- GG: Greengenes (only 16S available)
- UNITE: ITS focused on fungi
- PR2: SSU focused on Protists
- HITdb: database specialized only on human gut microbiota
- beetax: bee gut specific database
- CD: custom database
" --title $project --height=250 --width=600 --entry 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

if [ $ref = "CD" ]
then

customdb=$(zenity --title "Please choose your database file (in fasta format):" --file-selection 2>> $wd/${date}_detailed.log)

cd
cd $( dirname $customdb)

if [[ $? -ne 1 ]]
then 

customtax=$(zenity --title "Please choose your taxonomy file:" --file-selection 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

cd

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $customdb  -tax4refDB $customtax -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi
fi

elif [[ $ref == *"SLV"* ]]
then

type=$(zenity --text "Which Silva database do you want to use?" --title $project --list --column "" --column "" "LSU" "Database for large ribosomal subunit (23/28S)" "SSU" "Database for small ribosomal subunit (16/18S)" --height=250 --width=600 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $ref -amplicon_type $type -greengenesSpecies 0 -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi

else

start=$(date +%s)

echo -e "\nSequence alignment and taxonomic assignment proceeding ..."

lotus2 -c /usr/local/Pipeline/lotus2/lOTUs.cfg -p miSeq -thr $proc -simBasedTaxo $sim -refDB $ref -greengenesSpecies 0 -i $wd/Data/filtered_reads/good_sequences/ -m $wd/Data/map.txt -o $wd/Results -s /usr/local/Pipeline/lotus2/configs/sdm_miSeq.txt &>> $wd/${date}_detailed.log

fi
fi
fi

cd $wd/Results

if [ -f "OTU.biom" ]
then

if ! [ -s "OTU.biom" ]
then
echo -e "\nATTENTION: There was an error detected during the clustering/aligning process, your abundance file is empty! CoMA run terminated!"
xargs kill
fi

biom convert -i OTU.biom -o otu_table.txt --to-tsv --header-key taxonomy  &>> $wd/${date}_detailed.log

cp /usr/local/Pipeline/report.py ./
python3 report.py &>> $wd/${date}_detailed.log
rm report.py

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nSequence alignment and taxonomic assignment were successful! (Duration: "$dur"s) 
Output files are created using following settings:"
echo
echo "Aligner: " $sim

if [[ $ref == *"SLV"* ]]
then
echo "Reference database(s): "$ref" ("$type")"
else
echo "Reference database(s): " $ref
fi

echo -e "\n________________________________________________________________________________\n"

else
echo -e "An ERROR raised during the blasting process!"
xargs kill

echo -e "\n________________________________________________________________________________\n"
fi
fi
fi

###Post processing

#Singleton removal

(zenity --no-wrap --question --title $project --text "Do you want to remove rare OTUs/ASVs/ZOTUs from your dataset?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

depth=$(zenity --text "Please enter the minimum number of reads for an OTU/ASV/ZOTU to be retained:" --title $project --scale --min-value=0 --max-value=100000 --step=1 2>> $wd/${date}_detailed.log)

if [[ $depth = 0 ]] || [[ $depth = "" ]]
then
depth=1
fi

if [[ $? -ne 1 ]]
then

samples=$(zenity --text "Please enter the minimum number of samples in which an OTU/ASV/ZOTU must be present to be retained:" --title $project --scale --min-value=0 --max-value=100000 --step=1 2>> $wd/${date}_detailed.log)

if [[ $samples = 0 ]] || [[ $samples = "" ]]
then
samples=1
fi

if [[ $? -ne 1 ]]
then  

start=$(date +%s)

cd $wd/Results

echo -e "\nRemoval of rare OTUs/ASVs/ZOTUs proceeding ..."

mv OTU.biom OTU_original.biom
mv otu_table.txt otu_table_original.txt

filter_otus_from_otu_table.py -i OTU_original.biom -o OTU.biom -n $depth -s $samples &>> $wd/${date}_detailed.log
biom convert -i OTU.biom -o otu_table.txt --to-tsv --header-key taxonomy &>> $wd/${date}_detailed.log

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nProcess succeeded! (Duration: "$dur"s) Rare OTUs/ASVs/ZOTUs are removed from your 
dataset using the following settings:"
echo
echo "Minimum sum of reads within all samples: " $depth
echo "Minimum sample occurences: " $samples
echo -e "\n________________________________________________________________________________\n"
fi
fi
fi

#Rarefaction curves

(zenity --no-wrap --question --title $project --text "Do you want to generate rarefraction curves?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

calc=$(zenity --text "Please choose a calculator for rarefaction analysis:" --title $project --list --column "Calculator" --column "" "otu" "Observed taxonomic units" "chao" "Chao1 richness estimator" "shannon" "Shannon-Wiener diversity index" "simpson" "Simpson diversity index" "coverage" "Good's coverage for OTU" --separator="," --height=225 --width=400 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

fformat=$(zenity --text "Please choose a file format:" --title $project --list --column "File format" --column "" "EPS" "Encapsulated Postscript" "JPEG" "Joint Photographic Experts Group" "PDF" "Portable Document Format" "PNG" "Portable Network Graphics" "PS" "Postscript" "RAW" "Raw bitmap" "RGBA" "RGBA bitmap" "SVG" "Scalable Vector Graphics" "SVGZ" "Compressed SVG" "TIFF" "Tagged Image File Format" --separator="," --height=300 --width=400 2>> $wd/${date}_detailed.log)

if [ $fformat = "JPEG" ] || [ $fformat = "PNG" ] || [ $fformat = "RAW" ] || [ $fformat = "RGBA" ] || [ $fformat = "TIFF" ]
then

dpi=$(zenity --text "Pixel density [dpi]" --title $project --entry 2>> $wd/${date}_detailed.log)

else
dpi=100

fi


start=$(date +%s)

if [ $calc = "otu" ]
then
calc="sobs"
fi

echo -e "\nRarefaction curves are now created ..."

cd $wd/Results
mkdir -p rarefaction_curves
cd rarefaction_curves

cp ../otu_table.txt ./
cp /usr/local/Pipeline/create_shared_file.py ./
cp /usr/local/Pipeline/rarefactionplot.py ./

python3 create_shared_file.py otu_table.txt otu.shared &>> $wd/${date}_detailed.log
mothur "#rarefaction.single(shared=otu.shared, calc=$calc, processors=$proc)" &>> $wd/${date}_detailed.log
python3 rarefactionplot.py $calc $fformat $dpi &>> $wd/${date}_detailed.log

rm create_shared_file.py
rm rarefactionplot.py
rm otu_table.txt
rm otu.shared

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nProcess succeeded! (Duration: '$dur's)
\nCalculator: '$calc
echo -e "\n________________________________________________________________________________\n"
fi
fi

#Subsampling

(zenity --no-wrap --question --title $project --text "Do you want to make a subsampling of your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results

cp /usr/local/Pipeline/reads.py ./
python3 reads.py otu_table.txt 2>> $wd/${date}_detailed.log

sub=$(zenity --text "Please enter the number of reads for the subsampling:" --title $project --entry 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nSubsampling process proceeding ..."

mv OTU.biom OTU_without_subsampling.biom
mv otu_table.txt otu_table_without_subsampling.txt

single_rarefaction.py -i OTU_without_subsampling.biom -o OTU.biom -d $sub  &>> $wd/${date}_detailed.log
biom convert -i OTU.biom -o otu_table.txt --to-tsv --header-key taxonomy &>> $wd/${date}_detailed.log

rm reads.py

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nProcess succeeded! (Duration: '$dur's) Your samples are subsampled to the length of:' $sub
echo -e "\n________________________________________________________________________________\n"
fi
fi

#Renaming

(zenity --no-wrap --question --title $project --text "Do you want to rename your samples/groups?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

echo -e "\nRenaming of samples in progress ..."

cd $wd/Results

cp /usr/local/Pipeline/rename.py ./
python3 rename.py otu_table.txt 2>> $wd/${date}_detailed.log
biom convert -i otu_table.txt -o OTU.biom --to-hdf5 --table-type="OTU table" --process-obs-metadata taxonomy &>> $wd/${date}_detailed.log

rm rename.py

echo -e '\nProcess succeeded! Your samples are renamed now!'
echo -e "\n________________________________________________________________________________\n"

fi

#Mapping

(zenity --no-wrap --question --title $project --text "Do you want to add metadata (e.g. environmental data) to your samples?

These information can be used in the upcoming steps to group the samples specifically." &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results

cp /usr/local/Pipeline/mapping.py ./
python3 mapping.py otu_table.txt mapping.txt 2>> $wd/${date}_detailed.log
rm mapping.py

fi

#Summary Report

(zenity --no-wrap --question --title $project --text "Do you want to generate a summary report of the phylogenetic diversity?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

(zenity --no-wrap --question --title $project --text "Do you want to use the information in the mapping file to group your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results

cp /usr/local/Pipeline/map_group.py ./
python3 map_group.py otu_table.txt mapping.txt current_otu_table.txt 2>> $wd/${date}_detailed.log
rm map_group.py

else

cd $wd/Results

cp otu_table.txt ./current_otu_table.txt

fi

(zenity --no-wrap --question --title $project --text "Do you want a general summary?
Click 'No' for summary on a specific taxon!" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

sr=$(zenity --text "For which kingdom do you want to create the summary?" --title $project --list --checklist --column "" --column "Kingdom" "" "Archaea" "" "Bacteria" "" "Fungi" "" "Eukaryota" "" "Total" --separator="," --height=250 --width=600 2>> $wd/${date}_detailed.log)

entries=$(zenity --forms --title=$project --text='How many taxa do you wish to show for each taxonomic level?' --add-entry="Top" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nSummary report is beeing created now ..."

for kingdom in $(echo $sr | sed "s/,/ /g")
do

cd $wd/Results

cp /usr/local/Pipeline/otu_summary.py ./
cp /usr/local/Pipeline/kingdom_table.py ./
python3 kingdom_table.py current_otu_table.txt $kingdom.txt $kingdom &>> $wd/${date}_detailed.log
python3 otu_summary.py $kingdom.txt summary_report_$kingdom.txt $entries 2>> $wd/${date}_detailed.log
rm kingdom_table.py
rm otu_summary.py
rm $kingdom.txt

done

rm current_otu_table.txt &>> $wd/${date}_detailed.log

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nProcess succeeded! (Duration: '$dur's) Summary file(s) created!'
echo -e "\n________________________________________________________________________________\n"

fi

else

taxon=$(zenity --forms --title=$project --text='Please enter the name of the Taxon' --add-entry="Taxon: e.g. Firmicutes" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

entries=$(zenity --forms --title=$project --text='How many taxa do you wish to show for each taxonomic level?' --add-entry="Top" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nSummary report is beeing created now ..."

cd $wd/Results

cp /usr/local/Pipeline/otu_summary.py ./
cp /usr/local/Pipeline/specific_taxon.py ./
python3 specific_taxon.py current_otu_table.txt $taxon 2>> $wd/${date}_detailed.log
python3 otu_summary.py $taxon.txt summary_report_$taxon.txt $entries 2>> $wd/${date}_detailed.log
rm specific_taxon.py
rm otu_summary.py
rm current_otu_table.txt &>> $wd/${date}_detailed.log
rm $taxon.txt

end=$(date +%s)
dur=$(($end-$start))

echo -e '\nProcess succeeded! (Duration: '$dur's) Summary file created!'
echo -e "\n________________________________________________________________________________\n"
fi
fi
fi
fi

#Taxa plots

(zenity --no-wrap --question --title $project --text "Do you want to create plots of the most important taxa?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

(zenity --no-wrap --question --title $project --text "Do you want to use the information in the mapping file to group your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results

cp /usr/local/Pipeline/map_group.py ./
python3 map_group.py otu_table.txt mapping.txt current_otu_table.txt 2>> $wd/${date}_detailed.log
metavar=$(cat metavar.txt)
rm metavar.txt
rm map_group.py

else

cd $wd/Results

cp otu_table.txt ./current_otu_table.txt
metavar="individual"

fi

(zenity --no-wrap --question --title $project --text "Do you want general plots?
Click 'No' for plots of a specific taxon!" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

ki=$(zenity --text "For which kingdom do you want to create the plots?" --title $project --list --checklist --column "" --column "Kingdom" "" "Archaea" "" "Bacteria" "" "Fungi" "" "Eukaryota" "" "Total" --separator="," --height=250 --width=600 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

(zenity --no-wrap --question --title $project --text "Do you want to include unassigned taxa in the plots?" &>> $wd/${date}_detailed.log) && answer="Yes" || answer="No"

if [ $answer = "Yes" ]
then
ass="including_unassigned"
else
ass="without_unassigned"
fi

fformat=$(zenity --text "Please choose a file format:" --title $project --list --column "File format" --column "" "EPS" "Encapsulated Postscript" "JPEG" "Joint Photographic Experts Group" "PDF" "Portable Document Format" "PNG" "Portable Network Graphics" "PS" "Postscript" "RAW" "Raw bitmap" "RGBA" "RGBA bitmap" "SVG" "Scalable Vector Graphics" "SVGZ" "Compressed SVG" "TIFF" "Tagged Image File Format" --separator="," --height=300 --width=400 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $fformat = "JPEG" ] || [ $fformat = "PNG" ] || [ $fformat = "RAW" ] || [ $fformat = "RGBA" ] || [ $fformat = "TIFF" ]
then

params=$(zenity --forms --title=$project --text="Please provide the parameters for the plots:" --add-entry="Threshold [% of reads]" --add-entry="Pixel density [dpi]" 2>> $wd/${date}_detailed.log)

thresh=$(awk -F '[|]' '{print $1}' <<<$params)
dpi=$(awk -F '[|]' '{print $2}' <<<$params)

else
thresh=$(zenity --text "Threshold [% of reads]" --title $project --entry 2>> $wd/${date}_detailed.log)
dpi=100

fi

if [[ $? -ne 1 ]]
then 

start=$(date +%s)

echo -e "\nPlots are beeing created ..."

for kd in $(echo $ki | sed "s/,/ /g")
do

cd $wd/Results

cp /usr/local/Pipeline/kingdom_table.py ./
python3 kingdom_table.py current_otu_table.txt $kd.txt $kd &>> $wd/${date}_detailed.log
rm kingdom_table.py

mkdir -p taxa_plots
cd taxa_plots
mkdir -p $metavar"_"$thresh"%_"$ass
cd $metavar"_"$thresh"%_"$ass

mkdir -p $kd
cd $kd
cp /usr/local/Pipeline/otuplots.py ./
cp ../../../$kd.txt ./
python3 otuplots.py $kd.txt $thresh $fformat $dpi $answer 2>> $wd/${date}_detailed.log
rm otuplots.py
rm $kd.txt

cd $wd/Results

rm $kd.txt

done

rm current_otu_table.txt &>> $wd/${date}_detailed.log

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nProcess succeeded! (Duration: "$dur"s) Plots are created with a threshold of "$thresh"%."
echo -e "\n________________________________________________________________________________\n"
fi
fi
fi

else

tax=$(zenity --forms --title=$project --text='Please enter the name of the Taxon' --add-entry="Taxon: e.g. Firmicutes" 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then 

(zenity --no-wrap --question --title $project --text "Do you want to include unassigned taxa in the plots?" &>> $wd/${date}_detailed.log) && answer="Yes" || answer="No"

if [ $answer = "Yes" ]
then
ass="including_unassigned"
else
ass="without_unassigned"
fi

fformat=$(zenity --text "Please choose a file format:" --title $project --list --column "File format" --column "" "EPS" "Encapsulated Postscript" "JPEG" "Joint Photographic Experts Group" "PDF" "Portable Document Format" "PNG" "Portable Network Graphics" "PS" "Postscript" "RAW" "Raw bitmap" "RGBA" "RGBA bitmap" "SVG" "Scalable Vector Graphics" "SVGZ" "Compressed SVG" "TIFF" "Tagged Image File Format" --separator="," --height=300 --width=400 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $fformat = "JPEG" ] || [ $fformat = "PNG" ] || [ $fformat = "RAW" ] || [ $fformat = "RGBA" ] || [ $fformat = "TIFF" ]
then

params=$(zenity --forms --title=$project --text="Please provide the parameters for the plots:" --add-entry="Threshold [% of reads]" --add-entry="Pixel density [dpi]" 2>> $wd/${date}_detailed.log)

thresh=$(awk -F '[|]' '{print $1}' <<<$params)
dpi=$(awk -F '[|]' '{print $2}' <<<$params)

else
thresh=$(zenity --text "Threshold [% of reads]" --title $project --entry 2>> $wd/${date}_detailed.log)
dpi=100

fi

if [[ $? -ne 1 ]]
then 

start=$(date +%s)
echo -e "\nPlots are beeing created ..."

cd $wd/Results

cp /usr/local/Pipeline/specific_taxon.py ./
python3 specific_taxon.py current_otu_table.txt $tax 2>> $wd/${date}_detailed.log
rm specific_taxon.py

mkdir -p taxa_plots
cd taxa_plots
mkdir -p $metavar"_"$thresh"%_"$ass
cd $metavar"_"$thresh"%_"$ass

mkdir -p $tax
cd $tax
cp /usr/local/Pipeline/otuplots.py ./
cp ../../../$tax.txt ./
python3 otuplots.py $tax.txt $thresh $fformat $dpi $answer 2>> $wd/${date}_detailed.log
rm otuplots.py
rm $tax.txt

cd $wd/Results

rm $tax.txt
rm current_otu_table.txt &>> $wd/${date}_detailed.log

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nProcess succeeded! (Duration: "$dur"s) Plots are created with a threshold of "$thresh"%."
echo -e "\n________________________________________________________________________________\n"

fi
fi
fi
fi
fi

#Venn plots

(zenity --no-wrap --question --title $project --text "Do you want to create Venn plots for comparison of included taxa?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results
mkdir -p Venn_plots
cd Venn_plots

cp /usr/local/Pipeline/venn_plot.py ./
cp ../otu_table.txt ./

if [[ -f "../mapping.txt" ]]
then
python3 venn_plot.py otu_table.txt ../mapping.txt 2>> $wd/${date}_detailed.log
else
python3 venn_plot.py otu_table.txt 2>> $wd/${date}_detailed.log
fi

rm venn_plot.py
rm otu_table.txt

fi

#Alpha diversity

(zenity --no-wrap --question --title $project --text "Do you want to calculate/plot the alpha diversity of your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

metric=$(zenity --text "Please choose a metric for the alpha diversity calculation:" --title $project --list --column "Metric" --column "" "OTU" "Number of distinct OTUs/ASVs/ZOTUs" "Shannon" "Shannon-Wiener index" "Simpson" "Simpson's index" "Pielou" "Pielou's evenness index" "Goods_coverage" "Good's coverage of counts" "Chao1" "Chao1 richness estimator" "Faith_PD" "Faith's phylogenetic diversity" --separator="," --height=300 --width=180 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

(zenity --no-wrap --question --title $project --text "Do you want to use the information in the mapping file to group your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cd $wd/Results
mkdir -p alpha_diversity

cd alpha_diversity
cp /usr/local/Pipeline/alphadiversity_mapped.py ./

if [[ -f "../mapping.txt" ]]
then
python3 alphadiversity_mapped.py ../otu_table.txt $metric ../mapping.txt ../OTUphylo.nwk 2>> $wd/${date}_detailed.log
else
echo -e "\nYou are missing a map file, process terminated!"
echo -e "\n________________________________________________________________________________\n"
fi
rm alphadiversity_mapped.py

else

cd $wd/Results
mkdir -p alpha_diversity

cd alpha_diversity
cp /usr/local/Pipeline/alphadiversity.py ./
python3 alphadiversity.py ../otu_table.txt $metric ../OTUphylo.nwk 2>> $wd/${date}_detailed.log
rm alphadiversity.py

fi
fi
fi

#Beta diversity

(zenity --no-wrap --question --title $project --text "Do you want to calculate/plot the beta diversity of your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

beta=$(zenity --text "How do you want to depict the results of the beta diversity analysis?" --title $project --list --column "" --column "" "PCoA" "Ordination using Principal Coordinates Analysis" "HCA" "Hierarchical Cluster Analysis" --separator="," --height=180 --width=180 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $beta = "PCoA" ]
then

cd $wd/Results
mkdir -p beta_diversity
cd beta_diversity
mkdir -p ordination
cd ordination

metric=$(zenity --text "Please choose a metric for calculating the distance between your samples:" --title $project --list --column "Metric" --column "Remark" "Weighted_unifrac" "Phylogeny based metric - suggested for microbiome data" "Unweighted_unifrac" "Phylogeny based metric - suggested for microbiome data" "Minkowski" "Requires a p-norm (1, 2, 3, ...)" "Euclidean" "Corresponds to Minkowski distance with p = 2" "Manhattan" "Corresponds to Minkowski distance with p = 1" "Cosine" "" "Jaccard" "For presence/absence data - suggested for microbiome data" "Dice" "For presence/absence data" "Canberra" "" "Chebyshev" "Corresponds to Minkowski distance with infinitely high p" "Braycurtis" "Suggested for microbiome data" --separator="," --height=380 --width=280 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $metric = "Weighted_unifrac" ] || [ $metric = "Unweighted_unifrac" ]
then

(zenity --no-wrap --question --title $project --text "Do you want to use metadata from the mapping file in order to color your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cp /usr/local/Pipeline/ordination_mapped.py ./
python3 ordination_mapped.py ../../otu_table.txt $metric ../../mapping.txt ../../OTUphylo.nwk 2>> $wd/${date}_detailed.log
rm ordination_mapped.py

else

cp /usr/local/Pipeline/ordination.py ./
python3 ordination.py ../../otu_table.txt $metric ../../OTUphylo.nwk 2>> $wd/${date}_detailed.log
rm ordination.py

fi

elif [ $metric = "Minkowski" ]

then

p=$(zenity --text "P-norm:" --title $project --entry 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

(zenity --no-wrap --question --title $project --text "Do you want to use meta data from the mapping file in order to color your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cp /usr/local/Pipeline/ordination_mapped.py ./
python3 ordination_mapped.py ../../otu_table.txt $metric ../../mapping.txt $p 2>> $wd/${date}_detailed.log
rm ordination_mapped.py

else

cp /usr/local/Pipeline/ordination.py ./
python3 ordination.py ../../otu_table.txt $metric $p 2>> $wd/${date}_detailed.log
rm ordination.py

fi
fi

else

(zenity --no-wrap --question --title $project --text "Do you want to use meta data from the mapping file in order to color your samples?" &>> $wd/${date}_detailed.log) && shell="Yes" || shell="No"

if [ $shell = "Yes" ]
then

cp /usr/local/Pipeline/ordination_mapped.py ./
python3 ordination_mapped.py ../../otu_table.txt $metric ../../mapping.txt 2>> $wd/${date}_detailed.log
rm ordination_mapped.py

else

cp /usr/local/Pipeline/ordination.py ./
python3 ordination.py ../../otu_table.txt $metric 2>> $wd/${date}_detailed.log
rm ordination.py

fi
fi
fi

else
meth=$(zenity --text "Please choose a method for the HCA:" --title $project --list --column "Method" --column "Alternative name" "single" "Minimum" "complete" "Maximum" "average" "UPGMA" "weighted" "WPGMA" "centroid" "UPGMC" "median" "WPGMC" "ward" "Incremental" --separator="," --height=280 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $meth = "centroid" ] || [ $meth = "median" ] || [ $meth = "ward" ]
then

metr="euclidean"

else 

metr=$(zenity --text "Please choose a metric for measuring the distance between points:" --title $project --list --column "Metric" "euclidean" "cosine" "cityblock" "correlation" "jaccard" "braycurtis" "dice" --separator="," --height=280 --width=180 2>> $wd/${date}_detailed.log)

fi

if [[ $? -ne 1 ]]
then

(zenity --no-wrap --question --title $project --text "Do you want to plot the distance of each node in the dendrogram?" &>> $wd/${date}_detailed.log) && anno="Yes" || anno="No"

fformat=$(zenity --text "Please choose a file format:" --title $project --list --column "File format" --column "" "EPS" "Encapsulated Postscript" "JPEG" "Joint Photographic Experts Group" "PDF" "Portable Document Format" "PNG" "Portable Network Graphics" "PS" "Postscript" "RAW" "Raw bitmap" "RGBA" "RGBA bitmap" "SVG" "Scalable Vector Graphics" "SVGZ" "Compressed SVG" "TIFF" "Tagged Image File Format" --separator="," --height=300 --width=400 2>> $wd/${date}_detailed.log)

if [[ $? -ne 1 ]]
then

if [ $fformat = "JPEG" ] || [ $fformat = "PNG" ] || [ $fformat = "RAW" ] || [ $fformat = "RGBA" ] || [ $fformat = "TIFF" ]
then

dpi=$(zenity --text "Pixel density [dpi]" --title $project --entry 2>> $wd/${date}_detailed.log)

else
dpi=100

fi

if [[ $? -ne 1 ]]
then

start=$(date +%s)

echo -e "\nCluster analysis proceeding ..."

cd $wd/Results
mkdir -p beta_diversity
cd beta_diversity
mkdir -p cluster_analysis
cd cluster_analysis

cp /usr/local/Pipeline/cluster.py ./
cp /usr/local/Pipeline/create_shared_file.py ./
python3 create_shared_file.py ../../otu_table.txt otu.shared &>> $wd/${date}_detailed.log
python3 cluster.py otu.shared $meth $metr $anno $fformat $dpi 2>> $wd/${date}_detailed.log
rm cluster.py
rm create_shared_file.py
rm otu.shared

end=$(date +%s)
dur=$(($end-$start))

echo -e "\nProcess succeeded! Dendrogram created! (Duration: "$dur"s)"
echo
echo "Clustering method: " $meth
echo "Clustering metric: " $metr
echo -e "\n________________________________________________________________________________\n"
fi
fi
fi
fi
fi
fi
fi

zenity --no-wrap --text "Thank you for using CoMA, the NGS analysis pipeline! 

(C) 2020 
Sebastian Hupfauf
Mohammad Etemadi" --title $project --info &>> $wd/${date}_detailed.log

