import tkinter
import tkinter.ttk
import tkinter.font
import os
import ttkbootstrap
from ttkbootstrap import Style
import re
from optionwidget import *
from about import *

class LoginWindow:
    def __init__(self,rootwindow):
        rootwindow.root.attributes("-disabled", 1)
        # 开设新窗口
        self.login_window = ttkbootstrap.Toplevel(rootwindow.root)
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
        self.login_confirm_button = ttkbootstrap.Button(self.frame_login_window, text='确定',width=12, command= lambda: self.confirmLogin(rootwindow))
        # 打包
        self.login_label.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_entry.pack(side=ttkbootstrap.TOP, pady=5)
        self.login_confirm_button.pack(side=ttkbootstrap.TOP, pady=5)
        self.frame_login_window.pack(padx = 20, pady = 5)
        # 绑定事件
        self.login_window.protocol('WM_DELETE_WINDOW',lambda : self.quitLoginWindow(rootwindow))
        self.login_entry.bind('<Key>', self.loginEntryChanged) 

    # 检测登录输入框文字变化
    def loginEntryChanged(self,event):
        self.login_entry.config(bootstyle='default')

    # 确认登录
    def confirmLogin(self, rootwindow):
        # 错误检查
        if self.getConfluxSK()== '':
            self.login_label.config(text='请输入密钥', bootstyle='danger')
            self.login_entry.config( bootstyle='danger')
            return
        
        if not self.checkConfluxSK(self.getConfluxSK()):
            self.login_label.config(text='密钥格式无效', bootstyle='danger')
            self.login_entry.config( bootstyle='danger')
            return

        # UI响应
        self.login_label.config(text='登录成功', bootstyle='success')
        rootwindow.userinfo_variable.set('用户：'+self.getConfluxSK()[0:6]+'...'+self.getConfluxSK()[-4:])
        rootwindow.userinfo_label.pack(side=ttkbootstrap.LEFT,anchor=ttkbootstrap.SW, pady=4)
        rootwindow.button_about.pack_forget()
        rootwindow.button_login.pack_forget()
        rootwindow.root.attributes("-disabled", 0)

        rootwindow.confluxSK_text = self.getConfluxSK()

        if os.path.exists('..\\util\\AIpic.jpg'):
            rootwindow.activateSharing()
        else:
            rootwindow.feedback_label.config(text='先创造一张作品吧！')
        
        self.login_window.destroy()
    
    # 匹配正则表达式
    def checkConfluxSK(self, string:str):
        sk_regex = r'(cfx|cfxtest)\:[\w]{42}$'
        if re.match(sk_regex, string):
            return True
        else:
            return False

    # 退出登录窗口
    def quitLoginWindow(self,rootwindow):
        rootwindow.root.attributes("-disabled", 0)
        self.login_window.destroy()

    def getConfluxSK(self):
        return self.confluxSK_variable.get()