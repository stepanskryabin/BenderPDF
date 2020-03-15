# -*- coding:utf -8 -*-
__version__ = 'Версия: 0.0.1'

import tkinter
from tkinter import filedialog as fd
# from tkinter import ttk
from PIL import Image
#import os, sys
#import PyPDF2

#TODO переписать все функции разбив их на классы по следующей схеме:
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

#TODO добавить комментарии на English


root = tkinter.Tk()
root.geometry('800x600+200+100')
root.title('Конвертер BMP в PDF. ' + __version__)

text_frame = tkinter.LabelFrame(root, text='Перечень файлов')
text_frame.pack()

text = tkinter.Text(text_frame, padx=10, pady=5, wrap='word')
text.pack()

settings_frame_format = tkinter.LabelFrame(root, text='Формат конвертирования')
settings_frame_format.pack(side='left')

format_output_file = tkinter.StringVar()
format_output_file.set('.pdf')
check_button_true = tkinter.Radiobutton(settings_frame_format, text='Формат JPG', variable=format_output_file, value='.jpg')
check_button_false = tkinter.Radiobutton(settings_frame_format, text='Формат PDF', variable=format_output_file, value='.pdf')
check_button_true.pack()
check_button_false.pack()

settings_frame_split = tkinter.LabelFrame(root, text='Настройки разбивки файла')
settings_frame_split.pack(side='left')

split = tkinter.BooleanVar()
split.set(1)
split_true = tkinter.Radiobutton(settings_frame_split, text='Разбивать файл на части', variable=split, value=1, state='disable')
split_true.pack()
split_false = tkinter.Radiobutton(settings_frame_split, text='Не разбивать файл на части', variable=split, value=0, state='disable')
split_false.pack()


def ListFiles():
    global list_files;
    list_files = fd.askopenfilenames()
    text.delete(1.0, 99.0)
    text.insert(1.0, list_files)
    return list_files


def SaveFileName():
    global save_file_name;
    save_file_name = fd.asksaveasfilename(
        filetypes=[(f"Формат файла *{format_output_file.get()}", f"*{format_output_file.get()}")],
        defaultextension=format_output_file.get())
    return save_file_name

#TODO Переписать функцию, убрав лишние циклы
def ConvertFile(format='.pdf'):
    if format == '.pdf':
        i = 0
        for infile in list_files:
            i += 1
            outfile = save_file_name
            if i == 1:
                try:
                    with Image.open(infile) as im:
                        im.save(outfile, save_all=True)
                except IOError:
                    print("Невозможно конвертировать файл=", infile)
            else:
                try:
                    with Image.open(infile) as im:
                        im.save(outfile, append=True)
                except IOError:
                    print("Невозможно конвертировать файл=", infile)
        # if split.get() == True:
        #     pdf = PyPDF2.PdfFileReader(save_file_name)
        #     all_pages = pdf.getNumPages()
        #     page_range = 3
        #     new_outfile_path, new_outfile_format = os.path.splitext(save_file_name)
        #     page_part_1 = new_outfile_path + f"page-1-{page_range}" + new_outfile_format
        #     page_part_2 = new_outfile_path + f"page-{page_range + 1}-{all_pages}" + new_outfile_format
        #     for i in range(0, page_range):
        #         pdf_writer = PyPDF2.PdfFileWriter
        #         current_page = pdf.getPage(i)
        #         pdf_writer.addPage(current_page, i)
        #         with open(page_part_1, "wb") as out:
        #             pdf_writer.write(out)
        #     for i in range(page_range, all_pages):
        #         pdf_writer = PyPDF2.PdfFileWriter
        #         current_page = pdf.getPage(i)
        #         pdf_writer.addPage(current_page, i)
        #         with open(page_part_2, "wb") as out:
        #             pdf_writer.write(out)
        # else:
        #     pass
    elif format == '.jpg':
        for infile in list_files:
            outfile = save_file_name
            try:
                with Image.open(infile) as im:
                    im.save(outfile)
            except IOError:
                print("Невозможно конвертировать файл=", infile)
    else:
        print('Ошибка')


def CloseWindow():
    root.quit()


command_frame = tkinter.LabelFrame(root, text='Комманды')
command_frame.pack(side='right')

button_open = tkinter.Button(command_frame, text="(1) Добавить файлы", padx=8, pady=1, command=ListFiles)
button_open.pack(side='left')

button_save = tkinter.Button(command_frame, text="(2) Сохранить результат", padx=8, pady=1, command=SaveFileName)
button_save.pack(side='left')

button_run = tkinter.Button(command_frame, text="(3) Запустить", padx=8, pady=1, command=ConvertFile)
button_run.pack(side='left')

button_close = tkinter.Button(command_frame, text="(4) Выход", padx=8, pady=1, command=CloseWindow)
button_close.pack(side='left')

root.mainloop()
