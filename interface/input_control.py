import wx
import wx.richtext
from interface.settings import *


class LabeledTextCtrl(wx.TextCtrl):
    def __init__(self, panel, keyword, label, label_pos, *args, **kwargs):
        super().__init__(panel, *args, **kwargs)
        self.panel = panel
        self.keyword = keyword
        default_font = wx.Font(DEFAULT_FONT_SIZE, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label = wx.StaticText(panel, label=label, pos=label_pos, size=DEFAULT_LABEL_SIZE)
        self.label.SetFont(default_font)

    def get_value(self):
        return self.GetValue()


class LabeledRichTextCtrl(wx.richtext.RichTextCtrl):
    def __init__(self, panel, keyword, label, label_pos, *args, **kwargs):
        super().__init__(panel, *args, **kwargs)
        self.panel = panel
        self.keyword = keyword
        default_font = wx.Font(DEFAULT_FONT_SIZE, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label = wx.StaticText(panel, label=label, pos=label_pos, size=DEFAULT_LABEL_SIZE)
        self.label.SetFont(default_font)

    def get_value(self):
        return self.GetValue()
