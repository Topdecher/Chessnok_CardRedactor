import wx
from interface import settings


class SaveButton(wx.Button):
    def __init__(self, panel, extra_label, extra_label_pos, *args, **kwargs):
        super().__init__(panel, *args, **kwargs)
        self.panel = panel
        default_font = wx.Font(settings.DEFAULT_FONT_SIZE, wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label = wx.StaticText(panel, label=extra_label, pos=extra_label_pos, size=settings.DEFAULT_LABEL_SIZE)
        self.label.SetFont(default_font)
