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
    parse.add_argument("-f", "--fasta_file", required = True, help="fasta file with sequences")
    parse.add_argument("-m", "--motif_file", required = True, help="text file with motifs")
    return parse.parse_args()

args = get_args()

# motif class - each motif will be an instance of this class
class Motif:
    #make the name of the motif object the motif as it is in the motif file
    def __init__(self, mot_string):
        self.true_motif_name = mot_string
        self.motif_name = mot_string.upper()
        self.mot_length = len(self.motif_name)

    ## Methods ##
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




class Gene:
    #make the name of the gene object the header until the first space without the >
    def __init__(self, header, seq):
        self.header = header
        self.seq = seq
        self.motif_locs = {}
        #self.intron_pos = list()
        self.exon_pos = list() #start and ending position of the exon 
        self.motif_length = 0

    ## Methods ##
    def find_motif_locs(self, motif):
        match_list = list()
        p = re.finditer(motif.motif_name, self.seq.upper())
        for match in p:
            match = match.span()
            match_list.append(match)
        self.motif_locs[motif.true_motif_name] = match_list
        self.motif_length = (motif.mot_length)
        #print(self.motif_locs)

    def find_exon(self):
        for i,nuc in enumerate(self.seq):
            if nuc.isupper():
                self.exon_pos.append(i)
            else: #lower case
                continue
        self.exon_pos = [self.exon_pos[0], self.exon_pos[-1]]
        #print(self.exon_pos)

    # def find_intron(self):
    #     self.intron_pos.append(0)
    #     self.intron_pos.append((self.exon_pos[0]-1))
    #     self.intron_pos.append((self.exon_pos[1]+1))
    #     self.intron_pos.append((len(self.seq)-1))
    #     #print(self.intron_pos)

# gene class test
# gene1 = Gene('name', 'cccAAAccAAAc')
# gene1.find_exon()
# gene1.find_intron()
# gene1.find_motif_locs(mot1)


class Pycairo_draw:
    def __init__(self, motif_dict, seq_dict, color_list): #this is how you actually make the attributes of the class
    ## Data ##
        self.motif_dict = motif_dict
        self.seq_dict = seq_dict
        self.color_list = color_list

    ## Methods ##
    def create_figure(self):   
    #draw the cairo shit
        num_seq = len(self.seq_dict)
        size = num_seq * 100
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 900, size)
        context = cairo.Context(surface)

        #color the background
        context.rectangle(0, 0, 900, size) 
        context.set_source_rgb(0, 0, 0)
        context.fill()
 
        y_add = 60
        for motif, seq in self.seq_dict.items():
            #draw line
            context.move_to(70 ,y_add)
            context.line_to((len(seq.seq)+70), y_add)
            #print(len(seq.seq))
            context.set_source_rgba(0.5, 0.5, 0.5, 0.5) 
            context.set_line_width(2)
            context.stroke()
            y_add += 100

        #draw rectangle 
        start_y = 35
        for seqkey, seqvalue in self.seq_dict.items():
            #draw a rectangle       #(x0,y0,length,width)
            print(seqvalue.exon_pos)
            start_x = (seqvalue.exon_pos[0] + 70)
            print(start_x)
            end_x = ((seqvalue.exon_pos[1]-seqvalue.exon_pos[0]))
            print(end_x)
            context.rectangle(start_x, start_y, end_x , 50)
            context.set_source_rgba(0.5, 0.5, 0.5, .4)
            context.fill()
            start_y += 100

        y_start = 45
        y_end = 75

        for seqvalue in self.seq_dict.values():
            #print(seqvalue.motif_locs)
            i = 0
            for motif, locs in seqvalue.motif_locs.items():
                for one_loc in locs:
                    print(one_loc)
                    start = one_loc[0]+70
                    context.move_to(start , y_start)
                    context.line_to(start, y_end)
                    context.set_source_rgba(self.color_list[i][0],self.color_list[i][1],self.color_list[i][2], 0.5)
                    context.set_line_width(len(motif)-2)
                    context.stroke()
                i += 1
            y_start += 100
            y_end += 100

        y2 = 26
        for seqvalue in self.seq_dict.values():
            context.set_source_rgb(1, 1, 1)
                
            #context.select_font_face("sans-serif")
            context.set_font_size(13)
                
            context.move_to(70, y2)
            context.show_text(seqvalue.header[1:])
            y2 += 100

        #create legend
            y = 45
            for key in self.motif_dict.keys():
                context.set_source_rgb(1, 1, 1) 
                #gitcontext.select_font_face("sans-serif")
                context.set_font_size(12)
                context.move_to(750, y)
                context.show_text(key.upper())
                y += 30

            y = 35
            for i in range(len(self.motif_dict)):
                context.rectangle(730, y, 10 , 10)
                context.set_source_rgb(self.color_list[i][0],self.color_list[i][1],self.color_list[i][2])
                context.fill()
                y += 30


        surface.write_to_png('prettypic.png')


#################################################################################################
# main                                                                                          #
#################################################################################################

#define motif dict
motif_dict = {}
with open(args.motif_file, 'r') as fh:
    for line in fh:
        motif_dict[line.strip()] = Motif(line.strip())
#print(motif_dict)

#define seq dict
seq_dict = {}
seq_str = ''
name = ''
with open(args.fasta_file, 'r') as fh2:
    for line in fh2:
        if line.startswith('>'):
            if name != '':
                seq_dict[name.strip('\n')] = Gene(name.strip('\n'), seq_str.strip('\n')) #shorten the name in the key
            seq_str = ''
            name = line.strip('\n')
        else:
            seq_str += line.strip('\n')
    seq_dict[name.strip('\n')] = Gene(name.strip('\n'), seq_str.strip('\n')) #shorten the name in the key
#print(seq_dict)

#run motif method
for motifkey, motifvalue in motif_dict.items():
    motifvalue.make_motif_poss()

#run seq methods
for seqkey, seqvalue in seq_dict.items():
    seqvalue.find_exon()
    for motifkey, motifvalue in motif_dict.items():
        seqvalue.find_motif_locs(motifvalue)
    #print(seqkey, seqvalue.motif_locs)


color_list = list()
color_list.append((0.4,0.7,1)) #blue
color_list.append((0.8,0.3,0.9)) #purple
color_list.append((1,0.2,0)) #red
color_list.append((1,1,0)) #yellow
color_list.append((0.9,0.5,0)) # orange
#print(color_list)

figure1 = Pycairo_draw(motif_dict, seq_dict, color_list)
figure1.create_figure()