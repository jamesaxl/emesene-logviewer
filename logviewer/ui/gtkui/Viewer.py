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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import WebKit
import os
import time
from xml.dom.minidom import Document

class Viewer(WebKit.WebView):
    def __init__(self):
        WebKit.WebView.__init__(self)
        self.connect('populate-popup', self._create_context_menu)

    def generate_finished(self,file_name):
        js = 'alert("%s was succefuly generated in your emesene-log");' %file_name
        self.execute_script(js)

    def load_contact_log(self, info = ""):
        self.xml=""
        self.html = """  <?xml version="1.0" encoding="utf-8"?>
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
                    <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                    </head>
                    <body style="background-color:#fff">
                    <div id=chats> """
        image = ""
        doc = Document()
        messages = info[0]
        session = info[1]
        account = info[2]
        chat = doc.createElement("chats")
        doc.appendChild(chat)
        self.contact = ""
        for m in messages:
            if account != m[3]: self.contact = m[3]
            time_s = time.localtime(m[0])
            chat_time = time.strftime("%Y-%m-%d %H:%M", time_s)
            tstrf = doc.createElement("time")
            src = doc.createElement("src")
            msg = doc.createElement("msg")
            tstrf_txt = doc.createTextNode(chat_time)
            src_txt = doc.createTextNode(m[3])
            msg_txt = doc.createTextNode(m[1])
            tstrf.appendChild(tstrf_txt)
            src.appendChild(src_txt)
            msg.appendChild(msg_txt)
            chat.appendChild(tstrf)
            tstrf.appendChild(src)
            tstrf.appendChild(msg)
            if session == "msn":
                image = "%s/.config/emesene2/messenger.hotmail.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, m[3])
            if session == "gtlak":
                image = "%s/.config/emesene2/talk.google.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, m[3])
            if session == "faceboo":
                image = "%s/.config/emesene2/chat.facebook.com/%s/%s/avatars/last" %(os.getenv("HOME"), account, m[3])

            self.html += """ <style>
                            #in_out{
                                padding:2px 2px 2px 5px;
                                background-image: -webkit-gradient(
                                linear,
                                left bottom,
                                left top,
                                color-stop(0.32, rgb(171,173,173)),
                                color-stop(0.66, rgb(189,186,183)),
                                color-stop(1, rgb(168,168,168)));
                                -webkit-border-radius: 15px 15px 15px 15px;
                                -webkit-box-shadow: #B3B3B3 7px 7px 7px;
                                }

                            #chats{
                                padding:2px 5px 2px 5px;
                                }
    
                            #message{
                                font-size:14px;
                                    }

                            .name 
                            {float:right;
                            font-size:11px;
                            font-weight:bold;
                                }
                            img{
                            float:left
                            padding-left:3px;
                            }
        
                            .clear{
                             height:20px;
                             }
                        </style>
                        <div id="in_out">
                            <span class="name">%s @ %s</span>
                            <p id="message">
                                <img src="%s"  height=40 width=40>
%s
                            </p>
                        </div>
                        <div class="clear"></div> """ % (m[3], chat_time, image,m[1])
        self.html += "</div></body></html>"
        self.load_html_string(self.html  , "file:///")
        self.xml = doc.toprettyxml(encoding="utf-8")

    def _create_context_menu(self, view, menu):
        """Create the context menu."""
        children = menu.get_children()
        for i, child in enumerate(children):
            menu.remove(child)
            child.destroy()
        generate_xml = Gtk.MenuItem("Generte xml")
        generate_html= Gtk.MenuItem("Generte html")
        menu.append(generate_xml)
        menu.append(generate_html)
        generate_xml.connect("activate", self.generate_xml)
        generate_html.connect("activate", self.generate_html)
        menu.show_all()

    def generate_xml(self, genrate):
        d = "%s/emesene-log" %os.getenv("HOME")
        out = "%s/%s.xml" %(d ,self.contact)
        if not os.path.exists(d):
            os.makedirs(d)
        self.generate_finished(self.contact+".xml")
        fo = open(out, "w")
        fo.write(self.xml)

    def generate_html(self, genrate):
        d = "%s/emesene-log" %os.getenv("HOME")
        out = "%s/%s.html" %(d, self.contact)
        if not os.path.exists(d):
            os.makedirs(d)
        self.generate_finished(self.contact+".html")
        fo = open(out, "w")
        fo.write(self.html.encode('utf-8'))