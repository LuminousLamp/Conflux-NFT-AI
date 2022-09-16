from PIL import ImageFont, ImageDraw, Image
import tkinter
import tkinter.filedialog

def generateShareImage():

    image = Image.open("..\\util\\Background.jpg")
    logo = Image.open("..\\util\\AIPic.jpg")
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    layer.paste(logo, (50,60))
    out = Image.composite(layer, image, layer)


    path = tkinter.filedialog.askdirectory()
    if path != '':
        path = path.replace("/","\\")
    
    pathname = path + "\\share.png"
    out.save(pathname, "png")

    out.show()