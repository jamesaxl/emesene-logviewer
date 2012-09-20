# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-130
from gi.repository import Gtk
import os
import json

class MenuBar(Gtk.MenuBar):
    def __init__(self, get_session, fill_contact_list, 
        show_widget, unload, _about):

        Gtk.MenuBar.__init__(self)
        conf_path = "%s/.config/emesene2/config" %os.getenv("HOME")
        data = json.load(open(conf_path))
        accounts = data[11][1]
        self.get_session = get_session
        self.fill_contact_list = fill_contact_list
        self.show_widget = show_widget
        self.unload = unload
        self._about = _about
        self.filemenu = Gtk.Menu()
        self.helpmenu = Gtk.Menu()
        filem = Gtk.MenuItem("File")
        filem.set_submenu(self.filemenu)
        helpm = Gtk.MenuItem("Help")
        helpm.set_submenu(self.helpmenu)
        
        self.unload_item = Gtk.MenuItem("Unload")
        self.unload_item.connect("activate", self.unload, self.filemenu)
        exit = Gtk.MenuItem("Exit")
        exit.connect("activate", Gtk.main_quit)
        about = Gtk.MenuItem("About")
        about.connect("activate", self._about)

        self.filemenu.append(exit)
        self.helpmenu.append(about)
        self.append(filem)
        self.append(helpm)