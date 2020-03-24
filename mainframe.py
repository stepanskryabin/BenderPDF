#!/usr/bin/python
# -*- coding:utf -8 -*-

from tkinter import Tk, filedialog, ttk, Label, Text, Scale, Frame, Radiobutton, IntVar, Button, Scrollbar, Menu, messagebox, scrolledtext
# Импортируем имена индексов для текстового виджета
from tkinter import END, INSERT, CURRENT
from imageprocessing import ConvertFile


# TODO переписать все функции разбив их на классы по следующей схеме:
# Класс отвечающий за конвертацию файлов
# class Convert:
#    функция конвертирования в JPG
#    функция конвертирования в PDF
#    функция разбивки PDF
# Класс отвечающий за имена входящих и исходящих файлов
# class Files:
#    функция выдающая список входящих файлов
#    функция выдающая список исходящих файлов
# Класс отвечающий за отрисовку интерфейса
# class MainWindow:
#    функция отрисовки фрейма
#    функция отрисовки кнопки
#    функция отрисовки радиокнопки
#    функция отрисовки чекбокса

# TODO добавить комментарии на English

class MainFrame:

    def __init__(self, master):
        self.FORMAT = {0: '.pdf', 1: '.jpg', 2: '.png'}
        #
        self.command_label = Label(
            master, text='Команды:', textvariable='Команды:')
        self.command_label.grid(row=1, column=1)
        #
        self.text_label = Label(
            master, text='Перечень файлов:', textvariable='Перечень файлов:')
        self.text_label.grid(row=1, column=2, columnspan=6)
        #
        self.text = Text(master, wrap='char', width=60, height=10)
        self.scroll = Scrollbar(
            master, orient='vertical', command=self.text.yview())
        self.text.config(yscrollcommand=self.scroll.set)
        self.text.grid(row=2, column=2, rowspan=4, columnspan=6)
        self.scroll.grid(row=2, column=7, rowspan=4, sticky=('se', 'ne'))
        #
        self.format_output_file = IntVar()
        self.format_output_file.set(0)
        self.radiobutton_pdf = Radiobutton(master, text='Формат PDF',
                                           variable=self.format_output_file, value=0)
        self.radiobutton_jpg = Radiobutton(master, text='Формат JPG',
                                           variable=self.format_output_file, value=1)
        self.radiobutton_png = Radiobutton(master, text='Формат PNG',
                                           variable=self.format_output_file, value=2)
        self.radiobutton_pdf.grid(row=6, column=1, columnspan=3, sticky='w')
        self.radiobutton_jpg.grid(row=7, column=1, columnspan=3, sticky='w')
        self.radiobutton_png.grid(row=8, column=1, columnspan=3, sticky='w')
        # Задаём диапазон страниц по которому далее будем разделять файл
        self.scale_split = Scale(master, label='Количество страниц', from_=1, to=100,
                                 resolution=5, orient="horizontal")
        self.scale_split.grid(
            row=6, column=4, rowspan=2, columnspan=2, sticky='w')
        # Задаём диапазон качества результирующего файла
        self.scale_quality = Scale(master, label='Качество', from_=1, to=100,
                                   resolution=1, orient="horizontal")
        self.scale_quality.grid(
            row=6, column=6, rowspan=2, columnspan=2, sticky='w')
        #
        self.button_frame = Frame(master)
        self.button_frame.grid(row=2, column=1, rowspan=4)
        self.button_open = Button(self.button_frame, text="(1) Добавить",
                                  command=self.listFiles, state='active', pady=5, padx=8)
        self.button_open.pack()
        #
        self.button_save = Button(self.button_frame, text="(2) Сохранить",
                                  command=self.savefileName, state='active', pady=5, padx=5)
        self.button_save.pack()
        #
        self.button_run = Button(self.button_frame, text="(3) Запустить", command=lambda x=2: ConvertFile.process(input_file=self.listFiles(
        ), output_file=self.savefileName(), format=self.FORMAT[self.format_output_file.get()], split_step=self.scale_split.get()), state='active', pady=5, padx=7)
        self.button_run.pack()
        #
        self.button_close = Button(self.button_frame, text="(4) Выход",
                                   command=self.closeWindow, state='active', pady=5, padx=10)
        self.button_close.pack()
        #
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.sub_menu1 = Menu(self.menu)
        self.menu.add_cascade(label='Файл', menu=self.sub_menu1)
        self.sub_menu1.add_command(label='Выход', command=self.closeWindow)
        self.sub_menu2 = Menu(self.menu)
        self.menu.add_cascade(label='Информация', menu=self.sub_menu2)
        self.sub_menu2.add_command(label='О программе', command=self.aboutInfo)
        self.sub_menu2.add_command(label='Автор', command=self.aboutInfo)
        self.sub_menu2.add_command(label='Лицензия', command=self.aboutInfo)
        #
        self.filename = ''
        self.list_files = ''
        #

    def aboutInfo(self):
        messagebox.showinfo(
            title='О программе', message='BenderPDF - конвертер файлов для сайта ГИС ЖКХ')

    def closeWindow(self):
        root.quit()

    def listFiles(self):
        self.list_files = filedialog.askopenfilenames()
        self.text.delete(1.0, END)
        for i in self.list_files:
            self.text.insert(END, i)
            self.text.insert(END, '\n')
        return self.list_files

    def savefileName(self):
        default = self.FORMAT[0]
        format = self.FORMAT[self.format_output_file.get()]
        self.filename = filedialog.asksaveasfilename(filetypes=[(f"Формат файла *{format}", f"*{format}")],
                                                     defaultextension=f'{default}')
        return self.filename
