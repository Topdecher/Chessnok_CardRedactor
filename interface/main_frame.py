import wx
import wx.richtext

from image_redactor.image_drawer import ImageDrawer
from interface.menus.file_menu import FileMenu
from interface.input_control import LabeledTextCtrl, LabeledRichTextCtrl
from interface.settings import *


class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title='Chessnok card redactor', size=(1200, 800))
        self.Center()
        self.init_ui()
        self.image_drawer = ImageDrawer(self, ASSETS_PATH + CLASSIC_FACE, ASSETS_PATH + EDIT_FACE)
        self.bind_events()

    def init_ui(self):
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour(wx.GREEN)
        self.create_menu_bar()
        self.create_card_image()
        self.create_text_controls()

    def create_menu_bar(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menubar.Append(FileMenu(menubar), '&File')

    def create_card_image(self):
        self.card_image = wx.StaticBitmap(self.main_panel)
        # self.another = wx.StaticBitmap(self.main_panel)
        bitmap = wx.Bitmap(ASSETS_PATH + CLASSIC_FACE, wx.BITMAP_TYPE_PNG)
        bitmap = self.scale_bitmap(bitmap, CARD_SIZE[0], CARD_SIZE[1])
        x_pos = self.GetSize()[0] - CARD_RIGHT_GAP - CARD_SIZE[0]
        y_pos = self.GetSize()[1] // 2 - CARD_SIZE[1] // 2
        # self.another.SetBitmap(bitmap)
        # self.another.SetPosition((800, 400))
        self.card_image.SetPosition((x_pos, y_pos))
        self.card_image.SetBitmap(bitmap)

    def update_card_image(self):
        bitmap = wx.Bitmap(ASSETS_PATH + EDIT_FACE, wx.BITMAP_TYPE_PNG)
        bitmap = self.scale_bitmap(bitmap, CARD_SIZE[0], CARD_SIZE[1])
        self.card_image.SetBitmap(bitmap)

    def scale_bitmap(self, bitmap, width, height):
        image = wx.Bitmap.ConvertToImage(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

    def create_text_controls(self):
        self.card_name = LabeledTextCtrl(self.main_panel, 'name', 'card_name',
                                         NAME_LABEL_POS, pos=NAME_POS, size=NAME_SIZE)
        self.text_name = LabeledRichTextCtrl(self.main_panel, 'text', 'card text',
                                             TEXT_LABEL_POS, pos=TEXT_POS, size=TEXT_SIZE)

    def bind_events(self):
        self.main_panel.Bind(wx.EVT_TEXT, self.image_drawer.scheme_builder.on_redacting, self.card_name)
        self.main_panel.Bind(wx.EVT_TEXT, self.image_drawer.scheme_builder.on_redacting, self.text_name)
        self.main_panel.Bind(wx.EVT_CLOSE, self.on_quit)

    def on_quit(self, event):
        self.image_drawer.close_image()
        self.Close()
