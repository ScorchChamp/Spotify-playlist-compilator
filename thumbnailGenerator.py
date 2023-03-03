import os
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import datetime

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def wrapTitle(text):
    words = text.split()  # split the text into a list of words
    wrapped_text = ""     # initialize the wrapped text

    for i, word in enumerate(words):
        if i % 2 == 0 and i > 0:  # insert a newline after every 4th word
            wrapped_text += "\n"
        wrapped_text += word + " "  # add the word and a space to the wrapped text
    return wrapped_text

def generateThumbnail(thumbnailFile, title):
    title = wrapTitle(title)
    outputFile = thumbnailFile.replace(".png", "_thumbnail.png")
    image = Image.new(mode="RGBA", size=(1920,1080))
    foreground = Image.open(thumbnailFile).convert("RGBA")
    logo = Image.open('./assets/logoOpaque.png')
    ratio = 1080/foreground.height
    foreground = foreground.resize((int(foreground.width*ratio), int(foreground.height*ratio)))
    # foreground = foreground.filter(ImageFilter.GaussianBlur(radius=1))
    logo = logo.resize((1920,1080))
    foreground.putalpha(200)
    image.paste(foreground, (min(2200-foreground.width, 920), 0))
    image.paste(logo, (0,0), logo)


    font_size = 120
    font = ImageFont.truetype(f"{BASE_DIR}/title.ttf", font_size)     
    draw = ImageDraw.Draw(image)   
    fw, fh = draw.textsize(title, font=font)
    font = ImageFont.truetype(f"{BASE_DIR}/title.ttf", min(font_size, int(font_size * (900 / max(fw, 900)))))
    fw, fh = draw.textsize(title, font=font)
    draw.text(
        (480 - (fw/2)-5, 180 - (fh/2)+5),
        title, 
        "#ff00ff", 
        font=font, 
        align="center",
        # stroke_fill="black",
        # stroke_width=1
    )  
    draw.text(
        (480 - (fw/2), 180 - (fh/2)),
        title, 
        "white", 
        font=font, 
        align="center",
        # stroke_fill="black",
        # stroke_width=1
    )  

    date = datetime.datetime.now().strftime('%B %Y').replace(" ", "\n\n")
    font = ImageFont.truetype(f"{BASE_DIR}/title.ttf", 72)
    fw, fh = draw.textsize(date, font=font)
    draw.text(
        (480 - (fw/2)+5, 720 - (fh/2)-5),
        date,
        "#33ccff",
        font=font,
        align="center"
    )
    draw.text(
        (480 - (fw/2), 720 - (fh/2)),
        date,
        "white",
        font=font,
        align="center"
    )
    draw.line((480 - fw/1.5, 725, 480 + fw/1.5, 725), fill="#ff00ff", width=10)
    draw.line((490 - fw/1.5, 735, 490 + fw/1.5, 735), fill="cyan", width=10)
    draw.line((485 - fw/1.5, 730, 485 + fw/1.5, 730), fill="white", width=10)



    image.save(outputFile)
    image.show()
    return outputFile