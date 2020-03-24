#!/usr/bin/python
# -*- coding:utf -8 -*-

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

class ConvertFile:

    def __init__(self):
        pass

    def numberSteps(self, num_page, page_start, page_step):
        steps = list(range(page_start, num_page, page_step))
        steps.append(num_page)
        return steps

    def splitPdf(self, input_file, step):
        """
        Функция разделяет ПДФ на файлы согласно заданного диапазона
        :param filename: имя файла, обязательный параметр, тип str
        :param start: начало отсчёта диапазона, по умолчанию 0, тип int.
        :param step: шаг диапазона, по умолчанию 50 страниц, тип int.
        :return: возвращает несколько файлов по количеству диапазонов (имя генерируется по умолчанию).
        """
        pdf_input = PyPDF2.PdfFileReader(open(input_file, 'rb'))
        steps = self.numberSteps(num_page=pdf_input.getNumPages(),
                                 page_start=0, page_step=step)
        new_outfile_path, new_outfile_format = os.path.splitext(input_file)
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

    # def formatDefinition(self, input):
    #     for i in input:
    #         path, format = os.path.split(i)

# TODO Переписать функцию, убрать цикл и дописать автоматическое определение каким образом формировать файл ПДФ
    def to_pdf(self, in_file, out_file, page=0):
        if page == 0:
            im = Image.open(in_file)
            im.save(out_file, 'PDF', save_all=True)
        else:
            im = Image.open(in_file)
            im.save(out_file, append=True)

    def to_jpg(self, in_file, out_file):
        im = Image.open(in_file)
        size = im.size
        new_size = (size[0] // 2, size[1] // 2)
        img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
        img = img_resize.convert(mode='1')
        img.save(out_file, 'JPEG', optimize=True, dpi=(150, 150))

    def to_png(self, in_file, out_file):
        im = Image.open(in_file)
        size = im.size
        new_size = (size[0] // 2, size[1] // 2)
        img_resize = im.resize(size=new_size, resample=1, reducing_gap=3.0)
        img = img_resize.convert(mode='1')
        img.save(out_file, 'PNG', optimize=True, dpi=(150, 150))

    def process(self, input_file, output_file, format, split_step=0):
        """

        :param input: список файлов
        :param output: имя результирующего файла
        :param format: формат результирующего файла
        :param split_step: количество страниц на которое разбивается файл ПДФ
        :param split_start: начальная страница
        :return: в директории сохраняются файлы
        """
        print('Input=', input_file)
        print('Output=', output_file)
        print('Format=', format)
        print('split_step=', split_step)
        output_path, output_format = os.path.splitext(output_file)
        for i in input_file:
            print()
            if format == '.pdf':
                input_path, input_format = os.path.splitext(i)
                output_jpg = output_path + '.jpg'
                input_jpg = output_path + '.jpg'
                output_file = output_path + format
                self.to_jpg(i, output_jpg)
                self.to_pdf(input_jpg, output_file)
                del (input_format)
                del (input_path)
            elif format == '.jpg':
                input_path, input_format = os.path.splitext(i)
                output_file = input_path + format
                self.to_jpg(i, output_file)
                del(input_format)
            elif format == '.png':
                input_path, input_format = os.path.splitext(i)
                output_file = input_path + format
                self.to_png(i, output_file)
                del(input_format)
            else:
                pass
        if split_step > 0:
            self.splitPdf(output_file, step=split_step)
        else:
            pass
        del(output_format)
    # def ConvertFile(var, split):
    #     if var == 0:
    #         i = 0
    #         for infile in list_files:
    #             i += 1
    #             outfile = save_file_name
    #             file_path, file_format = os.path.splitext(save_file_name)
    #             temp_file = file_path + '-temp-'
    #             if i == 1:
    #                 try:
    #                     with Image.open(infile) as im:
    #                         size = im.size
    #                         new_size = (size[0]//2, size[1]//2)
    #                         img_resize = im.resize(
    #                             size=new_size, resample=1, reducing_gap=3.0)
    #                         img = img_resize.convert(mode='1')
    #                         img.save(temp_file, 'JPEG',
    #                                  optimize=True, dpi=(150, 150))
    #                     with Image.open(temp_file) as im2:
    #                         im2.save(outfile, save_all=True)
    #                         os.remove(temp_file)
    #                 except IOError:
    #                     print("1Невозможно конвертировать файл=", infile)
    #             else:
    #                 try:
    #                     with Image.open(infile) as im:
    #                         size = im.size
    #                         new_size = (size[0]//2, size[1]//2)
    #                         img_resize = im.resize(
    #                             size=new_size, resample=1, reducing_gap=3.0)
    #                         img = img_resize.convert(mode='1')
    #                         img.save(temp_file, 'JPEG',
    #                                  optimize=True, dpi=(150, 150))
    #                     with Image.open(temp_file) as im2:
    #                         im2.save(outfile, append=True)
    #                         os.remove(temp_file)
    #                 except IOError:
    #                     print("2Невозможно конвертировать файл=", infile)
    #     elif var == 1:
    #         for infile in list_files:
    #             file_path, file_format = os.path.splitext(infile)
    #             outfile = file_path + '.jpg'
    #             try:
    #                 with Image.open(infile) as im:
    #                     size = im.size
    #                     new_size = (size[0]//2, size[1]//2)
    #                     img_resize = im.resize(
    #                         size=new_size, resample=1, reducing_gap=3.0)
    #                     img = img_resize.convert(mode='1')
    #                     img.save(outfile, 'JPEG', optimize=True, dpi=(150, 150))
    #             except IOError:
    #                 print("3Невозможно конвертировать файл=", infile)
    #     else:
    #         print('Конвертирование остановлено')
    #     if split >= 5:
    #         split_pdf(filename=outfile, step=split)
    #     else:
    #         pass
