import wx


class FileMenu(wx.Menu):
    def __init__(self, menubar):
        super().__init__()
        self.menubar = menubar
        self.InitItems()

    def InitItems(self):
        open_item = self.Append(wx.ID_OPEN, '&Open\tCtrl+O', 'Open image')
        new_card_face_item = self.Append(wx.ID_NEW, '&New\tCtrl+N', 'New card face')
        main_frame = self.menubar.GetFrame()
        main_frame.Bind(wx.EVT_MENU, main_frame.on_quit, open_item)
