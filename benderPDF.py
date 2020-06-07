#!/usr/bin/python
# -*- coding:utf -8 -*-

from os import path
from os import remove
from threading import Thread

from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import LabelFrame
from tkinter import Text
from tkinter import Scale
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import BooleanVar
from tkinter import Button
from tkinter import Scrollbar
from tkinter import Menu
from tkinter import messagebox
from tkinter import END


from PIL import Image

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

__version__ = '0.0.6'
ABOUT = 'BenderPDF - конвертер файлов для сайта ГИС ЖКХ.\n' + 'Версия: ' + __version__ + \
    '\nРаспространяется по условиям лицензии GPLv3 https: // www.gnu.org/licenses/gpl-3.0.html'


def MainWindow(master):
    FORMAT = {0: '.pdf', 1: '.jpg'}
    SETTINGS_DPI = {0: 72, 1: 100, 2: 150}
    SETTINGS_COLOR = {0: '1', 1: 'RGB'}
    list_files = ''
    filename = ''
    lenght_list_files = ''
    ####################################################################################################
    # A1 # 1      # 2       # 3       # 4       # 5       # 6       # 7       # 8       # 9       # 10 #
    # A2 # BUTTON # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # VSCROLL # 10 #
    # A3 # BUTTON # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # VSCROLL # 10 #
    # A4 # BUTTON # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # VSCROLL # 10 #
    # A5 # BUTTON # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # TEXT    # VSCROLL # 10 #
    # A6 # 1      # HSCROLL # HSCROLL # HSCROLL # HSCROLL # HSCROLL # HSCROLL # HSCROLL # HSCROLL # 10 #
    # A7 # FORMAT # SPLIT   # SPLIT   # DPI     # DPI     # COLOR   # COLOR   # QUALITY # QUALITY # 10 #
    # A8 # FORMAT # SPLIT   # SPLIT   # DPI     # DPI     # COLOR   # COLOR   # QUALITY # QUALITY # 10 #
    # A9 # FORMAT # SPLIT   # SPLIT   # DPI     # DPI     # COLOR   # COLOR   # QUALITY # QUALITY # 10 #
    # A10# P_BAR  # P_BAR   # P_BAR   # P_BAR   # P_BAR   # P_BAR   # P_BAR   # P_BAR   # P_BAR   # 10 #
    ####################################################################################################
    text_box = Text(master, wrap='char', width=80, height=16)
    vscroll_text_box = Scrollbar(master, orient='vertical',
                                 command=text_box.yview())
    hscroll_text_box = Scrollbar(master, orient='horizontal',
                                 command=text_box.xview())
    text_box.config(yscrollcommand=vscroll_text_box.set,
                    xscrollcommand=hscroll_text_box.set)
    text_box.grid(row=2, column=2, rowspan=4, columnspan=7)
    vscroll_text_box.grid(row=2, column=9, rowspan=4,
                          sticky=('se', 'ne'))
    hscroll_text_box.grid(row=6, column=2, columnspan=8,
                          sticky=('we', 'ne'))
    #
    #
    # Настройки формата файла
    labelframe_format = LabelFrame(master, text="Формат файла")
    labelframe_format.grid(
        row=7, column=1, columnspan=1, rowspan=3, sticky='wens')
    format_output_file = IntVar()
    format_output_file.set(0)
    radiobutton_pdf = Radiobutton(labelframe_format, text='Формат PDF',
                                  variable=format_output_file, value=0, command=shutdown_button)
    radiobutton_jpg = Radiobutton(labelframe_format, text='Формат JPEG',
                                  variable=format_output_file, value=1, command=shutdown_button)
    radiobutton_pdf.pack(fill='x')
    radiobutton_jpg.pack(fill='x')
    #
    #
    # Задаём фрейм в котором будем размещать настройки разделения
    labelframe_split = LabelFrame(master, text="Развибка на страницы")
    labelframe_split.grid(
        row=7, column=2, columnspan=2, rowspan=3, sticky='wens')
    scale_split = Scale(labelframe_split, from_=0, to=100,
                        resolution=5, orient="horizontal")
    scale_split.pack(fill='both')
    #
    #
    # Задаём фрейм в котором будем размещать настройки качества файла
    labelframe_dpi = LabelFrame(master, text="Настройки качества")
    labelframe_dpi.grid(
        row=7, column=4, columnspan=2, rowspan=3, sticky='wens')
    dpi = IntVar()
    dpi.set(2)
    radiobutton_dpi_72 = Radiobutton(labelframe_dpi, text='Среднее',
                                     variable=dpi, value=0)
    radiobutton_dpi_100 = Radiobutton(labelframe_dpi, text='Хорошее',
                                      variable=dpi, value=1)
    radiobutton_dpi_150 = Radiobutton(labelframe_dpi, text='Отличное',
                                      variable=dpi, value=2)
    radiobutton_dpi_72.pack(fill='both')
    radiobutton_dpi_100.pack(fill='both')
    radiobutton_dpi_150.pack(fill='both')
    #
    #
    # Фрейм с настройками выбора цветное или ч/б
    labelframe_color = LabelFrame(master, text="Настройки цвета")
    labelframe_color.grid(
        row=7, column=6, columnspan=2, rowspan=3, sticky='wens')
    color = IntVar()
    color.set(0)
    radiobutton_bw = Radiobutton(labelframe_color, text='Чёрно/белое',
                                 variable=color, value=0)
    radiobutton_color = Radiobutton(labelframe_color, txt='Цветное',
                                    variable=color, value=1)
    radiobutton_bw.pack(fill='both')
    radiobutton_color.pack(fill='both')
    #
    #
    # Фрейм с настройками качества сжатия JPEG
    labelframe_quality = LabelFrame(
        master, text="Настройка сжатия файла")
    labelframe_quality.grid(
        row=7, column=8, columnspan=2, rowspan=3, sticky='nw ne')
    scale_quality = Scale(labelframe_quality, label='Хуже                   Лучше', from_=1, to=100,
                          resolution=1, orient="horizontal", state='active')
    scale_quality.set(100)
    scale_quality.pack(fill='both')
    #
    #
    # Чекбокс настройки оптимизации качества
    optimize_image = BooleanVar()
    optimize_image.set(False)
    checkbutton_optimize = Checkbutton(
        labelframe_quality, text='Автоматически', variable=optimize_image, onvalue=True, offvalue=False)
    checkbutton_optimize.pack()
    checkbutton_optimize.bind('<Button>', lambda event: change_state(event))
    #
    #
    # Задаем фрейм в котором будем размещать основные кнопки команд
    button_frame = Frame(master)
    button_frame.grid(row=2, column=1, rowspan=4)
    button_open = Button(button_frame, text="Добавить файлы",
                         command=listFiles, state='active', pady=5, padx=8)
    button_open.pack()
    button_save = Button(button_frame, text="Сохранить файл",
                         command=savefileName, state='active', pady=5, padx=9)
    button_save.pack()
    button_run = Button(button_frame, text="Запустить",
                        command=lambda x=True: process(
                            input_file=list_files, output_file=filename,
                            format_file=FORMAT[format_output_file.get(
                            )], dpi=SETTINGS_DPI[dpi.get()], color=SETTINGS_COLOR[color.get()],
                            optimize=optimize_image.get(),
                            quality=scale_quality.get(), split_step=scale_split.get()),
                        state='active', pady=5, padx=26)
    button_run.pack()
    #
    #
    # Progressbar
    pbar = ttk.Progressbar(
        master, orient='horizontal', mode='determinate', length=100, maximum=100)
    pbar.grid(row=10, column=1, columnspan=9, sticky='wens')
    #
    #
    # Меню программы
    menu = Menu(master)
    master.config(menu=menu)
    sub_menu1 = Menu(menu)
    menu.add_cascade(label='Файл', menu=sub_menu1)
    sub_menu1.add_command(label='Выход', command=closed_window)
    sub_menu2 = Menu(menu)
    menu.add_cascade(label='Информация', menu=sub_menu2)
    sub_menu2.add_command(
        label='О программе', command=show_about)
    return


def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


def change_state(event):
    if optimize_image.get() is False:
        scale_quality.config(state='disable')
    else:
        scale_quality.config(state='active')


def shutdown_button():
    if format_output_file.get() == 1:
        button_save.config(state='disable')
    else:
        button_save.config(state='active')


def update_progressbar(page):
    step = 100 / lenght_list_files
    step_range = list(frange(0, 100, step))
    pbar['value'] = step_range[page] + step
    root.update()


def show_about():
    messagebox.showinfo(
        title='О программе', message=ABOUT)


def show_error(message):
    messagebox.showerror(title='ОШИБКА', message=message)


def closed_window():
    root.quit()


def listFiles():
    """
    Функция привязана к кнопке "Добавить файлы".
    Результат работы функции - список файлов, который отображается в поле text_box
    """
    list_files = filedialog.askopenfilenames()
    lenght_list_files = len(list_files)
    text_box.delete(1.0, END)
    for i in list_files:
        text_box.insert(END, i)
        text_box.insert(END, '\n')
    return list_files


def savefileName():
    """
    Функция привязана к кнопке "Сохранить файл".
    Результат работы функции - полный путь к выходному файлу
    """
    default = FORMAT[0]
    setting_format = FORMAT[format_output_file.get()]
    filename = filedialog.asksaveasfilename(filetypes=[(f"Формат файла *{setting_format}",
                                                        f"*{setting_format}")],
                                            defaultextension=default)
    return filename


def splitPdf(input_file, step):
    """

    Функция разделяет ПДФ на файлы согласно заданного диапазона.
    Дипазон задается в страницах. Функция возвращает несколько файлов,
    по количеству диапазонов (имя генерируется по умолчанию).
    \n input_file: имя файла, обязательный параметр, тип str.
    \n step: шаг диапазона в страницах, тип int.

    """
    try:
        pdf_input = PdfFileReader(open(input_file, 'rb'))
    except Exception:
        pass

    """
        создаем список номеров страниц начала и конца диапазона
        на который будем разбивать файл, добавляем в конец списка
        номер последней страницы
    """
    steps = list(range(0, pdf_input.getNumPages(), step))
    steps.append(pdf_input.getNumPages())
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


def to_image(in_file, optimize, quality, dpi, color, format_file='JPEG'):
    """
    Функция конвертирует в формат JPEG или PNG.
    \n in_file: полный путь к исходному файлу, тип str.
    \n optimize: функция оптимизации качества результирующего изображения, тип bool.
    \n dpi: количество точек на дюйм (функции передаются значения из ряда: 72, 100, 150), тип int.
    \n format_file: формат результирующего файла (функции передаются значения из ряда: JPG, PNG), тип str.
    \n return: функция преобразует в файл с заданным форматом и выдаёт полный путь к этому файлу.
    """
    input_path, _ = path.splitext(in_file)
    out_file = ".".join([input_path, format_file])
    im = Image.open(in_file)
    size = im.size
    new_size = (size[0] // 2, size[1] // 2)
    img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
    img = img_resize.convert(mode=color)
    img.save(out_file, format_file, quality=quality, optimize=optimize,
             dpi=(dpi, dpi), progressive=True)
    return out_file


def process(input_file, output_file, format_file, dpi, color, optimize, quality, split_step=0):
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
        """
        Запускаем обновление прогрессбара в отдельном процессе
        """
        Thread(target=app.update_progressbar(page)).start()
        if format_file == '.pdf':
            """
            сначала конвертируем в формат JPEG
            """
            output_jpg = to_image(i, optimize, quality, dpi, color, 'JPEG')
            """
            JPEG добавляем в PDF-файл, выбираем параметры функции добавления основываясь на номере страницы
            """
            if page == 0:
                im = Image.open(output_jpg)
                im.save(output_file, 'PDF', save_all=True)
            elif page > 0:
                im = Image.open(output_jpg)
                im.save(output_file, 'PDF', append=True)
            remove(output_jpg)
        elif format_file == '.jpg':
            to_image(i, optimize, quality, dpi, color, 'JPEG')
        else:
            pass
        page += 1
    if format_file == '.pdf' and split_step > 0:
        splitPdf(output_file, step=split_step)
    else:
        pass
    return


# main window
if __name__ == "__main__":
    root = Tk()
    root.geometry('780x410+140-140')
    root.resizable(0, 0)
    # root.iconbitmap('./bender.ico')
    root.title('Конвертер изображений для ГИС ЖКХ')
    app = MainWindow(root)
    root.mainloop()
