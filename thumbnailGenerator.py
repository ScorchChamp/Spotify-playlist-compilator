import os
from PIL import Image, ImageFont, ImageDraw
import logging
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def wrapTitle(text):
    words = text.split()  # split the text into a list of words
    wrapped_text = ""     # initialize the wrapped text

    for i, word in enumerate(words):
        if i % 3 == 0 and i > 0:  # insert a newline after every 4th word
            wrapped_text += "\n"
        wrapped_text += word + " "  # add the word and a space to the wrapped text
    return wrapped_text

def generateThumbnail(thumbnailFile, title):
    title = wrapTitle(title)
    outputFile = thumbnailFile.replace(".png", "_thumbnail.png")
    image = Image.new(mode="RGBA", size=(1920,1080))
    foreground = Image.open(thumbnailFile)
    logo = Image.open('./assets/logoOpaque.png')
    ratio = min(800/foreground.width, 675/foreground.height)
    foreground = foreground.resize((int(foreground.width*ratio), int(foreground.height*ratio)))
    image.paste(Image.open('./assets/background.png'), (0,0))
    image.paste(foreground, (1100, 540 - foreground.height//2))
    image.paste(logo, (0,0), logo)
    font_size = 135
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Thin.ttf", font_size)     
    draw = ImageDraw.Draw(image)   
    fw, fh = draw.textsize(title, font=font)
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Thin.ttf", int(font_size * (900 / max(fw, 900))))
    fw, fh = draw.textsize(title, font=font)
    draw.text(
        ((1920/3)-(fw/2), 540 - (fh/2)),
        title, 
        "black", 
        font=font, 
        align="center",
    )  




    image.save(outputFile)
    return outputFile