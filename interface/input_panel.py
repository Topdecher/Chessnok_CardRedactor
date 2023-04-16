import wx
from wx.lib.filebrowsebutton import FileBrowseButton

from interface.save_button import SaveButton
from interface.settings import *
from interface.input_control import LabeledTextCtrl, LabeledRichTextCtrl


class InputPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.card_power_input = LabeledTextCtrl(self, 'power', 'Сила карты:',
                                                POWER_LABEL_POS, pos=POWER_POS, size=POWER_SIZE)
        self.card_power_input.SetMaxLength(POWER_MAX_CHARS)
        self.card_power_input.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.card_name_input = LabeledRichTextCtrl(self, 'name', 'Название карты',
                                                   NAME_LABEL_POS, pos=NAME_POS, size=NAME_SIZE)
        self.card_text_input = LabeledRichTextCtrl(self, 'text', 'Текст карты',
                                                   TEXT_LABEL_POS, pos=TEXT_POS, size=TEXT_SIZE)
        self.image_browse_button = FileBrowseButton(self, pos=IMAGE_BROWSER_POS, size=IMAGE_BROWSER_SIZE,
                                                    labelText='Найти изображение', buttonText='Найти',
                                                    dialogTitle='Выберите изображение')
        self.card_save_button = SaveButton(self, 'Cохранить изображение:', SAVE_BUTTON_LABEL_POS,
                                           pos=SAVE_BUTTON_POS, size=SAVE_BUTTON_SIZE, label='Сохранить')
