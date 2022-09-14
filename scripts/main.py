from ensurepip import bootstrap
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.font
import os
import io
import getImage
import ttkbootstrap
from ttkbootstrap import Style
import invokecontract
from PIL import Image, ImageTk
import requests
import urllib
import threading
import webbrowser

class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('AI生图')
        self.root.geometry('750x500')
        self.root.maxsize(750,500)
        self.root.minsize(750,500)
        self.style = Style(theme='minty')

        ###############################
        # 顶框
        self.frame_root = ttkbootstrap.Frame(self.root)

        self.frame_top = ttkbootstrap.Frame(self.frame_root, )
        self.title = ttkbootstrap.Label(self.frame_top, text = '这是标题',font=('Copperplate Gothic Bold', 25))
        self.button_login = ttkbootstrap.Button(self.frame_top, text='登录', width = 8, command=self.login)
        self.userinfo_variable = ttkbootstrap.StringVar()
        self.userinfo_label = ttkbootstrap.Label(self.frame_top, textvariable=self.userinfo_variable)
        self.horizontal_line = ttkbootstrap.ttk.Separator(self.root, orient=ttkbootstrap.HORIZONTAL)

        ###############################
        # 选项框
        self.frame_options = ttkbootstrap.LabelFrame(self.frame_root, text='绘图选项')
        
        self.option1_parameter = ('中秋','国庆','春节')
        self.option1_variable = ttkbootstrap.StringVar()
        self.option1_variable.set('选项1')
        self.option1_combobox = ttkbootstrap.ttk.Combobox(self.frame_options, bootstyle="default", width=18)
        self.option1_combobox.config(state='readonly', values=self.option1_parameter, textvariable=self.option1_variable)
        self.option1_combobox.bind('<<ComboboxSelected>>', self.combobox1_off)

        self.option2_parameter = ('月亮','2222','43534')
        self.option2_variable = ttkbootstrap.StringVar()
        self.option2_variable.set('选项2')
        self.option2_combobox = ttkbootstrap.ttk.Combobox(self.frame_options, bootstyle="default", width=18)
        self.option2_combobox.config(state='readonly', values=self.option2_parameter, textvariable=self.option2_variable)

        self.option3_parameter = ('月亮','2222','43534')
        self.option3_variable = ttkbootstrap.StringVar()
        self.option3_variable.set('选项2')
        self.option3_combobox = ttkbootstrap.ttk.Combobox(self.frame_options, bootstyle="default", width=18)
        self.option3_combobox.config(state='readonly', values=self.option3_parameter, textvariable=self.option3_variable)

        self.option4_parameter = ('水彩','油画','粉笔画','卡通','蜡笔画','儿童画','随机')
        self.option4_variable = ttkbootstrap.StringVar()
        self.option4_variable.set('风格')
        self.option4_combobox = ttkbootstrap.ttk.Combobox(self.frame_options, bootstyle="default", width=18)
        self.option4_combobox.config(state='readonly', values=self.option4_parameter, textvariable=self.option4_variable)


        ###################################
        # 图片生成框
        self.frame_generate_and_share = ttkbootstrap.Frame(self.frame_root)
        self.frame_generate = ttkbootstrap.LabelFrame(self.frame_generate_and_share, text='生成')

        self.wenxinAK_label = ttkbootstrap.Label(self.frame_generate,text='输入API钥')
        self.wenxinSK_label = ttkbootstrap.Label(self.frame_generate,text='输入API私钥')
        self.wenxinAK_variable = ttkbootstrap.StringVar()
        self.wenxinSK_variable = ttkbootstrap.StringVar()
        self.wenxinAK_variable.set('AWla1UImVSbRhtNF7hE0VYv0fekwm9X2')
        self.wenxinSK_variable.set('7GB8HPKoV0GvzjyTPTReFffBSu9k93yd')
        self.wenxinAK_entry = ttkbootstrap.Entry(self.frame_generate, textvariable=self.wenxinAK_variable, width=30)
        self.wenxinSK_entry = ttkbootstrap.Entry(self.frame_generate, textvariable=self.wenxinSK_variable, width=30)
        self.wenxin_link = ttkbootstrap.Label(self.frame_generate, text='还没有API钥？生成', font=('Microsoft Yahei',9,'underline'))

        self.wenxin_link.bind('<Button-1>',self.open_url)

        self.button_makeImage = ttkbootstrap.Button(self.frame_generate, text = '创作图片！' ,width=12, command = self.start_thread)

        ####################################
        # 图片显示框
        self.frame_image = ttkbootstrap.LabelFrame(self.frame_root, text='结果')

        global imgOpen
        imgOpen = Image.open("LOGO.jpg")
        imgOpen = imgOpen.resize((400,300))
        global img_png
        img_png = ImageTk.PhotoImage(imgOpen)
        self.image = tkinter.Label(self.frame_image, image=img_png, width=300, height=300)
        self.hint_label = ttkbootstrap.Label(self.frame_image, text='当前无图片。')


        #######################################
        # 分享框
        self.frame_share = ttkbootstrap.LabelFrame(self.frame_generate_and_share, text='分享', )
        self.button_share = ttkbootstrap.Button(self.frame_share, text='分享',width=12, command= self.toChain, state = ttkbootstrap.DISABLED)

        ########################################
        # 其他参数
        self.prompt = ''
        self.style = '油画'
        self.wenxinApikey = 'AWla1UImVSbRhtNF7hE0VYv0fekwm9X2'
        self.wenxinSecretkey = '7GB8HPKoV0GvzjyTPTReFffBSu9k93yd'
        self.confluxSK_text = 'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x'

        self.imageURL = 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/350d8b4ff34aeb21e17182f3dcb6ef10a2'


        
        

       
        
        ###################################
        # 打包
        self.title.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.W, expand = True, pady = 5)
        self.button_login.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.E, pady=5)
        self.frame_top.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N, fill = ttkbootstrap.X,padx = 5, pady=5)
        
        self.option1_combobox.pack(side=ttkbootstrap.LEFT, padx=8, pady = 4)
        self.option2_combobox.pack(side=ttkbootstrap.LEFT, padx=8, pady = 4)
        self.option3_combobox.pack(side=ttkbootstrap.LEFT, padx=8, pady = 4)
        self.option4_combobox.pack(side=ttkbootstrap.LEFT, padx=8, pady = 4)
        self.frame_options.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N, fill = ttkbootstrap.X, padx = 5, pady=5, ipady=5)
        
        self.wenxinAK_label.pack(anchor=ttkbootstrap.NW, padx=15, pady = 0)
        self.wenxinAK_entry.pack( anchor=ttkbootstrap.NW, padx=15, pady = 4)
        self.wenxinSK_label.pack(anchor=ttkbootstrap.NW, padx=15, pady = 0)
        self.wenxinSK_entry.pack(anchor=ttkbootstrap.NW, padx=15, pady = 4)
        self.wenxin_link.pack(anchor=ttkbootstrap.NW, padx=15, pady = 4)
        self.button_makeImage.pack(anchor=ttkbootstrap.N, padx=15, pady = 4)
        self.frame_generate.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N,  padx = 5, pady=5, ipady = 10)

        self.button_share.pack(anchor=ttkbootstrap.CENTER, padx=80, pady = 20)
        self.frame_share.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.CENTER,  padx = 5, pady=5, ipady = 10)

        self.frame_generate_and_share.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.NW)

        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.frame_image.pack(side=ttkbootstrap.LEFT, anchor = ttkbootstrap.NE, fill = ttkbootstrap.BOTH, expand=True, padx = 5, pady=5)
        
        self.frame_root.pack(padx = 20, pady = 10)


    def combobox1_off(self, event):
        self.option1_combobox.config(bootstyle = 'default')
    def combobox2_off(self, event):
        self.option2_combobox.config(bootstyle = 'default')
    def combobox3_off(self, event):
        self.option3_combobox.config(bootstyle = 'default')
    def combobox4_off(self, event):
        self.option4_combobox.config(bootstyle = 'default')

        
    ##############################################
    def login(self):
        self.root.attributes("-disabled", 1)
        # 开设新窗口
        self.login_window = ttkbootstrap.Toplevel(self.root)
        self.login_window.title('登入')
        self.login_window.geometry('300x120')
        self.login_window.maxsize(300,120)
        self.login_window.minsize(300,120)
        self.login_window.focus_force()
        # 控件
        self.confluxSK_variable = ttkbootstrap.StringVar()
        self.frame_login_window = ttkbootstrap.Frame(self.login_window,)
        self.login_label = ttkbootstrap.Label(self.frame_login_window, text='输入Conflux账号Secret Key')
        self.login_entry = ttkbootstrap.Entry(self.frame_login_window, textvariable=self.confluxSK_variable, width=30)
        self.login_confirm_button = ttkbootstrap.Button(self.frame_login_window, text='确定',width=12, command= self.confirm_login)
        # 打包
        self.login_label.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_entry.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_confirm_button.pack(side=ttkbootstrap.TOP, pady=5)
        self.frame_login_window.pack(padx = 20, pady = 5)

        self.login_window.protocol('WM_DELETE_WINDOW',self.quitLoginWindow) 
    
    def confirm_login(self):
        if self.confluxSK_variable.get()!= '':
            self.confluxSK_text = self.confluxSK_variable.get()
            self.userinfo_variable.set('用户：'+self.confluxSK_text)
            self.userinfo_label.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.SE, pady=4)
            self.button_login.pack_forget()

            
        self.root.attributes("-disabled", 0)
        self.login_window.destroy()
    
    def quitLoginWindow(self):
        self.root.attributes("-disabled", 0)
        self.login_window.destroy()

    def open_url(event,a):
        webbrowser.open("https://wenxin.baidu.com/moduleApi/key", new=0)

    def prepareToGetImage(self):
        # 检查prompt和style设置是否正确，不正确则给反馈
        # 若正确，检查apikey和secretkey是否正确，不正确则给反馈，正确则继续
        # 执行函数，并给“等待"的反馈
        # 完成后显示图片，设置可点击上链
        # 最多造三次图

        # 获取几个参数

        self.prompt = self.option1_variable.get() +"， "+ self.option2_variable.get() +"， "+ self.option3_variable.get()
        self.style = self.option4_variable.get()
        self.wenxinApikey = self.wenxinAK_variable.get()
        self.wenxinSecretkey = self.wenxinSK_variable.get()

        if self.option1_variable.get() not in self.option1_parameter:
            self.option1_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return
        if self.option2_variable.get() not in self.option2_parameter:
            self.option2_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return
        if self.option3_variable.get() not in self.option3_parameter:
            self.option3_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return
        if self.option4_variable.get() not in self.option4_parameter:
            self.option4_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return
        if self.wenxinAK_variable.get() == '':
            self.wenxinAK_entry.config(bootstyle="danger")
            self.hint_label.config(text='请填写API钥！', bootstyle='danger')
            return
        if self.wenxinSK_variable.get() == '':
            self.wenxinSK_entry.config(bootstyle="danger")
            self.hint_label.config(text='请填写API密钥钥！', bootstyle='danger')
            return
        


        self.image.pack_forget()
        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.hint_label.config(text='图片生成中...', bootstyle='default')


        

        # 调用函数
        self.imageURL = getImage.GetImage(self.prompt, self.style, self.wenxinApikey, self.wenxinSecretkey)
        # imageURL = imageURL + '.jpg'
        # image_bytes=requests.get(imageURL).content
        # print('imageURL: ', imageURL)
        # image_bytes = urllib.request.urlopen(imageURL).read()
        # print('imageURL: ', imageURL)

        # data_stream = io.BytesIO(image_bytes)
        # print("datastream: ", data_stream)


        # getImage完成，打开图片
        self.hint_label.pack_forget()
        self.button_share.config(state='normal')
        global imgOpen2
        imgOpen2 = Image.open("..\\nft\\AIpic.jpg")
        imgOpen2 = imgOpen2.resize((400,300))
        global img_png2
        img_png2 = ImageTk.PhotoImage(imgOpen2)
        self.image['image'] = img_png2
        self.image.configure(image=img_png2)
        
        self.image.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4) #显示图片
        self.root.update()


    def toChain(self):
        #没生成图片的时候，就不能按下
        #生成图片后：
        #检查secretkey值是否合法，合法才执行
        #执行成功后给反馈
        # self.confluxSecretKey = self.inputConfluxSK_variable.get()
        invokecontract.invoke(self.confluxSK_text, self.imageURL)


    def start_thread(self):
    	# 使self.do_something函数在子线程中运行
        insert_data = threading.Thread(target=self.prepareToGetImage, args=())
        insert_data.start()


"////////////////////////////////////////////////"
imgOpen = None
img_png = None
imgOpen2 = None
img_png2 = None

if __name__ == "__main__":
    WD = Window()
    tkinter.mainloop()
