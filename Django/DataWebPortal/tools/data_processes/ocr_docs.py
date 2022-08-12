import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import os
import PyPDF2
import io
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/username/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'  # your path may be different


def ocr_pdf(input_dir, output_dir, output_type):
    images = convert_from_path(input_dir)
    pdf_writer = PyPDF2.PdfFileWriter()
    cfg_filename = r'--oem 3 --psm 6'
    if output_type == 'pdf':
        for image in images:
            page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
            pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
            pdf_writer.addPage(pdf.getPage(0))
        # export the searchable PDF to searchable.pdf
        base = os.path.basename(input_dir)
        file_name = os.path.splitext(base)[0]
        print(file_name)
        head, tail = os.path.split(output_dir)
        print(head)
        destination = str(head) +"\\" +str(file_name) + '.' + output_type
        print(destination)
        with open(destination, "wb") as f:
            pdf_writer.write(f)
            f.close()
    if output_type == 'hocr':
        base = os.path.basename(input_dir)
        file_name = os.path.splitext(base)[0]
        print(file_name)
        head, tail = os.path.split(output_dir)
        print(head)
        destination = str(head) +"\\" +str(file_name) + '.' + output_type
        print(destination)
        for image in images:
            page = pytesseract.image_to_pdf_or_hocr(image, extension='hocr')
            if os.path.exists(destination):
                if isinstance(page, str):
                    append_write = 'a' # append if already exists
                    newline = "\n"
                else:
                    append_write = 'ab' # append if already exists
                    newline = bytes("\n", 'utf-8')
                with open(destination, append_write) as f:
                    f.write(newline)
                    f.write(page)
                    f.close()
            else:
                if isinstance(page, str):
                    append_write = 'w' # append if already exists
                else:
                    append_write = 'wb' # append if already exists              with open(destination, append_write) as f:
                with open(destination, append_write) as f:
                    f.write(page)
                    f.close()
    if output_type == 'txt':
        base = os.path.basename(input_dir)
        file_name = os.path.splitext(base)[0]
        print(file_name)
        head, tail = os.path.split(output_dir)
        print(head)
        destination = str(head) +"\\" +str(file_name) + '.' + output_type
        print(destination)
        for image in images:
            page = pytesseract.run_and_get_output(image, extension='txt', config=cfg_filename)
            if os.path.exists(destination):
                if isinstance(page, str):
                    append_write = 'a' # append if already exists
                    newline = "\n"
                else:
                    append_write = 'ab' # append if already exists
                    newline = bytes("\n", 'utf-8')
                with open(destination, append_write) as f:
                    f.write(newline)
                    f.write(page)
                    f.close()
            else:
                if isinstance(page, str):
                    append_write = 'w' # append if already exists
                else:
                    append_write = 'wb' # append if already exists              with open(destination, append_write) as f:
                with open(destination, append_write) as f:
                    f.write(page)
                    f.close()
    if output_type == 'xml':
        base = os.path.basename(input_dir)
        file_name = os.path.splitext(base)[0]
        print(file_name)
        head, tail = os.path.split(output_dir)
        print(head)
        destination = str(head) +"\\" +str(file_name) + '.' + output_type
        print(destination)
        for image in images:
            page = pytesseract.image_to_alto_xml(image)
            if os.path.exists(destination):
                if isinstance(page, str):
                    append_write = 'a' # append if already exists
                    newline = "\n"
                else:
                    append_write = 'ab' # append if already exists
                    newline = bytes("\n", 'utf-8')
                with open(destination, append_write) as f:
                    f.write(newline)
                    f.write(page)
                    f.close()
            else:
                if isinstance(page, str):
                    append_write = 'w' # append if already exists
                else:
                    append_write = 'wb' # append if already exists              with open(destination, append_write) as f:
                with open(destination, append_write) as f:
                    f.write(page)
                    f.close()


def ocr_image(input_dir, output_dir, output_type):
    image = cv2.imread(input_dir)
    cfg_filename = r'--oem 3 --psm 6'
    if output_type == 'pdf':
        data = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
    if output_type == 'hocr':
        data = pytesseract.image_to_pdf_or_hocr(image, extension='hocr')
    if output_type == 'txt':
        data = pytesseract.run_and_get_output(image, extension='txt', config=cfg_filename)
    if output_type == 'xml':
        data = pytesseract.image_to_alto_xml(image)
    base = os.path.basename(input_dir)
    file_name = os.path.splitext(base)[0]
    print(file_name)
    head, tail = os.path.split(output_dir)
    print(head)
    destination = str(head) +"\\" +str(file_name) + '.' + output_type
    print(destination)
    print(type(data))
    if isinstance(data, str):
        with open(destination, "w") as f:
            f.write(data)
            f.close()
    else:
        with open(destination, "wb") as f:
            f.write(data)
            f.close()

def ocr_file(input_dir, output_dir, output_type):
    file_name, file_extension = os.path.splitext(input_dir)
    input_type = file_extension
    if input_type == ".pdf":
        ocr_pdf(input_dir, output_dir, output_type)
    else:
        ocr_image(input_dir, output_dir, output_type)

