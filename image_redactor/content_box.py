from PIL import ImageDraw, ImageFont, Image
from image_redactor.constants import *


class Box:
    def __init__(self, drawer, width=0, height=0):
        self.drawer = drawer
        self.width = width
        self.height = height

    def parse_content(self): pass

    def update_content(self, content): pass


class TextBox(Box):
    def __init__(self, drawer, content='', font_path=DEFAULT_FONT, default_font_size=DEFAULT_TEXT_FONT_SIZE,
                 min_font_size=MIN_FONT_SIZE, size_step=SIZE_STEP, spacing=SPACING,
                 max_width=MAX_TEXT_WIDTH, max_height=MAX_TEXT_HEIGHT):
        super().__init__(drawer)
        self.content = content
        self.font_path = font_path
        self.default_font_size = default_font_size
        self.font_size = default_font_size
        self.min_font_size = min_font_size
        self.size_step = size_step
        self.max_width = max_width
        self.max_height = max_height
        self.spacing = spacing
        self.text = self.parse_content()

    def discard_font_size(self):
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
        text = ''
        self.discard_font_size()
        while self.font_size >= self.min_font_size:
            font = ImageFont.truetype(font=self.font_path, size=self.font_size, encoding='UTF-8')
            text = ''
            words = self.smart_split(self.content)
            print(words)
            word_counter = 0
            while word_counter < len(words):
                if font.getlength(words[word_counter]) > self.max_width:
                    return TOO_LARGE_STRING
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
                    if font.getlength(next_line) > self.max_width:
                        break
                    current_line = next_line
                    if current_line[-1] == '\n':
                        word_counter += 1
                        break
                    word_counter += 1
                text += current_line + ('' if current_line[-1] == '\n' else '\n')
            text_box = self.drawer.draw.multiline_textbbox((0, 0), text, font=font, spacing=self.spacing)
            self.font_size -= self.size_step
            self.width = text_box[2] - text_box[0]
            self.height = text_box[3] - text_box[1]
            if self.height <= self.max_height:
                break
        if self.height > self.max_height:
            return TOO_LARGE_STRING
        return text

    def update_content(self, content):
        self.content = content
        self.text = self.parse_content()


class NameBox(Box):
    def __init__(self, drawer, content='', font_path=DEFAULT_FONT, default_font_size=DEFAULT_NAME_FONT_SIZE,
                 max_width=MAX_TEXT_WIDTH, max_height=MAX_NAME_HEIGHT):
        super().__init__(drawer)
        self.content = content
        self.font_path = font_path
        self.default_font_size = default_font_size
        self.max_width = max_width
        self.max_height = max_height
        self.text = self.parse_content()

    def parse_content(self):
        font = ImageFont.truetype(font=self.font_path, size=self.default_font_size)
        text_box = self.drawer.draw.textbbox((0, 0), self.content, font)
        self.width = text_box[2] - text_box[0]
        self.height = text_box[3] - text_box[1]
        if self.width > self.max_width or self.height > self.max_height:
            return TOO_LARGE_STRING
        return self.content

    def update_content(self, content):
        self.content = content
        self.text = self.parse_content()


class ArtistBox(NameBox):
    def __init__(self, drawer, content='', font_path=DEFAULT_FONT, font_size=DEFAULT_ARTIST_FONT_SIZE,
                 max_width=MAX_ARTIST_WIDTH, max_height=MAX_ARTIST_HEIGHT):
        super().__init__(drawer, content, font_path, font_size, max_width, max_height)
        self.text = ARTIST_STRING + self.text

    def update_content(self, content):
        self.content = content
        self.text = ARTIST_STRING + self.parse_content()


class PowerBox(Box):
    def __init__(self, drawer, content=0, font_path=DEFAULT_FONT, font_size=DEFAULT_NAME_FONT_SIZE,
                 max_width=MAX_TEXT_WIDTH):
        super().__init__(drawer)
        self.content = int(content)
        self.font_path = font_path
        self.font_size = font_size
        self.max_width = max_width
        self.power = self.parse_content()

    def parse_content(self):
        font = ImageFont.truetype(self.font_path, self.font_size)
        if font.getlength(str(self.content)) > self.max_width or self.content < 0:
            return INVALID_NUMBER
        else:
            return str(self.content)

    def update_content(self, content):
        self.content = int(content)
        self.power = self.parse_content()


class IconBox(Box):
    def __init__(self, drawer, icon_name=None):
        super().__init__(drawer)
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
