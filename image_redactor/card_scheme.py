import wx
from image_redactor.content_box import TextBox, NumberBox, IconBox, BitmapBox
from image_redactor import constants
from interface import settings


class Card(dict):
    """just convenient class for holding and updating components"""
    def __init__(self, drawer, position, reference=None):
        """creates templates for main card components or load them from reference"""
        super().__init__()
        self.drawer = drawer
        self.position = position
        self.image = BitmapBox(None, None, can_centralize=False)
        self.image_anchor = (0, 0)
        self.text_box_height = settings.LOWER_TEXT_BORDER - settings.UPPER_BORDER
        self['face'] = BitmapBox(None, None, can_centralize=False)
        self['power'] = NumberBox(None, None, default_position=settings.CARD_POWER_POS)
        self['name'] = TextBox(None, None, case=constants.UPPER_CASE, can_centralize=False)
        self['text'] = TextBox(None, None, can_centralize=False)
        self['artist'] = BitmapBox(None, None)
        self['rarity'] = BitmapBox(None, None)
        self['set'] = BitmapBox(None, None)
        self['type'] = BitmapBox(None, None)
        self['king_table'] = BitmapBox(None, None)
        if reference is not None:
            pass

    def redact(self, keyword, new_value):
        """updates any text component by giving a keyword and new value"""
        attribute = self[keyword]
        attribute.update_content(new_value)
        if attribute.spacing == 0:
            self.drawer.draw_text(attribute, settings.EDIT_PREFIX + keyword + '.png')
        else:
            self.drawer.draw_multiline_text(attribute, settings.EDIT_PREFIX + keyword + '.png')
