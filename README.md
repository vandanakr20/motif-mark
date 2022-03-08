# Motif-Mark

Motif-Mark is a python program used to visualize motifs on sequences. This program takes in a fasta file and a txt file with motifs, and creates an image with the all motif locations on each sequence depicted as a png. Exons are depicted with rectangles and motifs with lines. Overlapping motifs will show up darker on the image if there are mutlple motifs. 

Usage: ./motif-mark-oop.py -f [Fasta File] -m [Motif File]

Requirements:
1. The absolute paths to the Fasta and Motif files are needed. 
2. This program can handle one fasta file with any number of sequences with one exon each and one motif file with up to 5 motifs. 

Example Output: <img width="1149" alt="Screen Shot 2022-03-07 at 9 12 47 PM" src="https://user-images.githubusercontent.com/83670690/157170619-97d37cf3-ac93-445a-9882-480b46087bb5.png">


