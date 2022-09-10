import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.font
import os
import getImage


class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('AI生图')
        self.root.geometry('800x600')
        self.root.maxsize(800,600)
        self.root.minsize(800,600)
        
        self.frame1 = tkinter.Frame(self.root, )


        "2.4 2_and_4 选值框Spinbox（整型）"
        # 下面的部分制作一个可显示2（代表歌词中的to）或4的选值框
        # 使用选值框Spinbox控件：https://zhuanlan.zhihu.com/p/353831304
        self.to_default = tkinter.IntVar() # 创建一个整型变量（IntVar），用于Spinbox的textvariable属性
        self.to_default.set(4)
        self.to_spinbox = tkinter.ttk.Spinbox(self.frame1, wrap=False, from_=2, to=4,
                                      increment=2, textvariable=self.to_default)
        # /////Spinbox中的wrap属性可设置True或False，若设置为true，spinbox中的值可以循环
        # /////from_是范围的开始值（有下划线是因为避免与python的关键字冲突），to是末端值，increment是递增量
        # /////这里使用textvariable的目的是让程序打开时控件内就有一个初始值，如果不设置，控件内初始为空


        "2.5 know_or_not 下拉栏Combobox"
        # 下面的部分制作一个可选择 but I don't know 或 and so do I 文本的下拉栏
        # //////下拉栏控件的使用示例：https://blog.csdn.net/xoofly/article/details/89716839
        self.knowOrNot_variable = tkinter.StringVar()
        self.knowOrNot_box_values = ('but I don\'t know', 'and so do I')  # 用元组（或列表）的形式给下拉栏设定值
        self.knowOrNot_box = tkinter.ttk.Combobox(self.frame1,textvariable= self.knowOrNot_variable, values = self.knowOrNot_box_values)
        # /////values属性设置下拉栏的属性，值为一个列表或元组
        self.knowOrNot_box.current(0) # 设定初始值
        # /////XXX.current()方法设置初始时下拉栏文本框内显示的内容，参数为一个整数，表示第几个值

        options = ('1','2222','43534')
        self.variable = tkinter.StringVar()
        self.variable.set('请选择')
        self.optionMenu1 = tkinter.OptionMenu(self.frame1, self.variable, *options)
        
        text = ''
        style = ''    
        apikey = ''
        secretkey = ''    
        
        
        self.makeImage = tkinter.Button(self.frame1, text = '画画', command = lambda : getImage.getImage(text, style, apikey, secretkey))


        self.to_spinbox.pack()
        self.knowOrNot_box.pack()
        self.optionMenu1.pack()
        self.makeImage.pack()
        self.frame1.pack()

WD = Window()
tkinter.mainloop()
