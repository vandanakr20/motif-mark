#!/usr/bin/env python

import argparse
import cairo
import itertools

'''
1. Fasta Class
    a. parse_seq - for each motif instance, loop through the sequence and find all the starting locations of all the possibilities

2. Drawing Class
    a. draw_surface - take the number of seqeuences (n) in and create a surface n times the size of one box (300 x 100?) 

    b. draw_hor_lines - draw the horizontal like accross each box

    c. draw_exons - draw the exon boxes

    d. draw motif lines - using the list of locations, draw the motif lines of the correct width on the box. take care of the overlapping problem here

    e. make_key - make a key and add a title to the box
'''

# case does not matter in motif file 
# lower case - intron 
# upper case - exon


#argparse

# use argparse to get user input of the file names, if the data is paired, and $
def get_args():
    parse = argparse.ArgumentParser(description="A program to visualize motifs within a sequence")
    parse.add_argument("-f", "--fasta_file", required = True, help="fasta file with sequences")
    parse.add_argument("-m", "--motif_file", required = True, help="text file with motifs")
    return parse.parse_args()

args = get_args()

class Motif:
    #make the name of the motif object the motif as it is in the motif file
    def __init__(self, mot_string):
        self.motif = mot_string.upper()
        self.indv_list = list()
        self.inter_list = list()
        self.poss_list = list()

    ## Methods ##
    def make_poss_list(self):
        nuc_list = list()
        for i in self.motif:
            nuc_list = list()
            if i == 'A' or i == 'C' or i == 'G' or i == 'T':
                nuc_list.append(i)
                #print('nuc')
            elif i == 'Y':
                nuc_list.append('C')
                nuc_list.append('T')
            elif i == 'R':
                nuc_list.append('A')
                nuc_list.append('G')
            self.indv_list.append(nuc_list)

        # need * to unpack the list
        self.inter_list = list(itertools.product(*self.indv_list))
        for i in self.inter_list:
            mot_str= ''
            for element in i:
                mot_str += str(element)
            self.poss_list.append(mot_str)
        #print(len(self.poss_list))

# motif class test
mot1 = Motif('YYYYYYYYYY')
mot1.make_poss_list()



class Gene:
    #make the name of the gene object the header until the first space without the >
    def __init__(self, header, seq):
        self.header = header
        self.seq = seq

    ## Methods ##
    #def make_poss_list(self):



class Pycairo:
  def __init__(self, num_fasta, num_motif): #this is how you actually make the attributes of the class
    ## Data ##
    self.num_fasta = num_fasta
    self.num_motif = num_motif

    ## Methods ##
    def create_surface(self, num_fasta):
        num = num_fasta * 300
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, num, 200)
        context = cairo.Context(surface)

    def create_background(self, surface, context):
        #color the background
        context.rectangle(0, 0, 300, 200) 
        context.set_source_rgb(.76, 1.00, .76)
        context.fill()

        #draw line
        context.move_to(0,100)
        context.line_to(300, 100)
        context.set_source_rgb(1, 0, 0)
        context.set_line_width(10)
        context.stroke()

        #draw a rectangle       #(x0,y0,x1,y1)
        context.rectangle(50, 50, 200, 100)
        context.set_source_rgb(.16, .56, .51)
        context.fill()



        #create png output
        surface.write_to_png('prettypicture.png')


motif_dict = {}
with open(args.motif_file, 'r') as fh:
    for line in fh:
        motif_dict[line.strip()] = Motif(line.strip())
#print(motif_dict)

seq_dict = {}
seq_str = ''
name = ''
with open(args.fasta_file, 'r') as fh2:
    for line in fh2:
        if line.startswith('>'):
            if name != '':
                seq_dict[name] = Gene(name, seq_str) #shorten the name in the key
            seq_str = ''
            name = line.strip('/n')
        else:
            seq_str += line.strip('/n')

print(seq_dict)