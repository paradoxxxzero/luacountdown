#! /usr/bin/env lua
--[[
  Lua countdown - A lua cairo countdown

  Copyright (C) 2010 Mounier Florian aka paradoxxxzero

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see http://www.gnu.org/licenses/.
--]]

require("lgob.gtk")
require("lgob.gdk")
require("lgob.cairo")

gtk.Countdown = {}
setmetatable(gtk.Countdown, {__index = gtk.DrawingArea})

local width, heigth = 100, 100
local step = 10
local val = 99
local inc = 100

---
-- Constructor of the countdown
--
function gtk.Countdown.new()
	local obj = gtk.DrawingArea.new()
	obj:cast(gtk.Countdown)
	glib.timeout_add(glib.PRIORITY_HIGH_IDLE, 10, gtk.Countdown.paint, obj)
	obj:connect("expose-event", gtk.Countdown.expose, obj)
	return obj;
end

---
-- Expose even callback
function gtk.Countdown:expose()
	local cr = gdk.cairo_create(self:get_window())
	local size = (math.min(self:get_size()) / 2)
	local mt = getmetatable(self)
	cr:set_line_width(3)

	inc = inc - 1
	if inc == 0 then
	   inc = 100
	   val = val - 1
	   if val == 0 then
	      gtk.main_quit()
	   end
	end

	cr:set_source_rgb(0, 0, 0)
	cr:rectangle(0, 0, width, heigth)
	cr:fill()

	cr:set_source_rgba(0, 0.4, 1, 0.8)
	cr:arc(50, 50, 40, 0, 2 * math.pi)
	cr:stroke()

	cr:set_source_rgba(0.2, 0.8, 1, 0.8)
	cr:arc(50, 50, 40, 0, 2 * math.pi * inc / 100 )
	cr:stroke()


	cr:move_to(25, 65)
	cr:set_font_size(40)
	cr:show_text(val)

end

---
-- Timeout callback
function gtk.Countdown:paint()
	self:queue_draw()
	return true
end


local window = gtk.Window.new(gtk.WINDOW_TOPLEVEL)
local box    = gtk.HBox.new(true, 20)
local cd = gtk.Countdown.new()

window:set("title", "Countdown Widget", "window-position", gtk.WIN_POS_CENTER)
window:connect("delete-event", gtk.main_quit)
window:set("width-request", width, "height-request", heigth)
window:set("opacity", 0.75)
window:set("resizable", false)

box:add(cd)
window:add(box)
window:show_all()
gtk.main()
