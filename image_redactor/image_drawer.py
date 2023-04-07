from PIL import Image, ImageDraw, ImageFont
from image_redactor.draw_scheme import SchemeBuilder


class ImageDrawer:
    def __init__(self, main_frame, image_path, save_path):
        self.main_frame = main_frame
        self.image_path = image_path
        self.save_path = save_path
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.scheme_builder = SchemeBuilder(self)

    def close_image(self):
        self.image.close()

    def draw_from_scheme(self):
        """dfnsdfkjdsfks"""
        self.image.close()
        self.image = Image.open(self.image_path)
        self.draw = ImageDraw.Draw(self.image)
        scheme = self.scheme_builder.scheme
        font = ImageFont.truetype(font=scheme.text.font_path, size=scheme.text.font_size, encoding='UTF-8')
        self.draw.multiline_text((100, 300), scheme.text.text, font=font, fill='black')
        self.image.save(self.save_path, "PNG")
        self.main_frame.update_card_image()
