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
    width, height = 1920, 1080
    title = wrapTitle(title)
    outputFile = thumbnailFile.replace(".png", "_thumbnail.png")
    image = Image.new(mode="RGBA", size=(width,height))
    foreground = Image.open(thumbnailFile).convert("RGBA")
    logo = Image.open('./assets/logoOpaque.png')
    ratio = max(width/foreground.width, height/foreground.height)
    foreground = foreground.resize((int(foreground.width*ratio), int(foreground.height*ratio)))
    foreground = foreground.filter(ImageFilter.GaussianBlur(radius=10))
    foreground.putalpha(200)
    image.paste(foreground, (0, -(foreground.height - height) // 2))


    font_size = 135
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Regular.ttf", font_size)     
    draw = ImageDraw.Draw(image)   
    fw, fh = draw.textsize(title, font=font)
    font = ImageFont.truetype(f"{BASE_DIR}/Roboto-Regular.ttf", int(font_size * ((width/2) / max(fw, (width/2)))))
    fw, fh = draw.textsize(title, font=font)
    draw.text(
        ((width/2)-(fw/2), (height/2) - (fh/2)),
        title, 
        "white", 
        font=font, 
        align="center",
        # stroke_fill="black",
        # stroke_width=1
    )  
    padding = 100
    stroke_width = 7
    draw.line(((width/2)-(fw/2) - padding, (height/2) - (fh/2) + padding, (width/2) - (fw/2) - padding, (height/2) + (fh/2) + padding), fill="white", width=stroke_width)
    draw.line(((width/2)+(fw/2) + padding, (height/2) - (fh/2) - padding, (width/2) + (fw/2) + padding, (height/2) + (fh/2) - padding), fill="white", width=stroke_width)
    # horizontal lines
    draw.line(((width/2)-(fw/2) + padding, (height/2) - (fh/2) - padding, (width/2) + (fw/2) + padding, (height/2) - (fh/2) - padding), fill="white", width=stroke_width)
    draw.line(((width/2)-(fw/2) - padding, (height/2) + (fh/2) + padding, (width/2) + (fw/2) - padding, (height/2) + (fh/2) + padding), fill="white", width=stroke_width)

    # draw diagonal lines in corner of image
    corner_padding = padding * 2.5
    draw.line((corner_padding, 0, 0, corner_padding), fill="white", width=stroke_width)
    draw.line((width - corner_padding, height, width, height - corner_padding), fill="white", width=stroke_width)
    draw.line((width - corner_padding, 0, width, corner_padding), fill="white", width=stroke_width)
    draw.line((corner_padding, height, 0, height - corner_padding), fill="white", width=stroke_width)
    image.paste(logo, (0,0), logo)

    image.save(outputFile)
    return outputFile