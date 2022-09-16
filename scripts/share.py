from PIL import ImageFont, ImageDraw, Image, ImageTk
import tkinter
import tkinter.filedialog
import ttkbootstrap
from optionwidget import Mode


class ShareWindow:
    def __init__(self, rootwindow, mode:Mode):
        rootwindow.root.attributes("-disabled", 1)
        self.share_window = ttkbootstrap.Toplevel(rootwindow.root)
        self.share_window.title('分享')
        self.share_window.geometry('300x120')
        self.share_window.maxsize(300,450)
        self.share_window.minsize(300,450)
        self.share_window.focus_force()

        global imgOpen3
        global img_png3

        imgOpen3 = self.generateShareImage(mode, rootwindow.confluxSK_text)
        self.out = imgOpen3
        imgOpen3 = imgOpen3.resize((250,333))
        img_png3 = ImageTk.PhotoImage(imgOpen3)

        
        self.frame_share_window =ttkbootstrap.Frame(self.share_window,)
        self.about_title_label = ttkbootstrap.Label(self.frame_share_window, text='分享',bootstyle='primary',font=('Microsoft Yahei',12))
        self.share_label = ttkbootstrap.Label(self.frame_share_window,  bootstyle='default')
        self.button_save = ttkbootstrap.Button(self.frame_share_window, text='保存图片', width=12, bootstyle='default', command=self.saveShareImage)
        self.share_label['image'] = img_png3
        self.share_label.configure(image=img_png3)

        # 打包
        self.about_title_label.pack(padx=5,pady=4)
        self.share_label.pack(padx=5,pady=4)
        self.button_save.pack(padx=5,pady=4)
        self.frame_share_window.pack(padx=5,pady=4)
        self.share_window.protocol('WM_DELETE_WINDOW',lambda: self.quitShareWindow(rootwindow))


    def quitShareWindow(self, rootwindow):
        rootwindow.root.attributes("-disabled", 0)
        self.share_window.destroy()

    def generateShareImage(self, mode:Mode, owner):
        
        text_title = mode.name
        text_owner = owner[0:12]+'...'+owner[-6:]

        image = Image.open("..\\util\\Background.png")
        logo = Image.open("..\\util\\AIPic.jpg").resize((580,580))
        layer = Image.new('RGBA', image.size, (0,0,0,0))
        layer.paste(logo, (85,190))
        pre_out = Image.composite(layer, image, layer)

        txt1=Image.new('RGBA', image.size, (0,0,0,0))
        txt2=Image.new('RGBA', image.size, (0,0,0,0))
        font1=ImageFont.truetype(font="C:\\Windows\\Fonts\\msyhbd.ttc", size=60, encoding='utf-8')
        font2=ImageFont.truetype(font="C:\\Windows\\Fonts\\msyh.ttc", size=25, encoding='utf-8')
        
        draw_title=ImageDraw.Draw(txt1)
        draw_title.text((270, 90), text_title, font=font1, fill='black')
        pre_out=Image.alpha_composite(pre_out, txt1)
        draw_owner=ImageDraw.Draw(txt2)
        draw_owner.text((190,810), text_owner, font=font2, fill='black')
        out = Image.alpha_composite(pre_out, txt2)

        return out

    def saveShareImage(self):
        path = tkinter.filedialog.askdirectory()
        if path != '':
            path = path.replace("/","\\")
        
        pathname = path + "\\share.png"
        self.out.save(pathname, "png")

        self.out.show()




imgOpen3 = None
img_png3 = None
