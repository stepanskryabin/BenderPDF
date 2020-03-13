import tkinter
from tkinter import filedialog as fd

root = tkinter.Tk()


button_open = tkinter.Button(root, text="Open file..")
button_save = tkinter.Button(root, text="Save file..")
button_close = tkinter.Button(root, text="Exit")
text_frame = tkinter.Text(root, width='10', height='10')


text_frame.pack()
button_open.pack()
button_save.pack()
button_close.pack()


def ListFiles(event):
    open = fd.askopenfilenames()

    return open


def SaveFileName(event):
    open = fd.asksaveasfilename(filetypes=[("Файл формата ПДФ", "*.pdf")], defaultextension='.pdf')
    return open

def CloseWindow(event):
    root.quit()


button_open.bind('<Button-1>', ListFiles)
button_save.bind('<Button-1>', SaveFileName)
button_close.bind('<Button-1>', CloseWindow)

class Convert:
    pass

class Files:
    pass

class MainWindow:
    pass

root.mainloop()
