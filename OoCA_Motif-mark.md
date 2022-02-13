Classes:
1. Motif class
    a. parse_motif_file - make a dictionary of all the motifs as keys and the values being a list of all the possibilities of that motif

    b. motif_possibilities - take a motif and return a list of all the possibilities


2. Fasta Class
    a. parse_fasta - for each record in the fasta, make a dictionary with the key the motif and the value a list of the start and ending locations of that motif. pass that dict to drawing class to draw it


3. Drawing Class
    a. draw_surface - take the number of seqeuences (n) in and create a surface n times the size of one box (300 x 100?) 

    b. draw_hor_lines - draw the horizontal like accross each box

    c. draw_exons - draw the exon boxes

    d. draw motif lines - using the list of locations, draw the motif lines of the correct width on the box. take care of the overlapping problem here

    e. make_key - make a key and add a title to the box
