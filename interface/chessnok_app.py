import wx

from interface.main_frame import MainFrame


class ChessnokApp(wx.App):
    """main class of app"""
    def __init__(self):
        super().__init__()
        self.main_frame = MainFrame()
        self.main_frame.Show()

    def bind_hotkeys(self):
        """setups hotkeys"""
        pass
