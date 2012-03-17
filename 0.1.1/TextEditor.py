#!/usr/bin/env python

"""
TextEditor 0.1.0
author  : Afief S
website : http://ap13p.blogspot.com
email   : apiep.oedin@gmail.com
11 Maret 2012
"""

import wx
from os import getcwd

CURRENT_DIR = getcwd()
WILDCARD = "Python source (*.py)|*.py|"     \
           "Text files (*.txt)|*.txt|"      \
           "All files (*.*)|*.*"
WINSIZE = (700, 400)

class TextEditor(wx.Frame):
    nama_file = "Untitled"
    path = None
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=WINSIZE)

        # Menubar
        menu_file = wx.Menu()
        item_open = menu_file.Append(101, "&Open")
        item_save = menu_file.Append(102, "&Save")
        menu_file.AppendSeparator()
        item_exit = menu_file.Append(103, "E&xit")
        menubar = wx.MenuBar()
        menubar.Append(menu_file, "&File")
        self.SetMenuBar(menubar)

        # Create the event handler
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

        # FIXME: UJI COBA
        self.Bind(wx.EVT_TEXT, self.set_modified, self.textctrl)

    def set_modified(self, event):
        self.SetTitle(self.nama_file + " - TextEditor")
        self.SetStatusText("[Modified]", number=1)

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
            self.textctrl.SetValue(self._data)
            self.SetStatusText(self.path, number=0)


        dlg.Destroy()

    def save_file(self, event=None):
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
                print path
                # FIXME: Belum sukses
                fp = file(path, 'w')
                fp.write(data)
                fp.close()
                self.path = path
                self.nama_file = path.split('/')[-1]
                self.SetTitle(self.nama_file)
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