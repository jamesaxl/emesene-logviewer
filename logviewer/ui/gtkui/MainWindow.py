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
from MenuBar import MenuBar
from ContactList import ContactList
from Viewer import Viewer
import os

class MainWindow(Gtk.Window):

    def __init__(self, get_session, get_chat):
        Gtk.Window.__init__(self, title="emesene log viewer")
        self.get_session = get_session
        self.get_chat = get_chat
        self.connect("delete-event", Gtk.main_quit)
        self.resize(300,500)
        self.image = Gtk.Image()
        self.image.set_from_file("logviewer/icons/logo.png")
        self.image.xalign = 0.5
        self.image.yalign = 0.5

        view = Viewer()
        contacts = ContactList(view.load_contact_log, self.get_chat)
        mb = MenuBar(self.get_session, contacts.fill_contact_list, 
            self.show_widget, self.unload)

        scroll_view = Gtk.ScrolledWindow()
        scroll_contact = Gtk.ScrolledWindow()

        scroll_view.set_border_width(1)
        scroll_contact.set_border_width(1)
 
        scroll_view.add(view)
        scroll_contact.add(contacts)
        self.hpaned = Gtk.HPaned()
        self.hpaned.add1(scroll_contact)
        self.hpaned.add2(scroll_view)
        self.hpaned.set_position(250)
        self.vbox = Gtk.VBox(False, 2)
        self.vbox.pack_start(mb, False, False, 1)
        self.vbox.add(self.image)
        self.add(self.vbox)
        self.show_all()

    def show_widget(self):
        self.vbox.pack_start(self.hpaned, True, True,5)
        self.vbox.remove(self.image)
        self.show_all()
        self.resize(850,530)

    def unload(self, item, filemenu):
        self.vbox.remove(self.hpaned)
        self.vbox.add(self.image)
        filemenu.remove(item)
        self.resize(300,530)