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

#draw a rectangle       #(x0,y0,x1,y1)
context.rectangle(25, 50, 70, 120)
context.set_source_rgb(.16, .56, .51)
context.fill()

#draw line
context.move_to(100, 110)
context.line_to(250, 110)
context.set_source_rgb(1, 0, 0)
context.set_line_width(10)
context.stroke()

#create png output
surface.write_to_png('prettypicture.png')



