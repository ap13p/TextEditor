#!/usr/bin/env python

"""
TextEditor 0.1.0
author  : Afief S
website : http://ap13p.blogspot.com
email   : apiep.oedin@gmail.com
12 Maret 2012
"""

import wx
from os import getcwd

CURRENT_DIR = getcwd()
WILDCARD = "All files (*.*)|*.*|"\
           "Python source (*.py)|*.py|"     \
           "Text files (*.txt)|*.txt|"      \

WINSIZE = (700, 400)

MODIFIER_DICT = {0: "",
                 4: "Shift",
                 2: "Ctrl",
                 1: "Alt"}

KARAKTER_DICT = {}
#48 - 126
#for i in range(48, 126): Asli
for i in range(1, 400):
    KARAKTER_DICT[i] = unichr(i)


class TextEditor(wx.Frame):
    nama_file = "Untitled"
    path = None

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=WINSIZE)

        # Menubar
        menu_file = wx.Menu()
        item_new = menu_file.Append(100, "&New File\tCtrl-N")
        item_open = menu_file.Append(101, "&Open\tCtrl-O")
        item_save = menu_file.Append(102, "&Save\tCtrl-S")
        menu_file.AppendSeparator()
        item_exit = menu_file.Append(103, "E&xit\tAlt-F4")
        menubar = wx.MenuBar()
        menubar.Append(menu_file, "&File")
        self.SetMenuBar(menubar)

        # Create the event handler
        self.Bind(wx.EVT_MENU, self.new_file, item_new)
        self.Bind(wx.EVT_MENU, self.open_file, item_open)
        self.Bind(wx.EVT_MENU, self.save_file, item_save)
        self.Bind(wx.EVT_MENU, self.close_app, item_exit)

        # Create the statusbar
        self.CreateStatusBar(number=3, winid=11, name="statusbar")

        # The TextCtrl
        self.textctrl = wx.TextCtrl(self, id=10,
                                    style=wx.TE_MULTILINE | wx.HSCROLL |
                                    wx.TE_AUTO_SCROLL)
        # Change the background to white
        self.textctrl.SetBackgroundColour("#FFFFFF")
        # Set the textctrl focused when the app is ready
        wx.CallAfter(self.textctrl.SetFocus)

        self.Bind(wx.EVT_TEXT, self.set_modified, self.textctrl)

        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_CHAR, self.onChar)

    def onKeyDown(self, event):
        modifier = MODIFIER_DICT[event.GetModifiers()]
        key_code = KARAKTER_DICT[event.GetKeyCode()]
#        print "Key Down", key_code, modifier

    def onKeyUp(self, event):
        modifier = MODIFIER_DICT[event.GetModifiers()]
        key_code = KARAKTER_DICT[event.GetKeyCode()]
#        print "Key Up", key_code, modifier
        if modifier == "Ctrl" and key_code == "O":
            self.open_file()
        elif modifier == "Ctrl" and key_code == "S":
            self.save_file()
        elif modifier == "Ctrl" and key_code == "N":
            self.new_file()
        else:
            pass

    def onChar(self, event):
        modifier = MODIFIER_DICT[event.GetModifiers()]
        key_code = KARAKTER_DICT[event.GetKeyCode()]
#        print "Char", key_code, modifier

    def set_modified(self, event):
        self.SetTitle(self.nama_file + " - TextEditor")
        self.SetStatusText("[Modified]", number=1)

    def new_file(self, event=None):
        self.textctrl.ChangeValue("")
        self.SetStatusText("", number=0)
        self.SetStatusText("", number=1)
        self.path = None
        self.set_judul(None)

    def open_file(self, event=None):
        dlg = wx.FileDialog(self,
                            message="Open File",
                            defaultDir=CURRENT_DIR,
                            defaultFile="",
                            wildcard=WILDCARD,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath()
            f_open = open(self.path, 'r')
            self._data = f_open.read().strip()
            f_open.close()
            self.nama_file = self.path.split('/')[-1]
            self.set_judul(self.nama_file)
            self.textctrl.ChangeValue(self._data)
            self.SetStatusText(self.path, number=0)
        dlg.Destroy()

    def save_file(self, event=None):
        # TODO: Beri peringatan ketika menulis ke file lain
        if self.path is not None:
            data = self.textctrl.GetValue()
            fp = open(self.path, 'w')
            fp.write(data)
            fp.close()
            self.SetStatusText("", number=1)
        else:
            dlg = wx.FileDialog(
                self, message="Save File",
                defaultDir=CURRENT_DIR,
                defaultFile="",
                wildcard=WILDCARD,
                style=wx.SAVE
                )
            data = self.textctrl.GetValue()

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
#                print path
                fp = file(path, 'w')
                fp.write(data)
                fp.close()
                self.path = path
                self.nama_file = path.split('/')[-1]
                self.set_judul(self.nama_file)
#                self.SetStatusText(path, 0)
            dlg.Destroy()
            self.SetStatusText("", number=1)

    def close_app(self, event=None):
        self.Close(True)

    def set_judul(self, judul=None):
        if judul is not None:
            self.SetTitle(judul + " - TextEditor")
        else:
            self.SetTitle("TextEditor")


class App(wx.App):
    def OnInit(self):
        te = TextEditor(None, -1, "TextEditor")
        te.Show()
        self.SetTopWindow(te)
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()