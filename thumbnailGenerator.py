import os
from PIL import Image, ImageFont, ImageDraw, ImageFilter


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
    foreground = Image.open(thumbnailFile).convert("RGBA")
    logo = Image.open('./assets/logoOpaque.png')
    ratio = max(1920/foreground.width, 1080/foreground.height)
    foreground = foreground.resize((int(foreground.width*ratio), int(foreground.height*ratio)))
    foreground = foreground.filter(ImageFilter.GaussianBlur(radius=10))
    foreground.putalpha(200)
    image.paste(foreground, (0, -(foreground.height - 1080) // 2))
    image.paste(logo, (0,0), logo)


    font_size = 135
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Regular.ttf", font_size)     
    draw = ImageDraw.Draw(image)   
    fw, fh = draw.textsize(title, font=font)
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Regular.ttf", int(font_size * (900 / max(fw, 900))))
    fw, fh = draw.textsize(title, font=font)
    draw.text(
        (960-(fw/2), 540 - (fh/2)),
        title, 
        "white", 
        font=font, 
        align="center",
        # stroke_fill="black",
        # stroke_width=1
    )  
    image.save(outputFile)
    return outputFile