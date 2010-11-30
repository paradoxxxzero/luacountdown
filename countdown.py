# !/usr/bin/env python
# -*- coding: utf8 -*-

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
import cairo

w = 100
h = 100
step = 10

class Countdown(gtk.DrawingArea):
  def __init__(self):
    gtk.DrawingArea.__init__(self)
    self.connect("expose_event", self.expose)
    self.inc = 100
    self.val = 19

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

    context.set_source_rgba(1, 1, 1, 0)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()

    context.set_source_rgba(0, 0, 0, 1)
    context.arc(50, 50, 40, 0, 2 * math.pi)
    context.fill()

    context.set_source_rgba(0, 0.4, 1, 0.8)
    context.arc(50, 50, 40, 0, 2 * math.pi)
    context.stroke()

    context.set_source_rgba(0.2, 0.8, 1, 0.8)
    context.arc(50, 50, 40, 0, 2 * math.pi * self.inc / 100 )
    context.stroke()

    context.move_to(50 - (25 * len(str(self.val)) / 2), 65)
    context.set_font_size(40)
    context.show_text(str(self.val))

def timeout(cd):
  cd.queue_draw()
  return True

def transparent_expose(widget, event):
  cr = widget.window.cairo_create()
  cr.set_operator(cairo.OPERATOR_CLEAR)
  region = gtk.gdk.region_rectangle(event.area)
  cr.region(region)
  cr.fill()
  return False

def main():
  window = gtk.Window()
  cd = Countdown()
  window.add(cd)
  window.set_title("Countdown Widget")
  window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
  window.set_skip_taskbar_hint(True)
  window.set_skip_pager_hint(True)
  window.set_keep_below(True)
  window.set_decorated(False)
  window.stick()
  window.set_position(gtk.WIN_POS_CENTER)
  colormap = window.get_screen().get_rgba_colormap()
  if colormap == None:
    print 'Your screen does not support alpha channels.'
    colormap = window.get_screen().get_rgb_colormap()
  window.set_colormap(colormap)
  window.set_app_paintable(True)
  window.connect("expose-event", transparent_expose)
  window.set_size_request(w, h)
  window.set_double_buffered(True)
  window.connect("destroy", gtk.main_quit)
  window.show_all()
  gobject.timeout_add(step, timeout, cd)
  gtk.main()


if __name__ == "__main__":
  main()
