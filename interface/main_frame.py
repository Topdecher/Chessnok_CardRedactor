import wx
import wx.richtext

from interface.menus.file_menu import FileMenu
from interface.card_panel import CardPanel
from interface.input_panel import InputPanel


class MainFrame(wx.Frame):
    """the frame where the redacting takes place"""
    def __init__(self):
        super(MainFrame, self).__init__(None, title='Chessnok card redactor', size=(1200, 800))
        self.Center()
        self.main_panel = wx.Panel(self)
        self.init_ui()
        self.bind_events()

    def init_ui(self):
        """creates all ui such as panels and menu bars"""
        self.create_menu_bar()
        self.card_panel = CardPanel(self.main_panel, pos=(self.GetSize()[0] // 2, 0),
                                    size=(self.GetSize()[0] // 2, self.GetSize()[1]))
        self.card_panel.SetName('card_panel')
        self.card_panel.SetBackgroundColour(wx.WHITE)
        self.input_panel = InputPanel(self.main_panel, pos=(0, 0), size=(self.GetSize()[0] // 2, self.GetSize()[1]))
        self.input_panel.SetName('input_panel')

    def create_menu_bar(self):
        """creates menu bar"""
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        menubar.Append(FileMenu(menubar), '&File')

    def bind_events(self):
        """bind events between two panels"""
        self.input_panel.Bind(wx.EVT_TEXT, self.card_panel.on_text_redacting, self.input_panel.card_power_input)
        self.input_panel.Bind(wx.EVT_TEXT, self.card_panel.on_text_redacting, self.input_panel.card_name_input)
        self.input_panel.Bind(wx.EVT_TEXT, self.card_panel.on_text_redacting, self.input_panel.card_text_input)
        self.input_panel.image_browse_button.changeCallback = self.card_panel.on_image_change
        self.input_panel.Bind(wx.EVT_BUTTON, self.card_panel.save_image, self.input_panel.card_save_button)
        self.main_panel.Bind(wx.EVT_CLOSE, self.on_quit)

    def on_quit(self, event):
        """fires on quit"""
        # self.image_drawer.close_image()
        self.Close()
