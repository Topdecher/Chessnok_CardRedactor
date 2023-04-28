from PIL import Image, ImageDraw, ImageFont

from interface import settings


class CardDrawer:
    """support class for more accurate image redacting and more simple file management"""
    def __init__(self, panel, save_path=None):
        self.panel = panel
        self.save_path = save_path
        self.draw = None

    def draw_multiline_text(self, text_box, save_path):
        """updates text image by drawing it in multiple lines"""
        if text_box.text == '':
            image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            image.save(settings.ASSETS_PATH + save_path, 'png')
            image.close()
            return
        image = Image.new('RGBA', (text_box.width, text_box.height + text_box.spacing), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(image)
        self.draw.multiline_text((0, 0), text_box.text, fill=settings.DEFAULT_FONT_COLOR, font=text_box.font,
                                 spacing=text_box.spacing, align='center')
        image.save(settings.ASSETS_PATH + save_path, 'png')
        image.close()

    def draw_text(self, text_box, save_path):
        """updates text image by drawing it in one line"""
        if text_box.text == '':
            image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            image.save(settings.ASSETS_PATH + save_path, 'png')
            image.close()
            return
        image = Image.new('RGBA', (text_box.width, text_box.height * 2), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(image)
        self.draw.text((0, 0), text_box.text, fill=settings.DEFAULT_FONT_COLOR, font=text_box.font, align='center')
        image.save(settings.ASSETS_PATH + save_path, 'png')
        image.close()

    def setup_image(self, image_path):
        """updates image for card"""
        image = Image.open(image_path).copy()
        image.save(settings.ASSETS_PATH + settings.EDIT_IMAGE, 'png')
        image.close()

    @staticmethod
    def get_multiline_textbox(text, font, spacing):
        """returns box of multiline text"""
        empty_image = Image.new('RGBA', settings.CARD_SIZE)
        textbox = ImageDraw.Draw(empty_image).multiline_textbbox((0, 0), text=text, font=font, spacing=spacing)
        empty_image.close()
        return textbox

    @staticmethod
    def get_textbox(text, font):
        """returns box of single line text"""
        empty_image = Image.new('RGBA', settings.CARD_SIZE)
        textbox = ImageDraw.Draw(empty_image).textbbox((0, 0), text=text, font=font)
        empty_image.close()
        return textbox

    @staticmethod
    def draw_card(card, save_path=None):
        """draws the card by components and saves it"""
        save_image = Image.new('RGBA', settings.CARD_SIZE)

        # image part
        if card.image.bitmap_path is not None:
            edit_image = Image.open(card.image.bitmap_path)
            cropped_image = edit_image.crop((card.image_anchor[0], card.image_anchor[1],
                                             card.image_anchor[0] + settings.CARD_SIZE[0],
                                             card.image_anchor[1] + settings.CARD_SIZE[1]))
            save_image.alpha_composite(cropped_image)
            cropped_image.close()

        # other components
        for component in card.values():
            if component.bitmap_path is not None:
                component_image = Image.open(component.bitmap_path)
                save_image.alpha_composite(component_image, component.position)
                component_image.close()

        save_image.save(settings.ASSETS_PATH + settings.EDIT_CARD, 'png')
        if save_path is not None:
            extension = save_path.split('.')[-1].upper()
            if extension in settings.IMAGE_EXTENSIONS:
                save_image.save(save_path, extension)
        save_image.close()
