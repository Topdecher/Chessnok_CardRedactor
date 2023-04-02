import wx
from interface.menus.file_menu import FileMenu


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Chessnok card redactor')
        self.InitUI()

    def InitUI(self):
        self.CreateMenuBar()

    def CreateMenuBar(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menubar.Append(FileMenu(menubar), '&File')

    def OnQuit(self, event):
        self.Close()
