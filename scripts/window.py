import tkinter
import tkinter.ttk
import tkinter.font
import os
import getImage
import ttkbootstrap
from ttkbootstrap import Style
import invokecontract
from PIL import Image, ImageTk, ImageSequence
import requests
import urllib
import threading
import webbrowser
import re
import random
import json
from optionwidget import *
from about import *
import share
import login



class Window:

    def __init__(self):
        ###############################
        # 基础参数
        with open('..\\util\\data.json','r',encoding='utf-8')as fp:
            data = json.load(fp)

            self.provided_keys = data["provided_keys"]
            self.style = data["style"]
            self.style_selected = None
            self.advanced_style = data["advanced_style"]
            self.advanced_style_adopted = None
            self.guide_text:str = data["guide_text"]
            self.guide_text_selected = None
            self.riddle = data["riddle"]
            self.autumn_element = data["autumn_element"]
            self.autumn_element_adopted1 = None
            self.autumn_element_adopted2 = None
        
        with open('..\\util\\animal.txt','r',encoding='utf-8')as fp2:
            self.animal:list[str] =[]
            alllines = fp2.readlines()
            for x in alllines:
                string = x[0:(x.find('\t'))]
                self.animal.append(string)
            self.animal_adopted = None


        self.prompt = None
        self.wenxinAK_text = None
        self.wenxinSK_text = None
        self.confluxSK_text = None
        #'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x'

        ###############################
        # 主窗口
        self.root = tkinter.Tk()
        self.root.title('芒了个盲NFT生成器')
        self.root.geometry('750x540')
        self.root.maxsize(750,540)
        self.root.minsize(750,540)

        ###############################
        # 顶框
        self.frame_root = ttkbootstrap.Frame(self.root)

        self.frame_top = ttkbootstrap.Frame(self.frame_root, )
        self.title = ttkbootstrap.Label(self.frame_top, text = '芒了个盲NFT生成器',font=('Microsoft Yahei', 25, 'bold'))
        self.button_login = ttkbootstrap.Button(self.frame_top, text='登录', width = 8, command=lambda : login.LoginWindow(self))
        self.button_about = ttkbootstrap.Button(self.frame_top, text='关于', width=8, command=lambda: AboutWindow(self, """芒了个盲NFT生成器 1.0.0\n陈一艺 陈栩颖 梁而道\n©2022"""))
        self.userinfo_variable = ttkbootstrap.StringVar()
        self.userinfo_label = ttkbootstrap.Label(self.frame_top, textvariable=self.userinfo_variable)
        self.horizontal_line = ttkbootstrap.ttk.Separator(self.root, orient=ttkbootstrap.HORIZONTAL)

        ###############################
        # 选项框
        self.frame_options = ttkbootstrap.LabelFrame(self.frame_root, text='绘图选项', bootstyle='primary')

        # 主选项：选择模式
        self.frame_mode_selection = ttkbootstrap.Frame(self.frame_options,)
        self.mode_selection_variable = ttkbootstrap.IntVar()
        self.mode_selection_dict = {0: 'default', 1: 'midautumn', 2:'diary'}
        self.mode_selection_variable.set(0)
        self.vertical_line = ttkbootstrap.ttk.Separator(self.frame_options, orient=ttkbootstrap.VERTICAL)

        
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
        global animation_photo
        animation_photo = ttkbootstrap.PhotoImage(file = "..\\util\\animation.gif")
        self.hint_animation = ttkbootstrap.Label(self.frame_image, image=animation_photo)


        #######################################
        # 分享框
        self.frame_share = ttkbootstrap.LabelFrame(self.frame_generate_and_share, text='上链', bootstyle='primary')
        self.frame_share_button = ttkbootstrap.Frame(self.frame_share)
        self.button_tochain = ttkbootstrap.Button(self.frame_share_button, text='铸造',width=12, command= self.toChain, state = ttkbootstrap.DISABLED)
        self.button_share = ttkbootstrap.Button(self.frame_share_button, text='分享', width=12, command= lambda: share.ShareWindow(self, self.mode_now), state=ttkbootstrap.DISABLED)
        self.feedback_label = ttkbootstrap.Label(self.frame_share, text='请先登录', bootstyle='secondary')

        ###################################
        # 打包
        "顶框"
        self.title.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.W, expand = True, pady = 5)
        self.button_login.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.E, padx=4,pady=5)
        self.button_about.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.E, padx=4,pady=5)
        self.frame_top.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.N, fill = ttkbootstrap.X,padx = 5, pady=5)

        "参数选择框"
        self.frame_mode_selection.pack(side=ttkbootstrap.LEFT, fill = ttkbootstrap.Y, padx = 4, pady=4, expand=True)
        self.vertical_line.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)
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
        self.button_tochain.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.CENTER, padx=10, pady = 5)
        self.button_share.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.CENTER, padx=10, pady = 5)
        self.frame_share_button.pack(anchor=ttkbootstrap.CENTER, padx=5, pady = 0)
        self.feedback_label.pack(anchor=ttkbootstrap.CENTER, padx=5, pady = 0)
        self.frame_share.pack(side=ttkbootstrap.TOP, anchor=ttkbootstrap.CENTER,  padx = 5, pady=5, ipady = 10)

        self.frame_generate_and_share.pack(side=ttkbootstrap.LEFT, anchor=ttkbootstrap.NW)

        "图片框"
        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.frame_image.pack(side=ttkbootstrap.LEFT, anchor = ttkbootstrap.NE, fill = ttkbootstrap.BOTH, expand=True, padx = 5, pady=5)
        
        self.frame_root.pack(padx = 20, pady = 10)


        ##############################
        # 控件相关
        self.mode_default = Mode(self,'一般模式','lumen',0)
        self.mode_autumn = Mode(self,'猜灯谜','united',1)
        self.mode_autumn2 = Mode(self, '团圆中秋','united',3)
        self.mode_diary = Mode(self,'心情日记', 'minty', 2)
        self.mode_list = [self.mode_default,self.mode_autumn,self.mode_diary, self.mode_autumn2]
        self.mode_now = None

        self.w_style = OptionWidget_C(self, 'global', 'style', '风格', self.style)
        self.w_advancedstyle = OptionWidget_C(self, 'global', 'advancedstyle', '进阶风格', self.advanced_style_adopted)
        self.w_guidedinput = OptionWidget(self, 'default', 'guidedinput', self.guide_text_selected,'',34)
        self.w_riddle = OptionWidget_C(self, 'autumn', 'riddle', '选一个灯谜！' , self.riddle,'',32)
        self.w_mood = OptionWidget(self,'diary', 'mood','一个词描述你的心情',)
        self.w_animal = OptionWidget_C(self,'diary','animal','你喜欢的动物', self.animal, state='normal')
        self.w_autumnelement1 = OptionWidget_C(self,'autumn2','autumnelement1','选一个中秋元素！',self.autumn_element_adopted1)
        self.w_autumnelement2 = OptionWidget_C(self,'autumn2','autumnelement2','选一个中秋元素！',self.autumn_element_adopted2)

        self.mode_default.addWidgets([self.w_style, self.w_advancedstyle, self.w_guidedinput])
        self.mode_autumn.addWidgets([self.w_style, self.w_advancedstyle, self.w_riddle])
        self.mode_diary.addWidgets([self.w_style, self.w_advancedstyle, self.w_mood, self.w_animal])
        self.mode_autumn2.addWidgets([self.w_style, self.w_advancedstyle, self.w_autumnelement1, self.w_autumnelement2])


        ###################################
        # 其他
        self.root.protocol('WM_DELETE_WINDOW',self.quitRootWindow)
        self.switchMode(self.selectModeByName(self.mode_default.name))
        self.updateParameters()


    ##############################################
    # 切换模式相关
    def switchMode(self, mode: Mode):
        if self.mode_now!= mode:
            rest = [x for x in self.mode_list if x.name != mode.name]

            for i in rest:
                i.pack_forget()
            mode.pack()
            self.updateParameters()
            self.mode_now = mode
            self.window_style = Style(theme=mode.style)
            self.root.update()

    def selectModeByIndex(self, index:int):
        selected = [x for x in self.mode_list if x.index == index][0]
        return selected

    def selectModeByName(self, name:str):
        selected = [x for x in self.mode_list if x.name == name][0]
        return selected


    ##############################################
    # 更新参数相关
    def updateParameters(self):
        self.selectAdvancedStyle()
        self.selectGuideText()
        self.selectAKSK()
        self.selectAnimal()
        self.selectAutumnElement()

    def selectAdvancedStyle(self):
        number = random.randint(4,6)
        self.advanced_style_adopted = ('无',) + tuple(random.sample(self.advanced_style, number))
        self.w_advancedstyle.setValue(self.advanced_style_adopted)

    def selectGuideText(self):
        self.guide_text_selected = random.choice(self.guide_text)
        self.w_guidedinput.updateLabel(self.guide_text_selected)

    
    def selectAKSK(self):
        selected_pair = random.choice(self.provided_keys)
        self.wenxinAK_text = selected_pair["ak"]
        self.wenxinSK_text = selected_pair["sk"]
        self.wenxinAK_variable.set(self.wenxinAK_text)
        self.wenxinSK_variable.set(self.wenxinSK_text)
    
    def selectAnimal(self):
        number = random.randint(8,10)
        self.animal_adopted = tuple(random.sample(self.animal, number))
        self.w_animal.setValue(self.animal_adopted)

    def selectAutumnElement(self):
        self.autumn_element_adopted1 = tuple(random.sample(self.autumn_element, 4))
        rest = [item for item in self.autumn_element if item not in set(self.autumn_element_adopted1)]
        self.autumn_element_adopted2 = tuple(random.sample(rest, 4))
        self.w_autumnelement1.setValue(self.autumn_element_adopted1)
        self.w_autumnelement2.setValue(self.autumn_element_adopted2)


    ##############################################
    # 图片生成相关
    def activateSharing(self):
        self.feedback_label.config(text='点击上链！',bootstyle='default')
        self.button_tochain.config(state=ttkbootstrap.NORMAL)
        self.button_share.config(state=ttkbootstrap.NORMAL)
    
    def disactivateSharing(self):
        self.hint_label.config(text='图片生成中...', bootstyle='default')
        self.button_tochain.config(state=ttkbootstrap.DISABLED)
        self.button_makeImage.config(state=ttkbootstrap.DISABLED)

    def generatePrompt(self):
        for widget in self.mode_now.widgets:
            if widget is OptionWidget_C:
                if widget.getValue() not in widget.paramater:
                    widget.input.config(bootstyle='danger')
                    self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
                    return
            else:
                if widget.getValue() == '':
                    widget.input.config(bootstyle='danger')
                    self.hint_label.config(text='请填写完整参数！', bootstyle='danger')
                    return
        
        selected_widgets = [widget for widget in self.mode_now.widgets if widget.name != '风格']
        keywordtuple = tuple(w.getValue() for w in selected_widgets)
        prompt = "，".join(keywordtuple)
        return prompt

    # 打开api链接
    def openUrl(event,a):
        webbrowser.open("https://wenxin.baidu.com/moduleApi/key", new=0)

    # 点击“生成”按钮之后的操作
    def onGenerateImage(self):

        prompt = self.generatePrompt()
        if prompt == None:
            return

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
        self.style_selected = self.w_style.getValue()
        self.wenxinAK_text = self.wenxinAK_variable.get()
        self.wenxinSK_text = self.wenxinSK_variable.get()
        
        # UI响应
        self.image.pack_forget()
        self.hint_label.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.progress_bar.pack(anchor=ttkbootstrap.CENTER, fill=ttkbootstrap.X, padx = 30,pady=4)
        self.progress_bar.start()
        self.hint_animation.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4)
        self.disactivateSharing()

        # 调用函数
        self.imageURL = getImage.GetImage(prompt, self.style_selected, self.wenxinAK_text, self.wenxinSK_text)

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

        # getImage完成，打开图片
        global imgOpen2, img_png2
        imgOpen2 = Image.open("..\\util\\AIpic.jpg").resize((300,300))
        img_png2 = ImageTk.PhotoImage(imgOpen2)
        self.image.configure(image=img_png2)

        # UI响应
        self.hint_label.pack_forget()
        self.progress_bar.pack_forget()
        self.image.pack(anchor = ttkbootstrap.CENTER, padx = 15,pady=4) 
        self.button_makeImage.config(state=ttkbootstrap.NORMAL)
        self.hint_animation.pack_forget()
        if self.confluxSK_text != None:
            self.activateSharing()
        
        self.root.update()
        self.updateParameters()

    # 打开多线程
    def start_thread(self):
    	# 使self.do_something函数在子线程中运行
        insert_data = threading.Thread(target=self.onGenerateImage, args=(), daemon=True)
        insert_data.start()
    

    ##############################################
    # 上链

    def toChain(self):
        try:
            result = invokecontract.invoke(self.confluxSK_text, self.imageURL)
            self.feedback_label.config(text='执行成功！',bootstyle='primary')
        except:
            self.feedback_label.config(text='执行失败',bootstyle='danger')

    
    def quitRootWindow(self):
        # 删除文件
        try:
            os.remove('..\\util\\AIpic.jpg')
        except:
            pass
        self.root.quit()

