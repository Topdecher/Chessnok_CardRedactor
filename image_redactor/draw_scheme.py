from PIL import ImageDraw, ImageFont, Image
from image_redactor.constants import *


class DrawScheme:
    def __init__(self, draw, reference, default_init=True):
        self.draw = draw
        self.reference = reference
        self.power = None
        self.name = None
        self.text = None
        self.artist = None
        self.rarity = None
        self.type = None
        self.king_table = None
        if default_init:
            self.DefaultInit()

    def DefaultInit(self):
        self.power = PowerBox(self.reference['power'])
        self.name = NameBox(self.draw, self.reference['name'])
        self.text = TextBox(self.draw, self.reference['text'])
        self.artist = ArtistBox(self.draw, self.reference['artist'])
        self.rarity = IconBox(self.reference['rarity'])
        self.type = IconBox(self.reference['type'])


class Box:
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height


class TextBox(Box):
    def __init__(self, draw, content='', font_path=DEFAULT_FONT, font_size=DEFAULT_TEXT_FONT_SIZE,
                 min_font_size=MIN_FONT_SIZE, size_step=SIZE_STEP, spacing=SPACING,
                 max_width=MAX_TEXT_WIDTH, max_height=MAX_TEXT_HEIGHT):
        super().__init__()
        self.draw = draw
        self.content = content
        self.font_path = font_path
        self.font_size = font_size
        self.min_font_size = min_font_size
        self.size_step = size_step
        self.max_width = max_width
        self.max_height = max_height
        self.spacing = spacing
        self.text = self.parse_content()

    def parse_content(self):
        text = ''
        while self.font_size >= self.min_font_size:
            font = ImageFont.truetype(font=self.font_path, size=self.font_size)
            text = ''
            words = self.content.split(' ')
            word_counter = 0
            while word_counter < len(words):
                current_line = ''
                while word_counter < len(words):
                    next_line = current_line + ' ' + words[word_counter]
                    if font.getlength(next_line) > self.max_width:
                        break
                    current_line = next_line
                    word_counter += 1
                    if current_line[-1] == '\n':
                        break
                text += current_line
                if current_line[-1] != '\n':
                    text += '\n'
            text_box = self.draw.multiline_textbbox((0, 0), text, spacing=self.spacing)
            self.font_size -= self.size_step
            self.width = text_box[2] - text_box[0]
            self.height = text_box[3] - text_box[1]
            if self.height <= self.max_height:
                break
        if self.height > self.max_height:
            return TOO_LARGE_STRING
        return text


class NameBox(Box):
    def __init__(self, draw, content='', font_path=DEFAULT_FONT, font_size=DEFAULT_NAME_FONT_SIZE,
                 max_width=MAX_TEXT_WIDTH, max_height=MAX_NAME_HEIGHT):
        super().__init__()
        self.draw = draw
        self.content = content
        self.font_path = font_path
        self.font_size = font_size
        self.max_width = max_width
        self.max_height = max_height
        self.text = self.parse_content()

    def parse_content(self):
        font = ImageFont.truetype(font=self.font_path, size=self.font_size)
        text_box = self.draw.textbbox((0, 0), self.content, font)
        self.width = text_box[2] - text_box[0]
        self.height = text_box[3] - text_box[1]
        if self.width > self.max_width or self.height > self.max_height:
            return TOO_LARGE_STRING
        return self.content


class ArtistBox(NameBox):
    def __init__(self, draw, content='', font_path=DEFAULT_FONT, font_size=DEFAULT_ARTIST_FONT_SIZE,
                 max_width=MAX_ARTIST_WIDTH, max_height=MAX_ARTIST_HEIGHT):
        super().__init__(draw, content, font_path, font_size, max_width, max_height)
        self.text = ARTIST_STRING + self.text


class PowerBox(Box):
    def __init__(self, number=0, font_path=DEFAULT_FONT, font_size=DEFAULT_NAME_FONT_SIZE, max_width=MAX_TEXT_WIDTH):
        super().__init__()
        self.number = number
        self.font_path = font_path
        self.font_size = font_size
        self.max_width = max_width
        font = ImageFont.truetype(font_path, font_size)
        if font.getlength(str(number)) > max_width or number < 0:
            self.power = INVALID_NUMBER
        else:
            self.power = str(self.number)


class IconBox(Box):
    def __init__(self, icon_name=None):
        super().__init__()
        self.icon_name = icon_name
        if icon_name is None:
            self.path = None
        else:
            self.path = ICON_PATH + icon_name
            with Image.open(self.path) as im:
                self.width = im.width
                self.height = im.height


class TableBox(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
