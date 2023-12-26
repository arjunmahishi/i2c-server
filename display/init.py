import time
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

try:
    from board import SCL, SDA
except NotImplementedError:
    # Handle the case where we're not on a Raspberry Pi
    SCL = None
    SDA = None

OVERFLOW_NONE = 0
OVERFLOW_NEXT_LINE = 1

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
                 transpose=None, overflow=OVERFLOW_NONE, width=128, height=32):

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
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_text(self, text):
        text = self.format_text(text)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top + 0), text, font=self.font, fill=255)
        self.show()

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
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

if __name__ == "__main__":
    display = Display(transpose=Image.ROTATE_180, overflow=OVERFLOW_NEXT_LINE)
    display.draw_text("Hello World! This is a test")
    time.sleep(2)
    display.draw_text("Hello World!")
    time.sleep(2)
    display.clear()

