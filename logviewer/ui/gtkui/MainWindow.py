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
from Login import Login
import os

class MainWindow(Gtk.Window):

    def __init__(self, get_session, get_chat):
        Gtk.Window.__init__(self, title="emesene log viewer")
        self.get_session = get_session
        self.get_chat = get_chat
        self.connect("delete-event", Gtk.main_quit)
        self.resize(300,500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.hpaned = Gtk.HPaned()
        view = Viewer()
        self.scroll_view = Gtk.ScrolledWindow()
        self.scroll_view.set_border_width(1)
        self.scroll_view.add(view)
        img_remove = Gtk.Image()
        img_remove.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        self.b_remove = Gtk.Button()
        self.b_remove.set_image(img_remove)
        self.b_alig = Gtk.Alignment(xalign=1, yalign=1, xscale=0.0, yscale=1.0)
        self.b_alig.add(self.b_remove)
        self.b_remove.connect('clicked', self._clicked) 
        self.view_box = Gtk.VBox(False,1)
        self.view_box.set_border_width(8)
        self.view_box.pack_start(self.b_alig, False, False, 1)
        self.view_box.pack_start(self.scroll_view, True, True, 1)

        contacts = ContactList(view.load_contact_log, self.get_chat, self.hpaned, self.view_box, self.resize)
        mb = MenuBar(self.get_session, contacts.fill_contact_list, 
            self.show_widget, self.unload, self._about)

        self.login = Login(self.get_session, contacts.fill_contact_list,
            self.show_widget, self.unload, mb.filemenu, mb.unload_item)

        scroll_contact = Gtk.ScrolledWindow()

        scroll_contact.set_border_width(1)
 
        scroll_contact.add(contacts)
        self.hpaned.add1(scroll_contact)
        self.hpaned.set_position(250)
        self.vbox = Gtk.VBox(False, 7)

        self.vbox.pack_start(mb, False, False, 1)
        self.vbox.pack_start(self.login, False, False, 10)
        self.add(self.vbox)
        self.show_all()

    def show_widget(self):
        self.vbox.remove(self.login)
        self.vbox.pack_start(self.hpaned, True, True,5)
        if self.hpaned.get_child2():
            self.hpaned.remove(self.view_box)
        self.resize(300,530)
        self.show_all()

    def unload(self, item, filemenu):
        self.vbox.remove(self.hpaned)
        self.vbox.pack_start(self.login, False, False, 10)
        filemenu.remove(item)
        self.resize(300,530)

    def _clicked(self, clicked = None):
        self.hpaned.remove(self.view_box)
        self.resize(300,530)

    def _about(self, about):
        dialog = Gtk.Dialog("About", self, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_default_size(300, 100)
        image = Gtk.Image()
        image.set_from_file("logviewer/icons/logo.png")
        title = Gtk.Label()
        title.set_markup("<big><b>emesene-logviewer</b></big>")
        disc = Gtk.Label()
        disc.set_markup("A simple tool to browse in chat history")
        authors = Gtk.Label()
        authors.set_markup("<small>jamesaxl and c10ud</small>")
        title.set_line_wrap(True)
        disc.set_line_wrap(True)
        authors.set_line_wrap(True)
        box = dialog.get_content_area()
        box.add(image)
        box.add(title)
        box.add(disc)
        box.add(authors)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()