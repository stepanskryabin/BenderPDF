#!/usr/bin/python
# -*- coding:utf -8 -*-
__version__ = '0.0.5'

from os import path
from os import remove
from threading import Thread

from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Text
from tkinter import Scale
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import Button
from tkinter import Scrollbar
from tkinter import Menu
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import END
from tkinter import INSERT
from tkinter import CURRENT

from PIL import Image

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

from numpy import arange


ABOUT = 'BenderPDF - конвертер файлов для сайта ГИС ЖКХ.\n' + 'Версия: ' + __version__ + \
    '\nРаспространяется по условиям лицензии GPLv3 https: // www.gnu.org/licenses/gpl-3.0.html'


class MainWindow:

    def __init__(self, master):
        self.FORMAT = {0: '.pdf', 1: '.jpg'}
        self.SETTINGS_DPI = {0: 72, 1: 100, 2: 150}
        self.list_files = ''
        self.filename = ''
        self.lenght_list_files = ''
        #
        self.text_box = Text(master, wrap='char', width=75, height=16)
        self.vscroll_text_box = Scrollbar(
            master, orient='vertical', command=self.text_box.yview())
        self.hscroll_text_box = Scrollbar(
            master, orient='horizontal', command=self.text_box.xview())
        self.text_box.config(yscrollcommand=self.vscroll_text_box.set,
                             xscrollcommand=self.hscroll_text_box.set)
        self.text_box.grid(row=2, column=2, rowspan=4, columnspan=6)
        self.vscroll_text_box.grid(
            row=2, column=7, rowspan=4, sticky=('se', 'ne'))
        self.hscroll_text_box.grid(
            row=6, column=2, columnspan=6, sticky=('we', 'ne'))
        #
        #
        # Настройки формата файла
        self.labelframe_format = LabelFrame(
            master, text="Формат файла")
        self.labelframe_format.grid(
            row=7, column=1, columnspan=1, rowspan=3, sticky='wens')
        self.format_output_file = IntVar()
        self.format_output_file.set(0)
        self.radiobutton_pdf = Radiobutton(self.labelframe_format, text='Формат PDF',
                                           variable=self.format_output_file, value=0, command=self.shutdown_button)
        self.radiobutton_jpg = Radiobutton(self.labelframe_format, text='Формат JPEG',
                                           variable=self.format_output_file, value=1, command=self.shutdown_button)
        self.radiobutton_pdf.pack(fill='x')
        self.radiobutton_jpg.pack(fill='x')
        #
        #
        # Задаём фрейм в котором будем размещать настройки разделения
        self.labelframe_split = LabelFrame(master, text="Развибка на страницы")
        self.labelframe_split.grid(
            row=7, column=2, columnspan=2, rowspan=3, sticky='wens')
        self.scale_split = Scale(self.labelframe_split, from_=0, to=100,
                                 resolution=5, orient="horizontal")
        self.scale_split.pack(fill='both')
        #
        #
        # Задаём фрейм в котором будем размещать настройки качества файла
        self.labelframe_dpi = LabelFrame(master, text="Настройки качества")
        self.labelframe_dpi.grid(
            row=7, column=4, columnspan=2, rowspan=3, sticky='wens')
        self.dpi = IntVar()
        self.dpi.set(2)
        self.radiobutton_dpi_72 = Radiobutton(self.labelframe_dpi, text='Среднее',
                                              variable=self.dpi, value=0)
        self.radiobutton_dpi_100 = Radiobutton(self.labelframe_dpi, text='Хорошее',
                                               variable=self.dpi, value=1)
        self.radiobutton_dpi_150 = Radiobutton(self.labelframe_dpi, text='Отличное',
                                               variable=self.dpi, value=2)
        self.radiobutton_dpi_72.pack(fill='both')
        self.radiobutton_dpi_100.pack(fill='both')
        self.radiobutton_dpi_150.pack(fill='both')
        #
        #
        # Фрейм с настройками качества сжатия JPEG
        self.labelframe_quality = LabelFrame(
            master, text="Настройка сжатия файла")
        self.labelframe_quality.grid(
            row=7, column=6, columnspan=2, rowspan=3, sticky='nw ne')
        self.scale_quality = Scale(self.labelframe_quality, label='Маленький                          Большой', from_=1, to=100,
                                   resolution=1, orient="horizontal", state='active')
        self.scale_quality.set(100)
        self.scale_quality.pack(fill='both')
        #
        #
        # Чекбокс настройки оптимизации качества
        self.optimize_image = BooleanVar()
        self.optimize_image.set(False)
        self.checkbutton_optimize = Checkbutton(
            self.labelframe_quality, text='Автоматически', variable=self.optimize_image, onvalue=True, offvalue=False)
        self.checkbutton_optimize.pack()
        self.checkbutton_optimize.bind(
            '<Button>', lambda event: self.change_state(event))
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
                                     )], dpi=self.SETTINGS_DPI[self.dpi.get()], optimize=self.optimize_image.get(),
                                     quality=self.scale_quality.get(), split_step=self.scale_split.get()),
                                 state='active', pady=5, padx=26)
        self.button_run.pack()
        #
        #
        # Progressbar
        self.pbar = ttk.Progressbar(
            master, orient='horizontal', mode='determinate', length=100, maximum=100)
        self.pbar.grid(row=10, column=1, columnspan=7, sticky='wens')
        #
        #
        # Меню программы
        self.menu = Menu(master)
        master.config(menu=self.menu)
        self.sub_menu1 = Menu(self.menu)
        self.menu.add_cascade(label='Файл', menu=self.sub_menu1)
        self.sub_menu1.add_command(label='Выход', command=self.closed_window)
        self.sub_menu2 = Menu(self.menu)
        self.menu.add_cascade(label='Информация', menu=self.sub_menu2)
        self.sub_menu2.add_command(
            label='О программе', command=self.show_about)

    def change_state(self, event):
        if self.optimize_image.get() == False:
            self.scale_quality.config(state='disable')
        else:
            self.scale_quality.config(state='active')

    def shutdown_button(self):
        if self.format_output_file.get() == 1:
            self.button_save.config(state='disable')
        else:
            self.button_save.config(state='active')

    def update_progressbar(self, page):
        step = 100 / self.lenght_list_files
        step_range = arange(0, 100, step)
        self.pbar['value'] = step_range[page] + step
        root.update()

    def show_about(self):
        messagebox.showinfo(
            title='О программе', message=ABOUT)

    def show_error(self, message):
        messagebox.showerror(title='ОШИБКА', message=message)

    def closed_window(self):
        root.quit()

    def listFiles(self):
        """ Функция привязана к кнопке "Добавить файлы". Результат работы функции - список файлов, который отображается в поле text_box """
        self.list_files = filedialog.askopenfilenames()
        self.lenght_list_files = len(self.list_files)
        self.text_box.delete(1.0, END)
        for i in self.list_files:
            self.text_box.insert(END, i)
            self.text_box.insert(END, '\n')
        return self.list_files

    def savefileName(self):
        """ Функция привязана к кнопке "Сохранить файл". Результат работы функции - полный путь к выходному файлу """
        default = self.FORMAT[0]
        setting_format = self.FORMAT[self.format_output_file.get()]
        self.filename = filedialog.asksaveasfilename(filetypes=[(f"Формат файла *{setting_format}",
                                                                 f"*{setting_format}")],
                                                     defaultextension=default)
        return self.filename


class ConvertFile:
    """

    Класс отвечает за конвертирование файлов изображений в форматы PDF, JPEG, PNG.
    Для файлов PDF есть возможность разделить на части с заданным количеством страниц.

    """

    def numberSteps(self, num_page, page_start, page_step):
        """

        Функция создаёт список значений диапазонов на которые разделяется файл

        """
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
                with open(file_part, 'wb') as pdf_output_stream:
                    pdf_output.write(pdf_output_stream)
            else:
                continue
            x += 1

    def to_image(self, in_file, optimize, quality, dpi, format_file='JPEG'):
        """

        Функция конвертирует в формат JPEG или PNG.
        \n in_file: полный путь к исходному файлу, тип str.
        \n optimize: функция оптимизации качества результирующего изображения, тип bool.
        \n dpi: количество точек на дюйм (функции передаются значения из ряда: 72, 100, 150), тип int.
        \n format_file: формат результирующего файла (функции передаются значения из ряда: JPG, PNG), тип str.
        \n return: функция преобразует в файл с заданным форматом и выдаёт полный путь к этому файлу.

        """
        input_path, input_format = path.splitext(in_file)
        out_file = input_path + '.' + format_file
        im = Image.open(in_file)
        size = im.size
        new_size = (size[0] // 2, size[1] // 2)
        img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
        img = img_resize.convert(mode='1')
        img.save(out_file, format_file, quality=quality, optimize=optimize,
                 dpi=(dpi, dpi), progressive=True)
        return out_file

    def process(self, input_file, output_file, format_file, dpi, optimize, quality, split_step=0):
        """

        Функция отвечает за запуск процесса конвертирования.
        \n input_file: список файлов, тип str.
        \n output_file: имя результирующего файла, тип str.
        \n format_file: формат результирующего файла (функции передаются значения из ряда: PDF, JPG, PNG), тип str.
        \n dpi: количество точек на дюйм (функции передаются значения из ряда: 72, 100, 150), тип int.
        \n split_step: шаг разбивки ПДФ-файла (указывается в страницах), тип int.
        \n return: в директории сохраняются файлы.

        """
        output_path, output_format = path.splitext(output_file)
        page = 0
        for i in input_file:
            """ Запускаем обновление прогрессбара в отдельном процессе """
            Thread(target=app.update_progressbar(page)).start()
            if format_file == '.pdf':
                """ сначала конвертируем в формат JPEG """
                output_jpg = self.to_image(i, optimize, quality, dpi, 'JPEG')
                """ JPEG добавляем в PDF-файл, выбираем параметры функции добавления основываясь на номере страницы """
                if page == True:
                    im = Image.open(output_jpg)
                    im.save(output_file, 'PDF', save_all=True)
                elif page > 0:
                    im = Image.open(output_jpg)
                    im.save(output_file, 'PDF', append=True)
                remove(output_jpg)
            elif format_file == '.jpg':
                self.to_image(i, optimize, quality, dpi, 'JPEG')
            else:
                pass
            page += 1
        if format_file == '.pdf' and split_step > 0:
            self.splitPdf(output_file, step=split_step)
        else:
            MainWindow.show_error('Конвертирование невозможно!')


# main window
if __name__ == "__main__":
    root = Tk()
    root.geometry('722x410+140-140')
    root.resizable(0, 0)
    # root.iconbitmap('./bender.ico')
    root.title('Конвертер изображений для ГИС ЖКХ')
    app = MainWindow(root)
    root.mainloop()
