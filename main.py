# -*- coding:utf -8 -*-
__version__ = 'Версия: 0.0.2'

import tkinter
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image
import os
import sys
import PyPDF2

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


root = tkinter.Tk()
root.geometry('900x600+100-100')
root.title('Конвертер изображений для ГИС ЖКХ. ' + __version__)

text_frame = tkinter.LabelFrame(root, text='Перечень файлов')
text_frame.pack()

text = tkinter.Text(text_frame, padx=5, pady=5, wrap='word')
text.pack()

settings_frame_format = tkinter.LabelFrame(root, text='Формат конвертирования')
settings_frame_format.pack(side='left')

format_output_file = tkinter.IntVar()
format_output_file.set(0)
check_button_true = tkinter.Radiobutton(
    settings_frame_format, text='Формат JPG', variable=format_output_file, value=1)
check_button_false = tkinter.Radiobutton(
    settings_frame_format, text='Формат PDF', variable=format_output_file, value=0)
check_button_true.pack()
check_button_false.pack()

settings_frame_split = tkinter.LabelFrame(
    root, text='Разбить на')
settings_frame_split.pack(side='left')

# Задаём диапазаон страниц по которому далее будем разделять файл
scale_split = tkinter.Scale(settings_frame_split, label='страниц',
                            from_=1, to=100, resolution=5, orient="horizontal")
scale_split.pack(side='left')


list_files = ''

# TODO добавить проверку на неверный формат файла


def ListFiles():
    global list_files
    list_files = fd.askopenfilenames()
    text.delete(1.0, 99.0)
    text.insert(1.0, list_files)
    return list_files


save_file_name = ''


def SaveFileName():
    FORMAT_FILE = {
        0: '.pdf',
        1: '.jpg'
    }
    global save_file_name
    save_file_name = fd.asksaveasfilename(filetypes=[(f"Формат файла *{FORMAT_FILE[format_output_file.get()]}", f"*{FORMAT_FILE[format_output_file.get()]}")],
                                          defaultextension=f'{FORMAT_FILE[0]}')
    return save_file_name


# TODO Переписать функцию, убрав лишние циклы


def ConvertFile(var, split):
    if var == 0:
        i = 0
        for infile in list_files:
            i += 1
            outfile = save_file_name
            file_path, file_format = os.path.splitext(save_file_name)
            temp_file = file_path + '-temp-'
            if i == 1:
                try:
                    with Image.open(infile) as im:
                        size = im.size
                        new_size = (size[0]//2, size[1]//2)
                        img_resize = im.resize(
                            size=new_size, resample=1, reducing_gap=3.0)
                        img = img_resize.convert(mode='1')
                        img.save(temp_file, 'JPEG',
                                 optimize=True, dpi=(150, 150))
                    with Image.open(temp_file) as im2:
                        im2.save(outfile, save_all=True)
                        os.remove(temp_file)
                except IOError:
                    print("1Невозможно конвертировать файл=", infile)
            else:
                try:
                    with Image.open(infile) as im:
                        size = im.size
                        new_size = (size[0]//2, size[1]//2)
                        img_resize = im.resize(
                            size=new_size, resample=1, reducing_gap=3.0)
                        img = img_resize.convert(mode='1')
                        img.save(temp_file, 'JPEG',
                                 optimize=True, dpi=(150, 150))
                    with Image.open(temp_file) as im2:
                        im2.save(outfile, append=True)
                        os.remove(temp_file)
                except IOError:
                    print("2Невозможно конвертировать файл=", infile)
    elif var == 1:
        for infile in list_files:
            file_path, file_format = os.path.splitext(infile)
            outfile = file_path + '.jpg'
            try:
                with Image.open(infile) as im:
                    size = im.size
                    new_size = (size[0]//2, size[1]//2)
                    img_resize = im.resize(
                        size=new_size, resample=1, reducing_gap=3.0)
                    img = img_resize.convert(mode='1')
                    img.save(outfile, 'JPEG', optimize=True, dpi=(150, 150))
            except IOError:
                print("3Невозможно конвертировать файл=", infile)
    else:
        print('Конвертирование остановлено')
    if split >= 5:
        split_pdf(filename=outfile, step=split)
    else:
        pass

# Функция добавляет номер последней страницы в диапазон


def number_of_steps(num_page, page_start, page_step):
    steps = list(range(page_start, num_page, page_step))
    steps.append(num_page)
    return steps

# Функция разделяет ПДФ на файлы согласно заданного диапазона


def split_pdf(filename, start=0, step=50):
    """
    Функция разделяет ПДФ на файлы согласно заданного диапазона
    :param filename: имя файла, обязательный параметр, тип str
    :param start: начало отсчёта диапазона, по умолчанию 0, тип int.
    :param step: шаг диапазона, по умолчанию 50 страниц, тип int.
    :return: возвращает несколько файлов по количеству диапазонов (имя генерируется по умолчанию).
    """
    pdf_input = PyPDF2.PdfFileReader(open(filename, 'rb'))
    steps = number_of_steps(num_page=pdf_input.getNumPages(),
                            page_start=start, page_step=step)
    new_outfile_path, new_outfile_format = os.path.splitext(filename)
    x = 1
    for i in steps:
        if x < len(steps):
            pdf_output = PyPDF2.PdfFileWriter()
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


# Функция конвертирования в ПДФ
"""     def convert_to_pdf(input_file, output_file):
        i = 0
        if i == 0:
            with Image.open(input_file) as im:
                im.save(output_file, 'PDF', save_all=True)
        else:
            with Image.open(input_file) as im:
                im.save(output_file, append=True)
        i += 1
        return output_file """

# Функция конвертирования в JPG
"""     def convert_to_jpg(input_file, output_file):
        im = Image.open(input_file)
        size = im.size
        new_size = (size[0]//2, size[1]//2)
        img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
        img = img_resize.convert(mode='1')
        img.save(output_file, 'JPEG', optimize=True, dpi=(150, 150))
        return output_file """


def CloseWindow():
    root.quit()


command_frame = tkinter.LabelFrame(root, text='Комманды')
command_frame.pack(side='left')

button_open = tkinter.Button(
    command_frame, text="(1) Добавить файлы", padx=8, pady=1, command=ListFiles, state='active')
button_open.pack(side='left')


button_save = tkinter.Button(command_frame, text="(2) Сохранить результат", padx=8, pady=1, command=SaveFileName,
                             state='active')
button_save.pack(side='left')


button_run = tkinter.Button(command_frame, text="(3) Запустить", padx=8,
                            pady=1, state='active', command=lambda x=2: ConvertFile(var=format_output_file.get(), split=scale_split.get()))
button_run.pack(side='left')


button_close = tkinter.Button(
    command_frame, text="(4) Выход", padx=8, pady=1, command=CloseWindow, state='active')
button_close.pack(side='left')

root.mainloop()
