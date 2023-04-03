import wx
from interface.menus.file_menu import FileMenu


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Chessnok card redactor')
        self.init_ui()

    def init_ui(self):
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menubar.Append(FileMenu(menubar), '&File')

    def on_quit(self, event):
        self.Close()
