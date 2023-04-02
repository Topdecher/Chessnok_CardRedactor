import wx

from interface.main_frame import MainFrame


class ChessnokApp(wx.App):
    def __init__(self):
        super().__init__()
        self.main_frame = MainFrame()
        self.main_frame.Show()

    def BindHotkeys(self):
        pass