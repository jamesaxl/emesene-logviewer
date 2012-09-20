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
from gi.repository import Gtk as gtk
import os
import json

class MenuBar(gtk.MenuBar):
    def __init__(self, get_session, fill_contact_list, 
        show_widget, unload):

        gtk.MenuBar.__init__(self)
        conf_path = "%s/.config/emesene2/config" %os.getenv("HOME")
        data = json.load(open(conf_path))
        accounts = data[11][1]
        self.get_session = get_session
        self.fill_contact_list = fill_contact_list
        self.show_widget = show_widget
        self.unload = unload
        self.filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(self.filemenu)
        session = gtk.MenuItem("Session")
        session_menu = gtk.Menu()
        msn = gtk.MenuItem("MSN")
        gtalk = gtk.MenuItem("Google Talk")
        facebook = gtk.MenuItem("Facebook")
        session_msn = gtk.Menu()
        session_facebook = gtk.Menu()
        session_gtalk = gtk.Menu()
        for a in accounts:
            if a.split('|')[1] == "msn":
                msn_item =  gtk.MenuItem(a.split('|')[0])
                session_msn.append(msn_item)
                msn_item.connect("activate", self.item_session, a.split('|')[1])
            if a.split('|')[1] == "gtalk":
                gtalk_item =  gtk.MenuItem(a.split('|')[0])
                session_gtalk.append(gtalk_item)
                gtalk_item.connect("activate", self.item_session, a.split('|')[1])
            if a.split('|')[1] == "facebook":
                facebook_item =  gtk.MenuItem(a.split('|')[0])
                session_facebook.append(facebook_item)
                facebook_item.connect("activate", self.item_session, a.split('|')[1])

        self.unload_item = gtk.MenuItem("Unload")
        self.unload_item.connect("activate", self.unload, self.filemenu)
        exit = gtk.MenuItem("Exit")        
        exit.connect("activate", gtk.main_quit)
        session_menu.append(msn)
        session_menu.append(gtalk)
        session_menu.append(facebook)
        session.set_submenu(session_menu)
        msn.set_submenu(session_msn)
        facebook.set_submenu(session_facebook)
        gtalk.set_submenu(session_gtalk)
        self.filemenu.append(session)
        self.filemenu.append(exit)
        self.append(filem)

    def item_session(self, item, session):
        self.fill_contact_list(self.get_session(session, item.get_label()), 
            session, item.get_label())
        self.filemenu.insert(self.unload_item, 1)
        self.show_widget()