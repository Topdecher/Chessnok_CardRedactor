from PIL import ImageDraw, ImageFont, Image

from image_redactor.card_drawer import CardDrawer
from image_redactor.constants import *


class BitmapBox:
    """base class for components' holders"""

    def __init__(self, bitmap, bitmap_path, default_position=(0, 0), can_centralize=True):
        """init box holder of card component"""
        self.bitmap = bitmap
        self.bitmap_path = bitmap_path
        self.position = default_position
        self.default_position = default_position
        self.can_centralize = can_centralize
        self.width = 0
        self.height = 0

    def set_bitmap(self, bitmap):
        self.bitmap = bitmap

    def set_bitmap_path(self, bitmap_path):
        self.bitmap_path = bitmap_path

    def set_position(self, pos_x, pos_y):
        self.position = (pos_x, pos_y)

    def move(self, vector):
        self.position = (self.position[0] + vector[0], self.position[1] + vector[1])

    def discard_position(self):
        self.position = self.default_position

    def get_position(self):
        return self.position

    def get_bitmap_width(self):
        if self.bitmap is None:
            return 0
        return self.bitmap.Size[0]

    def get_bitmap_height(self):
        if self.bitmap is None:
            return 0
        return self.bitmap.Size[1]

    def get_bitmap_size(self):
        if self.bitmap is None:
            return 0, 0
        return self.bitmap.GetSize()


class TextBox(BitmapBox):
    """derived class for specifically holding and parsing text images"""
    def __init__(self, bitmap, bitmap_path, content='', font_path=DEFAULT_FONT,
                 default_font_size=DEFAULT_TEXT_FONT_SIZE, min_font_size=MIN_FONT_SIZE,
                 size_step=SIZE_STEP, spacing=SPACING,
                 max_width=MAX_TEXT_WIDTH, max_height=MAX_TEXT_HEIGHT, case=LOWER_CASE, **kwargs):
        """setups font parameters"""
        super().__init__(bitmap, bitmap_path, **kwargs)
        self.content = content
        self.font = None
        self.font_path = font_path
        self.default_font_size = default_font_size
        self.font_size = default_font_size
        self.min_font_size = min_font_size
        self.size_step = size_step
        self.max_width = max_width
        self.max_height = max_height
        self.spacing = spacing
        self.case = case
        self.text = self.parse_content()

    def discard_font_size(self):
        """discards font size to default"""
        self.font_size = self.default_font_size

    def smart_split(self, text):
        """splits by ' ' and '\n' preserving last one at the end of word"""
        words = []
        space_split = text.split(' ')
        for i in range(len(space_split)):
            space_split[i] = space_split[i].rstrip()
        for merged_words in space_split:
            if merged_words == '':
                continue
            word_split = merged_words.rstrip().split('\n')
            for i in range(len(word_split) - 1):
                words.append(word_split[i] + '\n')
            if merged_words[-1] == '\n':
                words.append(word_split[-1] + '\n')
            else:
                words.append(word_split[-1])
        return words

    def parse_content(self):
        """parses text by resizing or splitting it to different lines to fit the box"""
        text = ''
        self.discard_font_size()
        while self.font_size >= self.min_font_size:
            self.font = ImageFont.truetype(font=self.font_path, size=self.font_size, encoding='UTF-8')
            text = ''
            words = self.smart_split(self.content.lower() if self.case == LOWER_CASE else self.content.upper())
            word_counter = 0
            while word_counter < len(words):
                if self.font.getlength(words[word_counter]) > self.max_width:
                    # make dynamic to font size in future
                    return self.make_too_large_string_error()
                current_line = words[word_counter]
                if current_line[-1] == '\n':
                    text += current_line
                    word_counter += 1
                    continue
                word_counter += 1
                while word_counter < len(words):
                    if words[word_counter] == '':
                        word_counter += 1
                        continue
                    next_line = current_line + ' ' + words[word_counter]
                    if self.font.getlength(next_line) > self.max_width:
                        break
                    current_line = next_line
                    if current_line[-1] == '\n':
                        word_counter += 1
                        break
                    word_counter += 1
                text += current_line + ('' if current_line[-1] == '\n' else '\n')
            text_box = CardDrawer.get_multiline_textbox(text, self.font, self.spacing)
            self.font_size -= self.size_step
            self.width = text_box[2] - text_box[0]
            self.height = text_box[3] - text_box[1]
            if self.height <= self.max_height:
                break
        if self.height > self.max_height:
            return self.make_too_large_string_error()
        self.font_size = self.font.size
        return text

    def make_too_large_string_error(self):
        """creates error text if text too large to fit any box"""
        self.font = ImageFont.truetype(font=self.font_path, size=ERROR_FONT_SIZE, encoding='UTF-8')
        text_box = CardDrawer.get_multiline_textbox(TOO_LARGE_STRING, self.font, self.spacing)
        self.width = text_box[2] - text_box[0]
        self.height = text_box[3] - text_box[1]
        return TOO_LARGE_STRING

    def update_content(self, content):
        """updates text of this box"""
        self.content = content
        self.text = self.parse_content()


class NumberBox(TextBox):
    """derived class for specifically holding number value"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_font_size=DEFAULT_POWER_FONT_SIZE, spacing=0,
                         max_width=MAX_POWER_WIDTH, max_height=MAX_POWER_HEIGHT, **kwargs)

    def parse_content(self):
        """checks if text is number and it is valid number"""
        self.font = ImageFont.truetype(self.font_path, self.font_size, encoding='UTF-8')
        if self.content == '':
            self.width = 0
            self.height = 0
            return ''
        for symbol in self.content:
            if symbol not in '0123456789':
                return self.make_invalid_number_error()
        if self.font.getlength(self.content) > self.max_width or int(self.content) < 0:
            return self.make_invalid_number_error()
        else:
            text_box = CardDrawer.get_textbox(self.content, self.font)
            self.width = text_box[2] - text_box[0]
            self.height = text_box[3] - text_box[1]
            return self.content

    def make_invalid_number_error(self):
        """creates error text if number text is invalid"""
        text_box = CardDrawer.get_textbox(INVALID_NUMBER, self.font)
        self.width = text_box[2] - text_box[0]
        self.height = text_box[3] - text_box[1]
        return INVALID_NUMBER


class IconBox(BitmapBox):
    """derived class for specifically holding icons"""
    def __init__(self, pos_x=0, pos_y=0, icon_name=None):
        super().__init__(pos_x, pos_y)
        self.icon_name = icon_name
        if icon_name is None:
            self.path = None
        else:
            self.path = ICON_PATH + icon_name
            with Image.open(self.path) as im:
                self.width = im.width
                self.height = im.height

