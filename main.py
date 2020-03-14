import tkinter
from tkinter import filedialog as fd
from tkinter import ttk

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
root.title('Конвертер BMP в PDF')

text_frame = tkinter.LabelFrame(root, text='Перечень файлов')
text_frame.pack()

text = tkinter.Text(text_frame, padx=60, pady=20, wrap='word')
text.pack()

settings_frame = tkinter.LabelFrame(root, text='Настройки конвертирования')
settings_frame.pack()

format_output_file = tkinter.StringVar()
format_output_file.set('.pdf')
check_button = tkinter.Checkbutton(settings_frame, text='Формат JPG', variable=format_output_file, onvalue='.jpg', offvalue='.pdf')
check_button.pack()
print(format_output_file.get())

radiobutton_slice = tkinter.BooleanVar()
radiobutton_slice.set(0)
radiobutton_slice_true = tkinter.Radiobutton(settings_frame, text='Разбивать файл на части', variable=radiobutton_slice, value=0)
radiobutton_slice_false = tkinter.Radiobutton(settings_frame, text='Не разбивать файл на части', variable=radiobutton_slice, value=1)
radiobutton_slice_true.pack()
radiobutton_slice_false.pack()
print(radiobutton_slice.get())


def ListFiles():
    open = fd.askopenfilenames()
    print(open)
    text.delete(1.0, 99.0)
    text.insert(1.0, open)


def SaveFileName():
    open = fd.asksaveasfilename(filetypes=[("Файл формата ПДФ", "*.pdf")], defaultextension=format_output_file.get())
    print(open)
    return open


def CloseWindow():
    root.quit()

command_frame = tkinter.LabelFrame(root, text='Комманды')
command_frame.pack()

button_open = tkinter.Button(command_frame, text="Open file..", padx=8, pady=1, command=ListFiles)
button_open.pack(side='left')


button_save = tkinter.Button(command_frame, text="Save file..", padx=8, pady=1, command=SaveFileName)
button_save.pack(side='left')


button_close = tkinter.Button(command_frame, text="Exit", padx=8, pady=1, command=CloseWindow)
button_close.pack(side='left')







root.mainloop()
