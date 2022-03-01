#!/usr/bin/env python

import cairo
import math

#create surface
surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 200)

#create context
context = cairo.Context(surface)

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



