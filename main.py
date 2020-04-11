#!/usr/bin/python
# -*- coding:utf -8 -*-
__version__ = 'Версия: 0.0.3'


from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import Label
from tkinter import Text
from tkinter import Scale
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Button
from tkinter import Scrollbar
from tkinter import Menu
from tkinter import messagebox
from tkinter import scrolledtext
# Импортируем имена индексов для текстового виджета
from tkinter import END
from tkinter import INSERT
from tkinter import CURRENT
from PIL import Image
from os import path
from os import remove
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.FORMAT = {0: '.pdf', 1: '.jpg', 2: '.png'}
        self.SETTINGS_DPI = {0: 72, 1: 100, 2: 150}
        self.list_files = ''
        self.filename = ''
        #
        self.command_label = Label(
            master, text='Команды:', textvariable='Команды:')
        self.command_label.grid(row=1, column=1)
        #
        self.text_label = Label(
            master, text='Перечень файлов:', textvariable='Перечень файлов:')
        self.text_label.grid(row=1, column=2, columnspan=6)
        #
        self.text_box = Text(master, wrap='char', width=75, height=10)
        self.scroll_text_box = Scrollbar(
            master, orient='vertical', command=self.text_box.yview())
        self.text_box.config(yscrollcommand=self.scroll_text_box.set)
        self.text_box.grid(row=2, column=2, rowspan=4, columnspan=6)
        self.scroll_text_box.grid(
            row=2, column=7, rowspan=4, sticky=('se', 'ne'))
        #
        #
        # Настройки формата файла
        self.format_output_file = IntVar()
        self.format_output_file.set(0)
        self.radiobutton_pdf = Radiobutton(master, text='Формат PDF',
                                           variable=self.format_output_file, value=0)
        self.radiobutton_jpg = Radiobutton(master, text='Формат JPG',
                                           variable=self.format_output_file, value=1)
        self.radiobutton_png = Radiobutton(master, text='Формат PNG',
                                           variable=self.format_output_file, value=2)
        self.radiobutton_pdf.grid(row=6, column=1, columnspan=2, sticky='w')
        self.radiobutton_jpg.grid(row=7, column=1, columnspan=2, sticky='w')
        self.radiobutton_png.grid(row=8, column=1, columnspan=2, sticky='w')
        #
        #
        # Настройки dpi
        self.dpi = IntVar()
        self.dpi.set(2)
        self.radiobutton_dpi_72 = Radiobutton(master, text='DPI 72',
                                              variable=self.dpi, value=0)
        self.radiobutton_dpi_100 = Radiobutton(master, text='DPI 100',
                                               variable=self.dpi, value=1)
        self.radiobutton_dpi_150 = Radiobutton(master, text='DPI 150',
                                               variable=self.dpi, value=2)
        self.radiobutton_dpi_72.grid(row=6, column=3, columnspan=2, sticky='w')
        self.radiobutton_dpi_100.grid(
            row=7, column=3, columnspan=2, sticky='w')
        self.radiobutton_dpi_150.grid(
            row=8, column=3, columnspan=2, sticky='w')
        #
        #
        # Настройки разделения файла ПДФ (задается диапазон страниц)
        self.scale_split = Scale(master, label='Количество страниц', from_=0, to=100,
                                 resolution=5, orient="horizontal")
        self.scale_split.grid(
            row=6, column=5, rowspan=2, sticky='we')
        #
        #
        # Настройка качества сжатия JPEG
        self.scale_quality = Scale(master, label='Качество', from_=1, to=100,
                                   resolution=1, orient="horizontal")
        self.scale_quality.set(90)
        self.scale_quality.grid(
            row=6, column=7, rowspan=2, sticky='we')
        #
        #
        # Задаем фрейм в котором будем размещать основные кнопки команд
        self.button_frame = Frame(master)
        self.button_frame.grid(row=2, column=1, rowspan=4)
        self.button_open = Button(self.button_frame, text="Добавить файлы",
                                  command=self.listFiles, state='active', pady=5, padx=8)
        self.button_open.pack()
        self.button_save = Button(self.button_frame, text="Сохранить файл",
                                  command=self.savefileName, state='active', pady=5, padx=9)
        self.button_save.pack()
        self.button_run = Button(self.button_frame, text="Запустить",
                                 command=lambda x=True: ConvertFile().process(
                                     input_file=self.list_files, output_file=self.filename,
                                     format_file=self.FORMAT[self.format_output_file.get(
                                     )],
                                     dpi=self.SETTINGS_DPI[self.dpi.get()], split_step=self.scale_split.get()),
                                 state='active', pady=5, padx=26)
        self.button_run.pack()
        self.button_close = Button(self.button_frame, text="Выход",
                                   command=self.closeWindow, state='active', pady=5, padx=36)
        self.button_close.pack()
        #
        #
        # Progressbar
        #
        # Меню программы
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

    def progressbar(self, lenght, value):
        pbar = ttk.Progressbar(
            self.master, orient='horizontal', mode='determinate', length=lenght)
        self.pbar.grid(row=9, column=1, columnspan=9, sticky='we')

    def aboutInfo(self):
        messagebox.showinfo(
            title='О программе', message='BenderPDF - конвертер файлов для сайта ГИС ЖКХ')

    def closeWindow(self):
        root.quit()

    # Функция привязана к кнопке "Добавить файлы". Результат работы функции - список файлов, который отображается в поле text_box
    def listFiles(self):
        self.list_files = filedialog.askopenfilenames()
        self.text_box.delete(1.0, END)
        for i in self.list_files:
            self.text_box.insert(END, i)
            self.text_box.insert(END, '\n')
        return self.list_files

    # Функция привязана к кнопке "Сохранить файл". Результат работы функции - полный путь к выходному файлу
    def savefileName(self):
        default = self.FORMAT[0]
        setting_format = self.FORMAT[self.format_output_file.get()]
        self.filename = filedialog.asksaveasfilename(filetypes=[(f"Формат файла *{setting_format}", f"*{setting_format}")],
                                                     defaultextension=f'{default}')
        return self.filename


class ConvertFile:
    """
    Класс отвечает за конвертирование файлов изображений в форматы PDF, JPEG, PNG.
    Для файлов PDF есть возможность разделить на части с заданным количеством страниц.
    """

    def __init__(self):
        pass

    def numberSteps(self, num_page, page_start, page_step):
        steps = list(range(page_start, num_page, page_step))
        steps.append(num_page)
        return steps

    def splitPdf(self, input_file, step):
        """
        Функция разделяет ПДФ на файлы согласно заданного диапазона.
        Дипазон задается в страницах. Функция возвращает несколько файлов, по количеству диапазонов (имя генерируется по умолчанию).
        \n input_file: имя файла, обязательный параметр, тип str.
        \n step: шаг диапазона в страницах, тип int.
        """
        pdf_input = PdfFileReader(open(input_file, 'rb'))
        steps = self.numberSteps(num_page=pdf_input.getNumPages(),
                                 page_start=0, page_step=step)
        new_outfile_path, new_outfile_format = path.splitext(input_file)
        x = 1
        for i in steps:
            if x < len(steps):
                pdf_output = PdfFileWriter()
                for z in list(range(i, steps[x])):
                    pdf_output.addPage(pdf_input.getPage(z))
                file_part = new_outfile_path + \
                    f"-page-{i}-{steps[x]}" + new_outfile_format
                pdf_output_stream = open(file_part, 'wb')
                pdf_output.write(pdf_output_stream)
                pdf_output_stream.close()
            else:
                continue
            x += 1

    def to_image(self, in_file, out_file, dpi):
        im = Image.open(in_file)
        size = im.size
        new_size = (size[0] // 2, size[1] // 2)
        img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
        img = img_resize.convert(mode='1')
        img.save(out_file, optimize=True, dpi=(dpi, dpi))

    def process(self, input_file, output_file, format_file, dpi, split_step=0):
        """
        Функция отвечает за запуск процесса конвертирования.
        \n input_file: список файлов, тип str
        \n output_file: имя результирующего файла, тип str
        \n format_file: формат результирующего файла, тип str
        \n dpi: настройка dpi
        \n split_step: начальная страница
        \n return: в директории сохраняются файлы
        """
        output_path, output_format = path.splitext(output_file)
        page = 0
        #pb = MainWindow().progressbar(len(input_file))
        for i in input_file:
            if format_file == '.pdf':
                input_path, input_format = path.splitext(i)
                output_jpg = input_path + '.jpg'
                self.to_image(i, output_jpg, dpi)
                if page == 0:
                    im = Image.open(output_jpg)
                    im.save(output_file, 'PDF', save_all=True)
                elif page > 0:
                    im = Image.open(output_jpg)
                    im.save(output_file, 'PDF', append=True)
                del(input_format)
                remove(output_jpg)
            elif format_file == '.jpg' or format_file == '.png':
                input_path, input_format = path.splitext(i)
                output_image = input_path + format_file
                self.to_image(i, output_image, dpi)
                del(input_format)
            else:
                pass
            page += 1
        if split_step > 0:
            self.splitPdf(output_file, step=split_step)
        else:
            pass
        del(output_format)


# main window
root = Tk()
root.geometry('725x420+140-140')
# root.iconbitmap('bender.ico')
root.title('Конвертер изображений для ГИС ЖКХ. ' + __version__)
app = MainWindow(root)
root.mainloop()
