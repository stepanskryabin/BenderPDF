#!/usr/bin/python
# -*- coding:utf -8 -*-
__version__ = 'Версия: 0.0.3'

from tkinter import Tk
from mainframe import MainFrame

# main window
root = Tk()
root.geometry('700x420+0-50')
root.iconbitmap('bender.ico')
root.title('Конвертер изображений для ГИС ЖКХ. ' + __version__)
app = MainFrame(root)
root.mainloop()
