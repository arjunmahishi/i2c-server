import logging, busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

try:
    from board import SCL, SDA
except NotImplementedError:
    logging.warning("No board detected. Running in test mode")
    SCL = None
    SDA = None

OVERFLOW_NONE = 0
OVERFLOW_NEXT_LINE = 1

BLACK = 0
WHITE = 255

class Device:
    def __init__(self, width=128, height=32):
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)

    def image(self, image):
        self.disp.image(image)

    def show(self):
        self.disp.show()

class Display:
    def __init__(self,
                 font=ImageFont.load_default(),
                 transpose=None, overflow=OVERFLOW_NONE, width=128, height=32,
                 inverted=False):

        self.device = None
        if SCL is not None and SDA is not None:
            self.device = Device(width, height)

        self.width = width
        self.height = height

        self.transpose = transpose
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.x = 0

        self.overflow = overflow
        self.font = font
        self.background = WHITE if inverted else BLACK
        self.foreground = BLACK if inverted else WHITE

        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_text(self, text):
        text = self.format_text(text)
        self.draw.rectangle((0, 0, self.width, self.height),
                            outline=BLACK,
                            fill=self.background)
        self.draw.text((self.x, self.top + 0),
                       text,
                       font=self.font,
                       fill=self.foreground)
        self.show()

    def draw_image(self, image):
        self.draw.rectangle((0, 0, self.width, self.height),
                            outline=BLACK,
                            fill=self.background)
        self.image.paste(image, (0, 0))
        self.show()

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height),
                            outline=BLACK,
                            fill=BLACK)
        self.show()

    def format_text(self, text):
        if self.overflow == OVERFLOW_NEXT_LINE:
            lines = []
            line = ""
            for word in text.split(" "):
                if self.font.getlength(line + word) > self.width:
                    lines.append(line)
                    line = ""
                line += word + " "
            lines.append(line)
            return "\n".join(lines)

        return text

    def show(self):
        image = self.image.copy()
        if self.transpose is not None:
            image = self.image.transpose(self.transpose)

        if self.device is not None:
            self.device.image(image)
            self.device.show()
            return

        image.show()

def resize_image(image, size):
    return image.resize(size)

if __name__ == "__main__":
    display = Display(inverted=True)
    # display.draw_text("Hello World! This is a test")

    img = Image.open("/Users/arjunmahishi/Downloads/1bit.png")
    resized = resize_image(img, (128, 32))
    display.draw_image(resized)
