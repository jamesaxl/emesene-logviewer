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

from gi.repository import Gtk, GdkPixbuf
import os
import json

class Login(Gtk.Alignment):
    def __init__(self, get_session, fill_contact_list, show_widget,
            unload, filemenu, unload_item):
        Gtk.Alignment.__init__(self, xalign=0.5, yalign=0.5, xscale=0.0, yscale=1.0)

        self.get_session = get_session
        self.fill_contact_list = fill_contact_list
        self.show_widget = show_widget
        self.unload = unload
        self.filemenu = filemenu
        self.unload_item = unload_item
        session_list = Gtk.ListStore(GdkPixbuf.Pixbuf, str)

        conf_path = "%s/.config/emesene2/config" %os.getenv("HOME")
        data = json.load(open(conf_path))
        self.contacts = data[11][1]

        h_session = Gtk.HBox(False,10)
        h_account = Gtk.HBox(False,10)
        u_img = Gtk.Image()
        u_img.set_from_file("logviewer/icons/user_def_image.png")
        s_img = Gtk.Image()
        s_img.set_from_file("logviewer/icons/session.png")

        session_img = "logviewer/icons/msn.png"
        session_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(session_img, 20, 20)
        session_list.append([session_pixbuf, "msn"])
        session_img = "logviewer/icons/gtalk.png"
        session_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(session_img, 20, 20)
        session_list.append([session_pixbuf, "gtalk"])
        session_img = "logviewer/icons/facebook.png"
        session_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(session_img, 20, 20)
        session_list.append([session_pixbuf, "facebook"])
        
        session_cb = Gtk.ComboBox.new_with_model(session_list)
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        renderer_text = Gtk.CellRendererText()
        session_cb.pack_start(renderer_pixbuf, True)
        session_cb.pack_start(renderer_text, True)
        session_cb.add_attribute(renderer_pixbuf, "pixbuf", 0)
        session_cb.add_attribute(renderer_text, "text", 1)

        account_list = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        account_cb = Gtk.ComboBox.new_with_model(account_list)
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        renderer_text = Gtk.CellRendererText()
        account_cb.pack_start(renderer_pixbuf, True)
        account_cb.pack_start(renderer_text, True)
        account_cb.add_attribute(renderer_pixbuf, "pixbuf", 0)
        account_cb.add_attribute(renderer_text, "text", 1)

        h_session.pack_start(s_img, False, False, 2)
        h_session.pack_start(session_cb, True, True, 2)
        h_account.pack_start(u_img, False, False, 2)
        h_account.pack_start(account_cb, True, True, 2)
        self.b_browse = Gtk.Button("Browse")
        self.b_browse.set_sensitive(False)
        self.b_browse.connect('clicked', self.open_log_session, session_cb, account_cb)
        al_button = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0.0, yscale=0.0)
        al_button.add(self.b_browse)
        image = Gtk.Image()
        u_image = "logviewer/icons/user_def_imagetool.png"
        image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
        image.set_from_pixbuf(image_pixbuf)
        image.xalign = 0.5
        image.yalign = 0.5

        session_cb.connect('changed', self.changed_cb, account_list, account_cb, image)
        v_login = Gtk.VBox(spacing=8)
        v_login.set_border_width(8)
        v_login.pack_start(image, False, False, 7)
        v_login.pack_start(h_session, False, False, 7)
        v_login.pack_start(h_account, False, False, 7)
        v_login.pack_start(al_button, False, False, 7)
        self.add(v_login)

    def changed_cb(self, session, account_list, account_cb, image):
        image_pixbuf = ""
        account_list.clear()
        model = session.get_model()
        index = session.get_active()
        if index != None:
            self.b_browse.set_sensitive(True)
            for c in self.contacts:
                if c.split('|')[1] == model[index][1]:
                    account_img = "logviewer/icons/%s.png" %model[index][1]
                    account_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(account_img, 20, 20)
                    account_list.append([account_pixbuf, c.split('|')[0]])
                    account_cb.set_active(0)
                    if model[index][1] == "msn":
                        u_image = "%s/.config/emesene2/messenger.hotmail.com/%s/avatars/last" %(os.getenv("HOME"), c.split('|')[0])
                        if os.path.exists(u_image):
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        else:
                            u_image = "logviewer/icons/user_def_imagetool.png"
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        image.set_from_pixbuf(image_pixbuf)
                    if model[index][1] == "gtalk":
                        u_image = "%s/.config/emesene2/talk.google.com/%s/avatars/last" %(os.getenv("HOME"), c.split('|')[0])
                        if os.path.exists(u_image):
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        else:
                            u_image = "logviewer/icons/user_def_imagetool.png"
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        image.set_from_pixbuf(image_pixbuf)
                    if model[index][1] == "facebook":
                        u_image = "%s/.config/emesene2/chat.facebook.com/%s/avatars/last" %(os.getenv("HOME"), c.split('|')[0])
                        if os.path.exists(u_image):
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        else:
                            u_image = "logviewer/icons/user_def_imagetool.png"
                            image_pixbuf =  GdkPixbuf.Pixbuf.new_from_file_at_size(u_image, 100, 100)
                        image.set_from_pixbuf(image_pixbuf)
        else:
            self.b_browse.set_sensitive(False)
        return

    def open_log_session(self, b_browse, session, account):
        model_s  = session.get_model()
        index_s = session.get_active()
        model_a = account.get_model()
        index_a = account.get_active()
        if index_a != None:
            self.fill_contact_list(self.get_session(model_s[index_s][1], model_a[index_a][1]), 
                model_s[index_s][1], model_a[index_a][1])
            self.filemenu.append(self.unload_item)
            self.show_widget()
        return