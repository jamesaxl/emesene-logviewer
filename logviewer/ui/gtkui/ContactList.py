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
import gi
from gi.repository import Gtk, GdkPixbuf
import os
class ContactList(Gtk.TreeView):

    def __init__(self, load, get_chat):
        self.load = load
        self.get_chat = get_chat
        self.model = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        Gtk.TreeView.__init__(self, self.model)
        self.connect("cursor-changed", self.get_selected_contact)
        self.set_headers_visible(0)
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, stock_id=0)
        self.append_column(column_pixbuf)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=1)
        self.append_column(column_text)
        self.fill_contact_list(None, None, None)

    def  get_selected_contact(self, treemodel):
        tb = treemodel.get_selection()
        if tb != None:
            mod, itr = tb.get_selected()
            if itr != None:
                self.load(self.get_chat(mod.get_value(itr, 1)))


    def fill_contact_list(self, contacts, session, account):
        self.model.clear()
        avatar_path = ""
        account_avatar = ""
        if contacts != None:
            for c in contacts:
                if session == "msn":
                    avatar_path = "%s/.config/emesene2/messenger.hotmail.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, c[0])
                if session == "gtalk":
                    avatar_path = "%s/.config/emesene2/talk.google.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, c[0])
                if session == "facebook":
                    avatar_path = "%s/.config/emesene2/chat.facebook.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, c[0])
                try:
                    account_avatar = GdkPixbuf.Pixbuf.new_from_file_at_size(avatar_path, 25, 25)
                except gi._glib.GError:
                    avatar_path = "logviewer/icons/user.png"
                    account_avatar = GdkPixbuf.Pixbuf.new_from_file_at_size(avatar_path, 25, 25)
                self.model.append([account_avatar,c[0]])