import tkinter
from tkinter import filedialog as fd
# from tkinter import ttk
from PIL import Image
import os, sys

# Class
# class Convert:
#     pass
#
# class Files:
#     pass
#
# class MainWindow:
#     pass
# End Class


root = tkinter.Tk()
root.geometry('800x600+200+100')
root.title('Конвертер BMP в PDF')

text_frame = tkinter.LabelFrame(root, text='Перечень файлов')
text_frame.pack()

text = tkinter.Text(text_frame, padx=10, pady=5, wrap='word')
text.pack()

settings_frame = tkinter.LabelFrame(root, text='Настройки конвертирования')
settings_frame.pack()

format_output_file = tkinter.StringVar()
format_output_file.set('.pdf')
check_button = tkinter.Checkbutton(settings_frame, text='Формат JPG', variable=format_output_file, onvalue='.jpg',
                                   offvalue='.pdf')
check_button.pack()
print(format_output_file.get())

split = tkinter.BooleanVar()
split.set(1)
split_true = tkinter.Radiobutton(settings_frame, text='Разбивать файл на части', variable=split, value=1)
split_false = tkinter.Radiobutton(settings_frame, text='Не разбивать файл на части', variable=split, value=0)
split_true.pack()
split_false.pack()
print(split.get())


def ListFiles():
    global list_files;
    list_files = fd.askopenfilenames()
    text.delete(1.0, 99.0)
    text.insert(1.0, list_files)


def SaveFileName():
    global save_file_name;
    save_file_name = fd.asksaveasfilename(
        filetypes=[(f"Формат файла *{format_output_file.get()}", f"*{format_output_file.get()}")],
        defaultextension=format_output_file.get())
    return save_file_name


def ConvertFile():
    if format_output_file.get() == '.pdf':
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
    elif format_output_file.get() == '.jpg':
        for infile in list_files:
            file_path, file_format = os.path.splitext(infile)
            outfile = file_path + format_output_file.get()
            if infile != outfile:
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
command_frame.pack()

button_open = tkinter.Button(command_frame, text="Добавить файлы", padx=8, pady=1, command=ListFiles)
button_open.pack(side='left')

button_save = tkinter.Button(command_frame, text="Сохранить как..", padx=8, pady=1, command=SaveFileName)
button_save.pack(side='left')

button_run = tkinter.Button(command_frame, text="Запустить", padx=8, pady=1, command=ConvertFile)
button_run.pack(side='left')

button_close = tkinter.Button(command_frame, text="Выход", padx=8, pady=1, command=CloseWindow)
button_close.pack(side='left')

root.mainloop()
