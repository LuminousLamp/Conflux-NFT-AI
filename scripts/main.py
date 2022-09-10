import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.font
import os
import getImage
from ttkbootstrap import Style
import invokecontract
from PIL import Image, ImageTk

class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('AI生图')
        self.root.geometry('800x600')
        self.root.maxsize(800,600)
        self.root.minsize(800,600)
        self.style = Style(theme='darkly')
        self.frame1 = tkinter.Frame(self.root, )
        playerAddress = ''
        self.tokenURI = ''



        self.prompt = ''
        self.style = '油画'    
        self.apikey = 'AWla1UImVSbRhtNF7hE0VYv0fekwm9X2'
        self.secretkey = '7GB8HPKoV0GvzjyTPTReFffBSu9k93yd'


        options1 = ('中秋','国庆','春节')
        self.variable1 = tkinter.StringVar()
        self.variable1.set('选项1')
        self.optionMenu1 = tkinter.OptionMenu(self.frame1, self.variable1, *options1)
        
        options2 = ('月亮','2222','43534')
        self.variable2 = tkinter.StringVar()
        self.variable2.set('选项2')
        self.optionMenu2 = tkinter.OptionMenu(self.frame1, self.variable2, *options2)

        options3 = ('1','2222','43534')
        self.variable3 = tkinter.StringVar()
        self.variable3.set('选项3')
        self.optionMenu3 = tkinter.OptionMenu(self.frame1, self.variable3, *options3)

        options4 = ('水彩','油画','粉笔画','卡通','蜡笔画','儿童画','随机')
        self.variable4 = tkinter.StringVar()
        self.variable4.set('风格')
        self.optionMenu4 = tkinter.OptionMenu(self.frame1, self.variable4, *options4)


            
        self.button_makeImage = tkinter.Button(self.frame1, text = '画画' ,width=8, command = lambda : self.PrepareToGetImage(self))
        self.button_toChain = tkinter.Button(self.frame1, text='上链',width=8, command= lambda : self.ToChain(self))


        global imgOpen
        imgOpen = Image.open("LOGO.jpg")
        global img_png
        img_png = ImageTk.PhotoImage(imgOpen)
        self.label_img = tkinter.Label(self.root, text='asd',image=img_png, width=40, height=30)



        self.optionMenu1.pack(side=tkinter.LEFT, padx=5)
        self.optionMenu2.pack(side=tkinter.LEFT, padx=5)
        self.optionMenu3.pack(side=tkinter.LEFT, padx=5)
        self.optionMenu4.pack(side=tkinter.LEFT, padx=5)
        self.button_makeImage.pack()
        self.label_img.pack()
        self.frame1.pack()

    def PrepareToGetImage(self):
        self.prompt = self.variable1.get() + self.variable2.get() + self.variable3.get()
        self.style = self.variable4.get()
        getImage.GetImage(self.prompt, self.style, self.apikey, self.secretkey)

    def ToChain(self):
        invokecontract(self.playerAddress,self.tokenURI)



WD = Window()
tkinter.mainloop()
