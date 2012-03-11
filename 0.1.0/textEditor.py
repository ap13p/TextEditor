#!/usr/bin/env python

import wx
import os

wildcard = "Python source (*.py)|*.py|"     \
           "Text files (*.txt)|*.txt|"      \
           "All files (*.*)|*.*"


class Frame(wx.Frame):
    _path = None
    def __init__(self, parent, winid=-1, title="Untitled"):
        wx.Frame.__init__(self, parent, winid, title)

        # Add a menu
        menu_file = wx.Menu()
        item_open = menu_file.Append(wx.ID_ANY, "&Open")
        self.Bind(wx.EVT_MENU, self.OnOpen, item_open)
        # FIXME: Belum bisa menangkap
#        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        item_save = menu_file.Append(wx.ID_ANY, "&Save")
        self.Bind(wx.EVT_MENU, self.OnSave, item_save)

        item_exit = menu_file.Append(wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, self.close_app, item_exit)

        # Menubar
        menubar = wx.MenuBar()
        menubar.Append(menu_file, "&File")
        self.SetMenuBar(menubar)

        # Create the rtc
        self.rtc = wx.TextCtrl(self, wx.ID_ANY,
                    style=wx.TE_MULTILINE|wx.TE_AUTO_SCROLL|wx.HSCROLL)

        wx.CallAfter(self.rtc.SetFocus)

        # Create statusbar
        self.CreateStatusBar(number=2, name="Status2")

    def close_app(self, event):
        self.Close()

    def OnOpen(self, event):
        dlg = wx.FileDialog(
            self, message="Open File",
            defaultDir=os.getcwd(),
            defaultFile='',
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR)
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                fp = open(path, 'r')
                self._path = path
                data = fp.read().strip()
#                print self._path
            self.rtc.SetValue(str(data))
            a = path.split('/')
            file_buka = a[-1]
            self.SetTitle(str(file_buka))
            self.SetStatusText(str(path), 0)
        dlg.Destroy()

    def OnSave(self, evt):
        if self._path is not None:
            data = self.rtc.GetValue()
            fp = open(self._path, 'w')
            fp.write(data)
            fp.close()
        else:
            dlg = wx.FileDialog(
                self, message="Save file as ...",
                defaultDir=os.getcwd(),
                defaultFile="", wildcard=wildcard,
                style=wx.SAVE
                )
            dlg.SetFilterIndex(2)
            data = self.rtc.GetValue()

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                print path
                # FIXME: Belum sukses
                fp = file(path, 'w')
                fp.write(data)
                fp.close()
                _file = path.split('/')[-1]
                self.SetTitle(_file)
                self.SetStatusText(path, 0)
            dlg.Destroy()

    def OnKeyDown(self, event):
#        if event is not None:
        print event.GetKeyCode()

class App(wx.App):
    def OnInit(self):
        main_frame = Frame(None, -1, "Untitled")
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()