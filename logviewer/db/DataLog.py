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

import sqlite3 as sqlite
import os
class DataLog(object):

    def get_session(self, session, account):
        contacts = []
        t = (account,)
        self.session = session
        self.account = account
        if self.session == "msn":
            self.path = "%s/.config/emesene2/messenger.hotmail.com/%s/log/base.db" %(os.getenv("HOME"),self.account)
        if self.session == "gtalk":
            self.path = "%s/.config/emesene2/talk.google.com/%s/log/base.db" %(os.getenv("HOME"), self.account)
        if self.session == "facebook":
            self.path = "%s/.config/emesene2/chat.facebook.com/%s/log/base.db" %(os.getenv("HOME"), self.account)

        connection = sqlite.connect(self.path)
        cursor = connection.cursor()
        SELECT_CONTACTS = '''SELECT account from d_account where account != ?;'''
        cursor.execute(SELECT_CONTACTS, t)
        for c in cursor:
            contacts.append(c)
        connection.close()
        return contacts

    def get_chat(self, account):
        infos = []
        t = (account,account)
        connection = sqlite.connect(self.path)
        cursor = connection.cursor()
        SELECT_CHATS = '''
        SELECT f.tmstp, f.payload, i.nick, a.account
        FROM fact_event f, d_info i, d_account a
        WHERE ((f.id_src_acc=1 and id_dest_acc = ( select id_account from d_account where account = ?)) or
        (f.id_dest_acc=1 and id_src_acc= (select id_account from d_account where account = ?))) and
        f.id_src_info = i.id_info and f.id_src_acc = a.id_account
        ORDER BY tmstp;
        '''
        cursor.execute(SELECT_CHATS, t)
        for c in cursor:
            infos.append(c)
        connection.close()
        return infos, self.session, self.account