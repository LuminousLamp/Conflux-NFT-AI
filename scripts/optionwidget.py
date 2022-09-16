import tkinter
import tkinter.ttk
import tkinter.font
import ttkbootstrap
from ttkbootstrap import Style


class OptionWidget:
    def __init__(self, window, mode:str, name:str, label_text:str, initial_value = '', width:int = 15):
        self.name:str = name
        self.mode:str = mode
        self.option_frame = ttkbootstrap.Frame(window.frame_options)
        self.variable = ttkbootstrap.StringVar()
        self.variable.set(initial_value)
        self.input = ttkbootstrap.Entry(self.option_frame, textvariable=self.variable, width=width)
        # self.input = ttkbootstrap.ttk.Combobox(self.option_frame, bootstyle="default", width=16, state="readonly", values=combobox_parameter, textvariable=self.variable)
        self.input.bind('<Key>', self.inputStyle2Default)
        self.label = ttkbootstrap.Label(self.option_frame, text=label_text)

    
    def pack(self):
        self.label.pack(anchor=ttkbootstrap.N, padx=4,pady=0)
        self.input.pack(anchor=ttkbootstrap.N, padx=4,pady=4)
        self.option_frame.pack(anchor=ttkbootstrap.W,side=ttkbootstrap.LEFT, padx = 4, pady=4,)

    def pack_forget(self):
        self.label.pack_forget()
        self.input.pack_forget()
        self.option_frame.pack_forget()
    
    def inputStyle2Danger(self,*a):
        self.input.config(bootstyle='danger')
    
    def inputStyle2Default(self,*a):
        self.input.config(bootstyle='default')
    
    def getValue(self):
        return self.variable.get()
    
    def setValue(self, newvalue:str):
        self.variable.set(newvalue)

    def updateLabel(self, newlabel:str):
        self.label.config(text=newlabel)


class OptionWidget_C(OptionWidget):
    def __init__(self, window, mode:str, name:str, label_text:str, combobox_parameter:list[str], initial_value:str='', width:int=15, state:str='readonly'):
        super().__init__(window, mode, name, label_text, initial_value, width)
        self.parameter:str = combobox_parameter
        self.input = ttkbootstrap.ttk.Combobox(self.option_frame, bootstyle="default", width=width, state=state, values=combobox_parameter, textvariable=self.variable)
        self.input.bind('<<ComboboxSelected>>', self.inputStyle2Default)
    
    def setValue(self, newvalue:tuple[str]):
        self.input.config(values=newvalue)
        self.variable.set('')



class Mode:
    def __init__(self, window, name:str, style:str, index:int):
        self.name:str = name
        self.widgets:list[OptionWidget| OptionWidget_C] = []
        self.style:str = style
        self.index:int = index
        self.radiobutton = ttkbootstrap.Radiobutton(window.frame_mode_selection, text=name, value=self.index, variable=window.mode_selection_variable, command=lambda: window.switchMode(self))
        self.radiobutton.pack(anchor=ttkbootstrap.N, padx=4,pady=2)
        # self.mode_selection_button_default = ttkbootstrap.Radiobutton(self.frame_mode_selection, text='一般模式', value=0, variable=self.mode_selection_variable, command=self.toDefaultMode)
    
    def addWidget(self, widget:OptionWidget):
        self.widgets.append(widget)
    
    def addWidgets(self, widgets:list[OptionWidget]):
        self.widgets = self.widgets + widgets

    def pack(self):
        for widget in self.widgets:
            widget.pack()

    def pack_forget(self):
        for widget in self.widgets:
            widget.pack_forget()