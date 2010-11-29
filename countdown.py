# !/usr/bin/env python2
# coding: utf8

############################################################################
# Lua countdown python version                                             #
#                                                                          #
# Copyright (C) 2010 Mounier Florian aka paradoxxxzero                     #
#                                                                          #
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or any later version.                                           #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see http://www.gnu.org/licenses/.      #
############################################################################

import gtk
import gobject
import math

w = 100
h = 100
step = 10

class Countdown(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        self.inc = 100
        self.val = 99
        
    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
        self.draw(self.context)
        return False
    
    def draw(self, context):
	context.set_line_width(3)
	self.inc = self.inc - 1
	if self.inc == 0:
            self.inc = 100
            self.val = self.val - 1
            if self.val == 0:
                gtk.main_quit()
                
        context.set_source_rgb(0, 0, 0)
	context.rectangle(0, 0, w, h)
	context.fill()

	context.set_source_rgba(0, 0.4, 1, 0.8)
	context.arc(50, 50, 40, 0, 2 * math.pi)
	context.stroke()

	context.set_source_rgba(0.2, 0.8, 1, 0.8)
	context.arc(50, 50, 40, 0, 2 * math.pi * self.inc / 100 )
	context.stroke()

	context.move_to(50 - (25 * (len(str(self.val)) / 2)), 65)
	context.set_font_size(40)
	context.show_text(str(self.val))

def timeout(cd):
    cd.queue_draw()
    return True

def main():
    window = gtk.Window()
    cd = Countdown()
    
    window.add(cd)
    window.set_title("Countdown Widget")
    window.set_size_request(w, h)
    window.set_opacity(0.75)
    window.set_resizable(False)
    window.stick()
    window.set_keep_below(True)
    window.connect("destroy", gtk.main_quit)
    window.show_all()
    gobject.timeout_add(step, timeout, cd)
    gtk.main()

    
if __name__ == "__main__":
    main()
