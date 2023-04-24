import wx

from image_redactor.card_drawer import CardDrawer
from image_redactor.card_scheme import Card
from interface.settings import *


class CardPanel(wx.Panel):
    """represents the right side of app where the card is showed"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.card_drawer = CardDrawer(self)
        self.init_card()
        self.setup_image(ASSETS_PATH + EDIT_IMAGE)
        self.bind_events()

    def init_card(self):
        """creates card and setups default face"""
        pos_x = self.GetSize()[0] - CARD_RIGHT_GAP - CARD_SIZE[0]
        pos_y = self.GetSize()[1] // 2 - CARD_SIZE[1] // 2 - CARD_BOTTOM_GAP
        self.card = Card(self.card_drawer, (pos_x, pos_y))
        self.card['face'].set_bitmap(wx.Bitmap(ASSETS_PATH + CLASSIC_FACE, wx.BITMAP_TYPE_PNG))
        self.card['face'].set_bitmap_path(ASSETS_PATH + CLASSIC_FACE)

    def bind_events(self):
        """binds paint and keyboard events"""
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_CHAR_HOOK, self.move_image)

    def centralize_card_component(self, keyword):
        """moves component to make its current position be the center of image"""
        component = self.card[keyword]
        if not component.can_centralize:
            return
        component.discard_position()
        size = self.card[keyword].get_bitmap_size()
        component.move((-(size[0] // 2), -(size[1] // 2)))
        component.move(self.card['face'].get_position())

    def update_card_component(self, keyword):
        """loads updated bitmap for component by keyword"""
        component = self.card[keyword]
        bitmap = wx.Bitmap(ASSETS_PATH + EDIT_PREFIX + keyword + DEFAULT_EXTENSION)
        if bitmap.GetSize() != EMPTY_BITMAP_SIZE:
            component.set_bitmap(bitmap)
            component.set_bitmap_path(ASSETS_PATH + EDIT_PREFIX + keyword + DEFAULT_EXTENSION)
        else:
            component.set_bitmap(None)
            component.set_bitmap_path(None)
        self.centralize_card_component(keyword)
        self.Refresh()

    def update_card_image(self):
        """specifically updates image component"""
        bitmap = wx.Bitmap(ASSETS_PATH + EDIT_IMAGE)
        if bitmap.GetSize() == (1, 1):
            self.card.image.set_bitmap(None)
            self.card.image.set_bitmap_path(None)
        if bitmap.GetSize()[0] < CARD_SIZE[0] or bitmap.GetSize()[1] < CARD_SIZE[1]:
            bitmap = wx.Bitmap(ASSETS_PATH + ERROR_IMAGE)
            self.card.image.set_bitmap_path(ASSETS_PATH + ERROR_IMAGE)
        else:
            self.card.image.set_bitmap_path(ASSETS_PATH + EDIT_IMAGE)
        self.card.image.set_bitmap(bitmap)
        self.card.image_anchor = ((bitmap.GetSize()[0] - CARD_SIZE[0]) // 2,
                                  (bitmap.GetSize()[1] - CARD_SIZE[1]) // 2)
        self.Refresh()

    def update_card_writable_component(self, keyword, new_content=None):
        """specifically updates any component with TextBox by keyword"""
        if new_content is None:
            self.card.redact(keyword, self.card[keyword].content)
        else:
            self.card.redact(keyword, new_content)
        self.update_card_component(keyword)

    def on_text_redacting(self, event: wx.Event):
        """updates text component if it is redacted"""
        input_text = event.GetEventObject()
        self.card.redact(input_text.keyword, input_text.get_value())
        self.update_card_component(input_text.keyword)
        if input_text.keyword == 'name' or input_text.keyword == 'text' or input_text.keyword == 'flavour_text':
            self.rearrange_text()

    def rearrange_text(self):
        """spaces text in the card and updates it if changes are made"""
        current_height = 0
        self.card['name'].set_position(CENTER_LINE - self.card['name'].width // 2, UPPER_BORDER)
        current_height += UPPER_BORDER + self.card['name'].height + TEXT_NAME_GAP
        self.card['text'].max_height = LOWER_TEXT_BORDER - current_height
        self.update_card_writable_component('text')
        self.card['text'].set_position(CENTER_LINE - self.card['text'].width // 2, current_height)
        # make error occurrence for absurdly long names
        self.Refresh()

    def on_paint(self, event: wx.Event):
        """draws the whole card by components on the right"""
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush(wx.WHITE))
        dc.Clear()

        # ... drawing here all other images in order of overlapping
        if self.card.image.bitmap is not None:
            image_bitmap = self.card.image.bitmap.GetSubBitmap(wx.Rect(self.card.image_anchor[0],
                                                                       self.card.image_anchor[1],
                                                                       CARD_SIZE[0], CARD_SIZE[1]))
            dc.DrawBitmap(image_bitmap, self.card.position[0], self.card.position[1], True)
        for component in self.card.values():
            if component.bitmap is not None:
                dc.DrawBitmap(component.bitmap, component.position[0] + self.card.position[0],
                              component.position[1] + self.card.position[1], True)

    def on_image_change(self, event: wx.Event):
        """fires when image of card is changed"""
        self.setup_image(event.GetEventObject().GetValue())

    def setup_image(self, image_path):
        """changes the image of card"""
        if image_path.split('.')[-1].upper() not in IMAGE_EXTENSIONS:
            return
        self.card_drawer.setup_image(image_path)
        bitmap = wx.Bitmap(ASSETS_PATH + EDIT_IMAGE)
        self.card.image_anchor = ((bitmap.GetSize()[0] - CARD_SIZE[0]) // 2, (bitmap.GetSize()[1] - CARD_SIZE[1]) // 2)
        self.update_card_image()

    def move_image(self, event: wx.KeyEvent):
        """moves images after pressing arrows on keyboard"""
        if self.card.image.bitmap is None:
            return
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RIGHT and self.card.image_anchor[0] + CARD_SIZE[0] + SCROLL_SPEED - 1 <\
                self.card.image.bitmap.GetSize()[0]:
            self.card.image_anchor = (self.card.image_anchor[0] + SCROLL_SPEED, self.card.image_anchor[1])
        elif keycode == wx.WXK_LEFT and self.card.image_anchor[0] > SCROLL_SPEED - 1:
            self.card.image_anchor = (self.card.image_anchor[0] - SCROLL_SPEED, self.card.image_anchor[1])
        elif keycode == wx.WXK_DOWN and self.card.image_anchor[1] + CARD_SIZE[1] + SCROLL_SPEED - 1 <\
                self.card.image.bitmap.GetSize()[1]:
            self.card.image_anchor = (self.card.image_anchor[0], self.card.image_anchor[1] + SCROLL_SPEED)
        elif keycode == wx.WXK_UP and self.card.image_anchor[1] > SCROLL_SPEED - 1:
            self.card.image_anchor = (self.card.image_anchor[0], self.card.image_anchor[1] - SCROLL_SPEED)
        self.Refresh()

    def save_image(self, event=None):
        """saves image to browsed path with CardDrawer"""
        with wx.FileDialog(self, "Save PNG file", wildcard="PNG files (*.png)|*.png",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                CardDrawer.draw_card(self.card)
                return
            save_path = fileDialog.GetPath()
        CardDrawer.draw_card(self.card, save_path)

