#!/usr/bin/env python

import argparse
import cairo
import re

# case does not matter in motif file 
# lower case - intron 
# upper case - exon

# use argparse to get user input of the fasta and motif file names
def get_args():
    parse = argparse.ArgumentParser(description="A program to visualize motifs within a sequence")
    parse.add_argument("-f", "--fasta_file", required = True, help="absolute path to fasta file with sequences")
    parse.add_argument("-m", "--motif_file", required = True, help="absolute path to text file with motifs")
    return parse.parse_args()

args = get_args()


#################################################################################################
# CLASS DECLARATIONS                                                                            #
#################################################################################################

# motif class - each motif will be an instance of this class
class Motif:
    #pass each motif and make an instance of the motif class with 2 attributes, the actual motif name and the motif name editted for Ambiguous nucleotide motifs
    def __init__(self, mot_string):
        self.true_motif_name = mot_string
        self.motif_name = mot_string.upper()

    #create a regex expression for the motif to look through sequences with
    def make_motif_poss(self):
        mot = self.motif_name
        mot = mot.replace('Y', '[CTU]')
        mot = mot.replace('R', '[AG]')
        mot = mot.replace('W', '[AT]')
        mot = mot.replace('S', '[CG]')
        mot = mot.replace('M', '[AC]')
        mot = mot.replace('K', '[GT]')
        mot = mot.replace('B', '[CGT]')
        mot = mot.replace('D', '[AGT]')
        mot = mot.replace('H', '[ACT]')
        mot = mot.replace('V', '[ACG]')
        mot = mot.replace('N', '[ACGT]')
        self.motif_name = mot


# gene class - each sequence will be an instance of this class
class Gene:
    #pass each sequence and make an instance of the sequence class with 4 attributes, the header, the sequence, a dictionary of motif locations, and a list of starting and ending exon positions
    def __init__(self, header, seq):
        self.header = header
        self.seq = seq
        self.motif_locs = {}   #key: motif, value: list of starting and ending positions
        self.exon_pos = list()   #start and ending position of the exon 

    ## Methods ##
    #find all the motif matches in the sequence and add it to the dictionary with the motifs as the keys
    def find_motif_locs(self, motif):
        match_list = list()
        p = re.finditer(motif.motif_name, self.seq.upper())
        for match in p:
            match = match.span()
            match_list.append(match)
        self.motif_locs[motif.true_motif_name] = match_list

    #find the exon in the sequence denoted with capital letters. Only finds one exon
    def find_exon(self):
        for i,nuc in enumerate(self.seq):
            if nuc.isupper():
                self.exon_pos.append(i)
            else: #lower case
                continue
        self.exon_pos = [self.exon_pos[0], self.exon_pos[-1]]

# pycairo class - each image is an instance of the class
class Pycairo_draw:
    def __init__(self, motif_dict, seq_dict, color_list): 
        #pass all of the motif objects in a dict and all of the sequence objects in a dict along with the list of colors to use. Use those variables as the 3 attributes of the class
        self.motif_dict = motif_dict
        self.seq_dict = seq_dict
        self.color_list = color_list

    ## Methods ##
    #draw the figure using Pycairo
    def create_figure(self):   
        #create the surface as 900 x 100*number of sequences
        num_seq = len(self.seq_dict)
        size = num_seq * 100
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 900, size)
        context = cairo.Context(surface)

        #color the background black
        context.rectangle(0, 0, 900, size) 
        context.set_source_rgb(0, 0, 0)
        context.fill()

        #starting at x postion 60, draw lines for each sequence based on the length of the sequence
        y_add = 60
        for motif, seq in self.seq_dict.items():
            context.move_to(70 ,y_add)
            context.line_to((len(seq.seq)+70), y_add)
            context.set_source_rgba(0.5, 0.5, 0.5, 0.5) 
            context.set_line_width(2)
            context.stroke()
            y_add += 100

        #draw rectangle of size 50 starting at the start of the exon and ending as the end of the exon
        start_y = 35
        for seqvalue in self.seq_dict.values():
            start_x = (seqvalue.exon_pos[0] + 70)
            end_x = ((seqvalue.exon_pos[1]-seqvalue.exon_pos[0]))
            context.rectangle(start_x, start_y, end_x , 50)
            context.set_source_rgba(0.5, 0.5, 0.5, .4)
            context.fill()
            start_y += 100

        #add the motifs to the surface for a total size of 30
        y_start = 45
        y_end = 75
        for seqvalue in self.seq_dict.values():
            i = 0
            #make each motif a different color
            for motif, locs in seqvalue.motif_locs.items():
                for one_loc in locs:
                    start = one_loc[0]+70
                    context.move_to(start , y_start)
                    context.line_to(start, y_end)
                    # make transparent to see overlapping motifs
                    context.set_source_rgba(self.color_list[i][0],self.color_list[i][1],self.color_list[i][2], 0.5)
                    context.set_line_width(len(motif)-2)
                    context.stroke()
                i += 1
            y_start += 100
            y_end += 100

        #add the labels for each one of the sequences from the headers of the fasta file 
        y2 = 26
        for seqvalue in self.seq_dict.values():
            context.set_source_rgb(1, 1, 1)
            context.set_font_size(13)
            context.move_to(70, y2)
            context.show_text(seqvalue.header[1:])
            y2 += 100

            #create legend
            y = 45
            #create rectangles of each color of each motif
            for key in self.motif_dict.keys():
                context.set_source_rgb(1, 1, 1) 
                context.set_font_size(12)
                context.move_to(750, y)
                context.show_text(key.upper())
                y += 30
            
            #add motif names next to the rectangles to finish the key 
            y = 35
            for i in range(len(self.motif_dict)):
                context.rectangle(730, y, 10 , 10)
                context.set_source_rgb(self.color_list[i][0],self.color_list[i][1],self.color_list[i][2])
                context.fill()
                y += 30

        #get the name of the fasta file from the full path and name the .png file with the same prefixs
        name = args.fasta_file.partition('.')[0]
        file_name = name.split('/')[-1]
        file_name = file_name + '.png'
        surface.write_to_png(file_name)


#################################################################################################
# main                                                                                          #
#################################################################################################

#define motif dict with the keys as the name of the motif and the object as the value
motif_dict = {}
with open(args.motif_file, 'r') as fh:
    for line in fh:
        motif_dict[line.strip()] = Motif(line.strip())


#define seq dict with the keys as the sequence header and the object as the value
seq_dict = {}
seq_str = ''
name = ''
with open(args.fasta_file, 'r') as fh2:
    for line in fh2:
        if line.startswith('>'):
            if name != '':
                seq_dict[name.strip('\n')] = Gene(name.strip('\n'), seq_str.strip('\n')) 
            seq_str = ''
            name = line.strip('\n')
        else:
            seq_str += line.strip('\n')
    seq_dict[name.strip('\n')] = Gene(name.strip('\n'), seq_str.strip('\n')) 

#run motif method
for motifkey, motifvalue in motif_dict.items():
    motifvalue.make_motif_poss()

#run seq methods
for seqkey, seqvalue in seq_dict.items():
    seqvalue.find_exon()
    for motifkey, motifvalue in motif_dict.items():
        seqvalue.find_motif_locs(motifvalue)


#create the list of colors 
color_list = list()
color_list.append((0.4,0.7,1)) #blue
color_list.append((0.8,0.3,0.9)) #purple
color_list.append((1,0.2,0)) #red
color_list.append((1,1,0)) #yellow
color_list.append((0.9,0.5,0)) # orange

#run the pycairo methods to draw the images
figure1 = Pycairo_draw(motif_dict, seq_dict, color_list)
figure1.create_figure()