import wx
from image_redactor.content_box import *


class DrawScheme:
    def __init__(self, drawer, reference=None):
        self.drawer = drawer
        self.power = PowerBox(drawer)
        self.name = NameBox(drawer)
        self.text = TextBox(drawer)
        self.artist = ArtistBox(drawer)
        self.rarity = None
        self.set = None
        self.type = None
        self.king_table = None
        if reference is not None:
            self.load_from_reference(reference)

    def load_from_reference(self, reference):
        self.power = PowerBox(self.drawer, reference['power'])
        self.name = NameBox(self.drawer, reference['name'])
        self.text = TextBox(self.drawer, reference['text'])
        self.artist = ArtistBox(self.drawer, reference['artist'])
        self.set = IconBox(self.drawer, reference['set'])
        self.rarity = IconBox(self.drawer, reference['rarity'])
        self.type = IconBox(self.drawer, reference['type'])


class SchemeBuilder:
    def __init__(self, image_drawer):
        self.image_drawer = image_drawer
        self.scheme = DrawScheme(image_drawer)

    def on_redacting(self, event: wx.Event):
        input_object = event.GetEventObject()
        self.scheme.__getattribute__(input_object.keyword).update_content(input_object.get_value())
        self.image_drawer.draw_from_scheme()
