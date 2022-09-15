import tkinter
import tkinter.ttk
import tkinter.font
import os
import getImage
import ttkbootstrap
from ttkbootstrap import Style
import invokecontract
from PIL import Image, ImageTk
import requests
import urllib
import threading
import webbrowser
import re
import random


class Window:
    def __init__(self):
        ###############################
        # 基础参数
        self.provided_keys = ({"ak":"AWla1UImVSbRhtNF7hE0VYv0fekwm9X2","sk":"7GB8HPKoV0GvzjyTPTReFffBSu9k93yd"},
            {"ak":"koxjmqRUOeBvIxKHdo94aHuehbUSNdbd","sk":"VM6eMck4R25wgYG5xVxNdI91KTKIYdU4"},
            {"ak":"KsWEIIQq1QhQ9iaCjKOeG3i4H9TyBDGB","sk":"gGj4GCRW0S37o649f3NIOUmZ9v8okclw"},
            {"ak":"ezem375HQDvMc80rRDftOqA16fOSgtfW","sk":"49Fs8nTgcnSqPajdcpDbuSr7pA9xNIHs"},
            {"ak":"E9cwReHYyOyaxuQf5qgAteo1One3h3sw","sk":"e0PePV3MMMvzBY1qOwdVofoI13yztmUo"},
            {"ak":"xyCUpoaiewGuYtsWwV1jumGfrDCHFdXi","sk":"IDQnNCEgycyanLU8dRDbKuHcr9c6aCAC"})
        self.style = ('水彩','油画','粉笔画','卡通','蜡笔画','儿童画','随机')
        self.style_selected = None
        self.advanced_style = ('概念艺术','像素艺术','包豪斯艺术','蒸汽波艺术','故障艺术','素人主义','女巫店风格','维京人风格','矢量心风格','浮世绘风格','史前遗迹风格','立体主义风格','未来主义风格','古埃及风格','复古海报风','港风','抽象技术风格')
        self.advanced_style_adopted = None
        self.guide_text = ('请输入你抬头看到的一件事','请输入你抬头左转看到的第一件物品','找到微信第一位好友！请TA提供一个元素','最近一顿吃了什么？','恭喜你获得一次传送机会！你想去……')
        self.guide_text_selected = None
        self.riddle = ('春色满园十五夜','十五月亮照海滩','大鹏展翅腾九霄')


        self.prompt = None
        self.wenxinAK_text = None
        self.wenxinSK_text = None
        self.confluxSK_text = None


        #'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x'

        ###############################
        # 主窗口
        self.root = tkinter.Tk()
        self.root.title('AI生图')
        self.root.geometry('750x520')
        self.root.maxsize(750,520)
        self.root.minsize(750,520)
        self.window_style = Style(theme='lumen')

        ###############################
        # 顶框
        self.frame_root = ttkbootstrap.Frame(self.root)

        self.frame_top = ttkbootstrap.Frame(self.frame_root, )
        self.title = ttkbootstrap.Label(self.frame_top, text = '绷不住了',font=('Copperplate Gothic Bold', 25))
        self.button_login = ttkbootstrap.Button(self.frame_top, text='登录', width = 8, command=self.onLogin)
        self.button_about = ttkbootstrap.Button(self.frame_top, text='关于', width=8, command=self.onAbout)
        self.userinfo_variable = ttkbootstrap.StringVar()
        self.userinfo_label = ttkbootstrap.Label(self.frame_top, textvariable=self.userinfo_variable)
        self.horizontal_line = ttkbootstrap.ttk.Separator(self.root, orient=ttkbootstrap.HORIZONTAL)

        ###############################
        # 选项框

        self.frame_options = ttkbootstrap.LabelFrame(self.frame_root, text='绘图选项', bootstyle='primary')

        # 选项1：默认/中秋
        self.frame_mode_selection = ttkbootstrap.Frame(self.frame_options,)

        self.mode_selection_variable = ttkbootstrap.IntVar()
        self.mode_selection_dict = {0: 'default', 1: 'midautumn'}
        self.mode_selection_variable.set(0)
        self.mode_selection_button_default = ttkbootstrap.Radiobutton(self.frame_mode_selection, text='一般模式', value=0, variable=self.mode_selection_variable, command=self.toDefaultMode)
        self.mode_selection_button_midautumn = ttkbootstrap.Radiobutton(self.frame_mode_selection, text='中秋专栏', value=1, variable=self.mode_selection_variable, command=self.toMidAutumnMode)
        self.mode_selection_label = ttkbootstrap.Label(self.frame_mode_selection, text='选择模式')

        self.vertical_line = ttkbootstrap.ttk.Separator(self.frame_options, orient=ttkbootstrap.VERTICAL)

        # 风格选择
        self.frame_style = ttkbootstrap.Frame(self.frame_options,)

        self.style_variable = ttkbootstrap.StringVar()
        self.style_variable.set('-')
        self.style_combobox = ttkbootstrap.ttk.Combobox(self.frame_style, bootstyle="default", width=18)
        self.style_combobox.config(state='readonly', values=self.style, textvariable=self.style_variable)
        self.style_combobox.bind('<<ComboboxSelected>>', self.styleCombobox_off)
        self.style_label = ttkbootstrap.Label(self.frame_style, text='风格')

        # 进阶风格
        self.frame_advanced_style = ttkbootstrap.Frame(self.frame_options,)

        self.advanced_style_variable = ttkbootstrap.StringVar()
        self.advanced_style_variable.set('-')
        self.advanced_style_combobox = ttkbootstrap.ttk.Combobox(self.frame_advanced_style, bootstyle="default", width=18)
        self.advanced_style_combobox.config(state='readonly', values=self.advanced_style_adopted, textvariable=self.advanced_style_variable)
        self.advanced_style_combobox.bind('<<ComboboxSelected>>', self.advancedStyleCombobox_off)
        self.advanced_style_label = ttkbootstrap.Label(self.frame_advanced_style, text='进阶风格')

        # （默认模式）自由输入
        self.frame_free_input = ttkbootstrap.Frame(self.frame_options,)

        self.free_input_variable = ttkbootstrap.StringVar()
        self.free_input_entry = ttkbootstrap.Entry(self.frame_free_input, textvariable=self.free_input_variable, width=30)
        self.free_input_label = ttkbootstrap.Label(self.frame_free_input, text=self.guide_text_selected)
        self.free_input_entry.bind('<Key>', self.freeInputEntry_off)

        # （中秋模式）谜语
        self.frame_riddle = ttkbootstrap.Frame(self.frame_options,)
        self.riddle_variable = ttkbootstrap.StringVar()
        self.riddle_variable.set('-')
        self.riddle_combobox = ttkbootstrap.ttk.Combobox(self.frame_riddle, bootstyle="default")
        self.riddle_combobox.config(state='readonly', values=self.riddle, textvariable=self.riddle_variable, width=28)
        self.advanced_style_combobox.bind('<<ComboboxSelected>>', self.riddleCombobox_off)
        self.riddle_label = ttkbootstrap.Label(self.frame_riddle, text='选一个灯谜！')
        
        ###################################
        # 图片生成框
        self.frame_generate_and_share = ttkbootstrap.Frame(self.frame_root)
        self.frame_generate = ttkbootstrap.LabelFrame(self.frame_generate_and_share, text='生成', bootstyle='primary')

        self.wenxinAK_label = ttkbootstrap.Label(self.frame_generate,text='输入API钥')
        self.wenxinSK_label = ttkbootstrap.Label(self.frame_generate,text='输入API私钥')
        self.wenxinAK_variable = ttkbootstrap.StringVar()
        self.wenxinSK_variable = ttkbootstrap.StringVar()
        self.wenxinAK_entry = ttkbootstrap.Entry(self.frame_generate, textvariable=self.wenxinAK_variable, width=30)
        self.wenxinSK_entry = ttkbootstrap.Entry(self.frame_generate, textvariable=self.wenxinSK_variable, width=30)
        self.wenxin_link = ttkbootstrap.Label(self.frame_generate, text='还没有API钥？生成', font=('Microsoft Yahei',9,'underline'))

        self.wenxin_link.bind('<Button-1>',self.openUrl)

        self.button_makeImage = ttkbootstrap.Button(self.frame_generate, text = '创作图片！' ,width=12, command = self.start_thread)

        ####################################
        # 图片显示框
        self.frame_image = ttkbootstrap.LabelFrame(self.frame_root, text='结果', bootstyle='primary')

        self.image = tkinter.Label(self.frame_image, width=300, height=300)
        self.progress_variable = ttkbootstrap.IntVar()
        self.progress_bar = ttkbootstrap.Progressbar(self.frame_image, orient=ttkbootstrap.HORIZONTAL, mode='indeterminate', maximum=100,bootstyle='primary', value=80)
        self.hint_label = ttkbootstrap.Label(self.frame_image, text='当前无图片。')


        #######################################
        # 分享框
        self.frame_share = ttkbootstrap.LabelFrame(self.frame_generate_and_share, text='分享', bootstyle='primary')
        self.button_share = ttkbootstrap.Button(self.frame_share, text='分享',width=12, command= self.toChain, state = ttkbootstrap.DISABLED)

        ###################################
        # 打包
        "顶框"
        self.title.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.W, expand = True, pady = 5)
        self.button_login.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.E, padx=4,pady=5)
        self.button_about.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.E, padx=4,pady=5)
        self.frame_top.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N, fill = ttkbootstrap.X,padx = 5, pady=5)

        "参数选择框"
        self.mode_selection_label.pack(anchor=ttkbootstrap.N, padx=4,pady=2)
        self.mode_selection_button_default.pack(anchor=ttkbootstrap.N, padx=4,pady=2)
        self.mode_selection_button_midautumn.pack(anchor=ttkbootstrap.N, padx=4,pady=2)
        self.frame_mode_selection.pack(side=ttkbootstrap.LEFT, fill = ttkbootstrap.Y, padx = 4, pady=4, expand=True)

        self.vertical_line.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)

        self.style_label.pack(anchor=ttkbootstrap.N, padx=4,pady=0)
        self.style_combobox.pack(anchor=ttkbootstrap.N, padx=4,pady=4)
        self.frame_style.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)

        self.advanced_style_label.pack(anchor=ttkbootstrap.N, padx=4,pady=0)
        self.advanced_style_combobox.pack(anchor=ttkbootstrap.N, padx=4,pady=4)
        self.frame_advanced_style.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)

        self.showDefaultMode()
        self.frame_options.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N, fill = ttkbootstrap.X, padx = 5, pady=5, )

        "图片生成框"
        self.wenxinAK_label.pack(anchor=ttkbootstrap.NW, padx=15, pady = 2)
        self.wenxinAK_entry.pack( anchor=ttkbootstrap.N, padx=15, pady = 2)
        self.wenxinSK_label.pack(anchor=ttkbootstrap.NW, padx=15, pady = 2)
        self.wenxinSK_entry.pack(anchor=ttkbootstrap.N, padx=15, pady = 4)
        self.wenxin_link.pack(anchor=ttkbootstrap.NW, padx=15, pady = 4)
        self.button_makeImage.pack(anchor=ttkbootstrap.N, padx=15, pady = 2)
        self.frame_generate.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N,  padx = 5, pady=5, ipady = 10, fill=tkinter.X)

        "分享框"
        self.button_share.pack(anchor=ttkbootstrap.CENTER, padx=80, pady = 20)
        self.frame_share.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.CENTER,  padx = 5, pady=5, ipady = 10)
        self.frame_generate_and_share.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.NW)

        "图片框"
        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.frame_image.pack(side=ttkbootstrap.LEFT, anchor = ttkbootstrap.NE, fill = ttkbootstrap.BOTH, expand=True, padx = 5, pady=5)
        
        self.frame_root.pack(padx = 20, pady = 10)

        ###################################
        # 事件绑定
        self.root.protocol('WM_DELETE_WINDOW',self.quitRootWindow)
        self.updateParameters()

    
    #############################################
    # 切换模式

    def toDefaultMode(self):

        self.window_style = Style(theme='lumen')
        self.hideAutumnMode()
        self.showDefaultMode()
        self.updateParameters()

    def toMidAutumnMode(self):
        self.window_style = Style(theme='united')
        self.hideDefaultMode()
        self.showAutumnMode()
        self.updateParameters()

    def hideAutumnMode(self):
        self.riddle_combobox.pack_forget()
        self.riddle_label.pack_forget()
        self.frame_riddle.pack_forget()

    def hideDefaultMode(self):
        self.free_input_label.pack_forget()
        self.free_input_entry.pack_forget()
        self.frame_free_input.pack_forget()

    def showDefaultMode(self):
        self.free_input_label.pack(anchor=ttkbootstrap.N, padx=4,pady=0)
        self.free_input_entry.pack(anchor=ttkbootstrap.N, padx=4,pady=4)
        self.frame_free_input.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)
        
    def showAutumnMode(self):
        self.riddle_label.pack(anchor=ttkbootstrap.N, padx=4,pady=0)
        self.riddle_combobox.pack(anchor=ttkbootstrap.N, padx=4,pady=4)
        self.frame_riddle.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)
        
        

    ##############################################
    # 选择相关
    def updateParameters(self):
        self.selectAdvancedStyle()
        self.selectGuideText()
        self.selectAKSK()

    def selectAdvancedStyle(self):
        number = random.randint(4,6)
        self.advanced_style_adopted = ('无',) + tuple(random.sample(self.advanced_style, number))
        self.advanced_style_combobox.config(values=self.advanced_style_adopted)

    def selectGuideText(self):
        self.guide_text_selected = random.choice(self.guide_text)
        self.free_input_label.config(text=self.guide_text_selected)
    
    def selectAKSK(self):
        selected_pair = random.choice(self.provided_keys)
        self.wenxinAK_text = selected_pair["ak"]
        self.wenxinSK_text = selected_pair["sk"]
        self.wenxinAK_variable.set(self.wenxinAK_text)
        self.wenxinSK_variable.set(self.wenxinSK_text)


    def onAbout(self):
        self.root.attributes("-disabled", 1)
        # 开设新窗口
        self.about_window = ttkbootstrap.Toplevel(self.root)
        self.about_window.title('关于')
        self.about_window.geometry('300x120')
        self.about_window.maxsize(300,120)
        self.about_window.minsize(300,120)
        self.about_window.focus_force()
        # 控件
        about_text = """绷不住了 1.0.0\n陈一艺 陈栩颖 梁而道\n©2022"""

        self.frame_about_window =ttkbootstrap.Frame(self.about_window,)
        self.about_title_label = ttkbootstrap.Label(self.frame_about_window, text='关于',bootstyle='primary',font=('Microsoft Yahei',12))
        self.about_label = ttkbootstrap.Label(self.frame_about_window, text=about_text, bootstyle='default')
        # 打包
        self.about_title_label.pack(padx=5,pady=4)
        self.about_label.pack(padx=5,pady=4)
        self.frame_about_window.pack(padx=5,pady=4)



        self.about_window.protocol('WM_DELETE_WINDOW',self.quitAboutWindow)
        

    def quitAboutWindow(self):
        self.root.attributes("-disabled", 0)
        self.about_window.destroy()
    
    ##############################################
    # 登入相关

    # 登录界面
    def onLogin(self):
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
        self.login_label = ttkbootstrap.Label(self.frame_login_window, text='输入Conflux账号', bootstyle = 'default')
        self.login_entry = ttkbootstrap.Entry(self.frame_login_window, textvariable=self.confluxSK_variable, width=30, show ="*")
        self.login_confirm_button = ttkbootstrap.Button(self.frame_login_window, text='确定',width=12, command= self.confirmLogin)
        # 打包
        self.login_label.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_entry.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_confirm_button.pack(side=ttkbootstrap.TOP, pady=5)
        self.frame_login_window.pack(padx = 20, pady = 5)
        # 绑定事件
        self.login_window.protocol('WM_DELETE_WINDOW',self.quitLoginWindow)
        self.login_entry.bind('<Key>', self.loginEntryChanged) 

    # 检测登录输入框文字变化
    def loginEntryChanged(self,event):
        self.login_entry.config(bootstyle='default')

    # 确认登录
    def confirmLogin(self):
        self.confluxSK_text = self.confluxSK_variable.get()
        if self.confluxSK_variable.get()== '':
            self.login_label.config(text='请输入密钥', bootstyle='danger')
            self.login_entry.config( bootstyle='danger')
            return
        
        if not self.checkConfluxSK():
            self.login_label.config(text='密钥格式无效', bootstyle='danger')
            self.login_entry.config( bootstyle='danger')
            return

        self.login_label.config(text='登录成功', bootstyle='success')
        self.userinfo_variable.set('用户：'+self.confluxSK_text[0:6]+'...'+self.confluxSK_text[-4:])
        self.userinfo_label.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.SE, pady=4)
        self.button_login.pack_forget()
        self.root.attributes("-disabled", 0)
        self.login_window.destroy()
    
    # 匹配正则表达式
    def checkConfluxSK(self):
        sk_regex = r'(cfx|cfxtest)\:[\w]{42}$'
        if re.match(sk_regex, self.confluxSK_text):
            return True
        else:
            return False

    # 退出登录窗口
    def quitLoginWindow(self):
        self.root.attributes("-disabled", 0)
        self.login_window.destroy()


    ##############################################
    # 图片生成相关

    # 打开api链接
    def openUrl(event,a):
        webbrowser.open("https://wenxin.baidu.com/moduleApi/key", new=0)

    # 点击“生成”按钮之后的操作
    def onGenerateImage(self):

        mode = self.mode_selection_dict[self.mode_selection_variable.get()]

        # 检查通用参数正确性
        if self.style_variable.get() not in self.style or self.style_variable.get()=='':
            self.style_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return
        if self.advanced_style_variable.get() not in self.advanced_style_adopted or self.advanced_style_variable.get()=='':
            self.advanced_style_combobox.config(bootstyle="danger")
            self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
            return

        # 检查特定参数正确性 + 获取参数
        if mode == 'default':
            if self.free_input_variable.get()=='':
                self.free_input_entry.config(bootstyle="danger")
                self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
                return
            self.prompt = self.free_input_entry.get() +"， "+ self.advanced_style_variable.get()
        
        elif mode == 'midautumn':
            if self.riddle_variable.get() not in self.riddle or self.riddle_variable.get()=='':
                self.riddle_combobox.config(bootstyle="danger")
                self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
                return
            self.prompt = self.riddle_variable.get() +"， "+ self.advanced_style_variable.get()

        # 检查key参数
        if self.wenxinAK_variable.get() == '':
            self.wenxinAK_entry.config(bootstyle="danger")
            self.hint_label.config(text='请填写API钥！', bootstyle='danger')
            return
        if self.wenxinSK_variable.get() == '':
            self.wenxinSK_entry.config(bootstyle="danger")
            self.hint_label.config(text='请填写API密钥！', bootstyle='danger')
            return

        # 获取几个参数
        self.style_selected = self.style_variable.get()
        self.wenxinAK_text = self.wenxinAK_variable.get()
        self.wenxinSK_text = self.wenxinSK_variable.get()
        
        # UI响应
        self.image.pack_forget()
        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.progress_bar.pack(anchor=ttkbootstrap.CENTER, fill=ttkbootstrap.X, padx = 30,pady=4)
        self.progress_bar.start()
        self.hint_label.config(text='图片生成中...', bootstyle='default')

        # 调用函数
        self.imageURL = getImage.GetImage(self.prompt, self.style_selected, self.wenxinAK_text, self.wenxinSK_text)

        # 错误处理
        if self.imageURL == 'APIError':
            self.hint_label.config(text='API无效。', bootstyle='danger')
            return
        if self.imageURL == 'APIConnectionError':
            self.hint_label.config(text='网络连接错误，请检查是否联网。', bootstyle='danger')
            return
        elif self.imageURL == 'error':
            self.hint_label.config(text='生成图片出错。', bootstyle='danger')
            return

        # imageURL = imageURL + '.jpg'
        # image_bytes=requests.get(imageURL).content
        # print('imageURL: ', imageURL)
        # image_bytes = urllib.request.urlopen(imageURL).read()
        # print('imageURL: ', imageURL)

        # data_stream = io.BytesIO(image_bytes)
        # print("datastream: ", data_stream)

        # getImage完成，打开图片
        self.button_share.config(state='normal')
        global imgOpen2
        imgOpen2 = Image.open("..\\nft\\AIpic.jpg")
        imgOpen2 = imgOpen2.resize((400,300))
        global img_png2
        img_png2 = ImageTk.PhotoImage(imgOpen2)
        self.image['image'] = img_png2
        self.image.configure(image=img_png2)

        # UI响应
        self.hint_label.pack_forget()
        self.progress_bar.pack_forget()
        self.image.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4) 
        self.root.update()
        self.updateParameters()

    # 打开多线程
    def start_thread(self):
    	# 使self.do_something函数在子线程中运行
        insert_data = threading.Thread(target=self.onGenerateImage, args=())
        insert_data.start()
    

    ##############################################
    # 上链
    def toChain(self):
        #执行成功后给反馈
        # self.confluxSecretKey = self.inputConfluxSK_variable.get()
        result = invokecontract.invoke(self.confluxSK_text, self.imageURL)



    ##############################################
    # 其他
    
    def styleCombobox_off(self, event):
        self.style_combobox.config(bootstyle = 'default')
    def advancedStyleCombobox_off(self, event):
        self.advanced_style_combobox.config(bootstyle = 'default')
    def freeInputEntry_off(self, event):
        self.free_input_entry.config(bootstyle = 'default')
    def riddleCombobox_off(self, event):
        self.riddle_combobox.config(bootstyle = 'default')
    
    def quitRootWindow(self):
        # 删除文件
        try:
            os.remove('..\\nft\\AIpic.jpg')
        except:
            pass
        self.root.quit()


"////////////////////////////////////////////////"
imgOpen = None
img_png = None
imgOpen2 = None
img_png2 = None

if __name__ == "__main__":
    WD = Window()
    tkinter.mainloop()
