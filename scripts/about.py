import tkinter
import tkinter.ttk
import tkinter.font
import ttkbootstrap
from ttkbootstrap import Style

class AboutWindow:
    def __init__(self, rootwindow, text):
        rootwindow.root.attributes("-disabled", 1)
        self.about_window = ttkbootstrap.Toplevel(rootwindow.root)
        self.about_window.title('关于')
        self.about_window.geometry('300x120')
        self.about_window.maxsize(300,120)
        self.about_window.minsize(300,120)
        self.about_window.focus_force()

        self.frame_about_window =ttkbootstrap.Frame(self.about_window,)
        self.about_title_label = ttkbootstrap.Label(self.frame_about_window, text='关于',bootstyle='primary',font=('Microsoft Yahei',12))
        self.about_label = ttkbootstrap.Label(self.frame_about_window, text=text, bootstyle='default')
        # 打包
        self.about_title_label.pack(padx=5,pady=4)
        self.about_label.pack(padx=5,pady=4)
        self.frame_about_window.pack(padx=5,pady=4)

        self.about_window.protocol('WM_DELETE_WINDOW',lambda: self.quitAboutWindow(rootwindow))


    def quitAboutWindow(self, rootwindow):
        rootwindow.root.attributes("-disabled", 0)
        self.about_window.destroy()
