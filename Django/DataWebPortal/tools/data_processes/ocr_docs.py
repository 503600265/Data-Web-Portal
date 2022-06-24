# import os
# import sys
# import argparse
# import subprocess
#
# def set_up(paths, list_dir):
#     if list_dir == "list":
#         if not os.path.isdir(paths):
#             sys.exit("Input directory is not a directory or does not exist")
#
#         path_list = []
#         with open(paths,'r') as f:
#             for line in f.readlines():
#                 if line.split('.')[-1].lower().strip() == "pdf":
#                     path_list.append(line.strip())
#     else:
#         if not os.path.isfile(paths):
#             sys.exit("File list file is not a file or does not exist")
#         path_list = []
#         for root, dir, files in os.walk(paths):
#             for f in files:
#                 if f.split('.')[-1].lower().strip() == "pdf":
#                     path_list.append(os.path.join(root,f))
#
#     path_dict = dict()
#     path_dict['full_path'] = path_list
#     path_dict['basename'] = [os.path.basename(x) for x in path_list]
#     return path_dict
#
# def output_setup(files, loc, suffix = ""):
#     if not os.path.isdir(loc):
#         os.makedirs(loc)
#
#     output_basenames = [os.path.splitext(x)[0]+suffix+".pdf" for x in files['basename']]
#     output_fullpaths = [os.path.join(loc,x) for x in output_basenames]
#
#     output_dict = dict()
#     output_dict['full_path'] = output_fullpaths
#     output_dict['basename'] = output_basenames
#     return output_dict
#
# def ocr_doc(inpdf, outpdf, rot_conf = None, out_type =None, DPI = None):
#     arg_list = []
#     if DPI:
#         ocr_dpi = DPI
#         arg_list = arg_list+['--oversample',DPI]
#     else:
#         ocr_dpi = None
#
#     if rot_conf:
#         rotation_conf = rot_conf
#     else:
#         rotation_conf = 3
#     arg_list = arg_list + ['--rotate-pages-threshold',rotation_conf]
#
#     if out_type:
#         output = out_type
#     else:
#         output = "pdfa"
#     arg_list = arg_list + ['--output_type',output]
#
#     return_info = subprocess.run(['ocrmypdf', '--rotate-pages','--deskew', '--remove_background',
#                                   '--clean','--skip-text'] + arg_list + [inpdf, outpdf],
#                                  capture_output=True)
#     return return_info
#
# def main(args):
#     # Set up input file list
#     if not ((args.input_dir) & (args.file_list)):
#         print("Error: Need to specify the files to be OCRd using either, --input_dir or --file_list arguments.")
#         sys.exit(0)
#     if ((args.input_dir) & (args.file_list)):
#         print("Error: Need to specify exactly one of --input_dir or --file_list")
#         sys.exit(0)
#     if args.file_list:
#         infile_dict = set_up(args, "list")
#     else:
#         infile_dict = set_up(args,"dir")
#
#     # Set up output directory and output file names
#     if args.output_dir:
#         if not args.suffix:
#             outfile_dict = output_setup(infile_dict, loc = args.output_dir)
#         else:
#             outfile_dict = output_setup(infile_dict, loc = args.output_dir, suffix = args.suffix)
#     else:
#         if not args.suffix:
#             outfile_dict = output_setup(infile_dict, loc=args.input_dir, suffix = "_ocr")
#         else:
#             outfile_dict = output_setup(infile_dict, loc=args.input_dir, suffix=args.suffix)
#
#     # OCR the Documents
#     for infile, outfile in zip(infile_dict['full_path'],outfile_dict['full_path']):
#         ocr_doc(infile, outfile, rot_conf=args.rotate_thresh, out_type=args.out_type, DPI=args.DPI)
#
# if __name__ == "__main__":
#     argument_parser = argparse.ArgumentParser(prog="OCR Documents",
#                                               description="Convert Non-Searchable PDF to Searchable PDF")
#     argument_parser.add_argument('-h', '--help',
#                                  help="Print help for script")
#
#     argument_parser.add_argument('-i', '--input_dir',
#                                  help="The directory containing the raw PDF files that will be converted")
#
#     argument_parser.add_argument('-f', '--file_list',
#                                  help="If you would prefer to specify a list of files in a text file with each \
# file on a seperate line, this will work in place of the --input_dir argument.")
#
#     argument_parser.add_argument('-o', '--output_dir',
#                                  help="The location where you would like the output file(s). If not specified, \
# will create files with _ocr appended to the end of the filename in the same directory as the file.")
#
#     argument_parser.add_argument('-d', '--DPI',
#                                  help="The DPI you would like the tool to use during conversion, the default does it \
# automatically, but a higher DPI can sometimes improve results")
#
#     argument_parser.add_argument('-r', '--rotate_thresh',
#                                  help="The confidence threshold for rotating pages, which is how ratio of how \
# likely the program believes the page needs to be rotated vs. how likely it believes the page does not. The default \
# is 5.0 because a lower rotation threshold can work better with difficult documents, but this can make also \
# unintentional rotations happen. If documents are being rotated too often, increase this value to 7.5 or 10, or \
# if they aren't decrease to 2 or 3.")
#
#     argument_parser.add_argument('-t', '--out_type',
#                                  help="The output type/format of your outputted PDF file. The default is PDF-2/A \
# compliance format, but speicifying just 'pdf' will make it convert to standard pdf compliance, however the compression \
# of standard pdf tends to be worse than PDF-2/A, so some of your files could get a little (or sometimes a lot) \
# larger after OCR in standard format")
#
#     argument_parser.add_argument('-s', '--suffix',
#                                  help="The suffix you would like appended to your files, if you would like one at all. \
# If no output directory specified, this argument would override the _ocr suffix, otherwise OCRd documents will be put in \
# the directory specified by output_dir, with this suffix appended.")
#     arguments = argument_parser.parse_args()
#     main(arguments)
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import os
import PyPDF2
import io
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/jxu/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'  # your path may be different

# In[2]:


# IMG_DIR = 'images/'
#
#
# # ### Preprocessing of images using OpenCV
# #
# # We will write basic functions for different preprocessing methods
# # - grayscaling
# # - thresholding
# # - dilating
# # - eroding
# # - opening
# # - canny edge detection
# # - noise removal
# # - deskwing
# # - template matching.
# #
# # Different methods can come in handy with different kinds of images.
#
# # In[3]:
#
#
# # get grayscale image
# def get_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # noise removal
# def remove_noise(image):
#     return cv2.medianBlur(image,5)
#
# #thresholding
# def thresholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#
# #dilation
# def dilate(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.dilate(image, kernel, iterations = 1)
#
# #erosion
# def erode(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.erode(image, kernel, iterations = 1)
#
# #opening - erosion followed by dilation
# def opening(image):
#     kernel = np.ones((5,5),np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
# #canny edge detection
# def canny(image):
#     return cv2.Canny(image, 100, 200)
#
# #skew correction
# def deskew(image):
#     coords = np.column_stack(np.where(image > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return rotated
#
# #template matching
# def match_template(image, template):
#     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
#
#
# # In[4]:
#
#
# # Plot original image
#
# image = cv2.imread(IMG_DIR + 'aurebesh.jpg')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.imshow(rgb_img)
# plt.title('AUREBESH ORIGINAL IMAGE')
# plt.show()
#
#
# # In[5]:
#
#
# # Preprocess image
#
# gray = get_grayscale(image)
# thresh = thresholding(gray)
# opening = opening(gray)
# canny = canny(gray)
# images = {'gray': gray,
#           'thresh': thresh,
#           'opening': opening,
#           'canny': canny}
#
#
# # In[6]:
#
#
# # Plot images after preprocessing
#
# fig = plt.figure(figsize=(13,13))
# ax = []
#
# rows = 2
# columns = 2
# keys = list(images.keys())
# for i in range(rows*columns):
#     ax.append( fig.add_subplot(rows, columns, i+1) )
#     ax[-1].set_title('AUREBESH - ' + keys[i])
#     plt.imshow(images[keys[i]], cmap='gray')
#
#
# # In[7]:
#
#
# # Get OCR output using Pytesseract
#
# custom_config = r'--oem 3 --psm 6'
# print('-----------------------------------------')
# print('TESSERACT OUTPUT --> ORIGINAL IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(image, config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> THRESHOLDED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(image, config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> OPENED IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(image, config=custom_config))
# print('\n-----------------------------------------')
# print('TESSERACT OUTPUT --> CANNY EDGE IMAGE')
# print('-----------------------------------------')
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # ### Bounding box information using Pytesseract
# #
# # While running and image through the tesseract OCR engine, pytesseract allows you to get bounding box imformation
# # - on a character level
# # - on a word level
# # - based on a regex template
# #
# # We will see how to obtain both
#
# # In[8]:
#
#
# # Plot original image
#
# image = cv2.imread(IMG_DIR + 'invoice-sample.jpg')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
#
# plt.figure(figsize=(16,12))
# plt.imshow(rgb_img)
# plt.title('SAMPLE INVOICE IMAGE')
# plt.show()
#
#
# # In[9]:
#
#
# # Plot character boxes on image using pytesseract.image_to_boxes() function
#
# image = cv2.imread(IMG_DIR + 'invoice-sample.jpg')
# h, w, c = image.shape
# boxes = pytesseract.image_to_boxes(image)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
#
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
#
# plt.figure(figsize=(16,12))
# plt.imshow(rgb_img)
# plt.title('SAMPLE INVOICE WITH CHARACTER LEVEL BOXES')
# plt.show()
#
#
# # In[10]:
#
#
# # Plot word boxes on image using pytesseract.image_to_data() function
#
# image = cv2.imread(IMG_DIR + 'invoice-sample.jpg')
# d = pytesseract.image_to_data(image, output_type=Output.DICT)
# print('DATA KEYS: \n', d.keys())
#
# n_boxes = len(d['text'])
# for i in range(n_boxes):
#     # condition to only pick boxes with a confidence > 60%
#     if int(d['conf'][i]) > 60:
#         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#         image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.figure(figsize=(16,12))
# plt.imshow(rgb_img)
# plt.title('SAMPLE INVOICE WITH WORD LEVEL BOXES')
# plt.show()
#
#
# # In[11]:
#
#
# # Plot boxes around text that matches a certain regex template
# # In this example we will extract the date from the sample invoice
#
# image = cv2.imread(IMG_DIR + 'invoice-sample.jpg')
# date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
#
# n_boxes = len(d['text'])
# for i in range(n_boxes):
#     if int(d['conf'][i]) > 60:
#         if re.match(date_pattern, d['text'][i]):
#             (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#             image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.figure(figsize=(16,12))
# plt.imshow(rgb_img)
# plt.title('SAMPLE INVOICE WITH BOXES FOR DATES')
# plt.show()
#
#
# # ### Page Segmentation Modes
# #
# # There are several ways a page of text can be analysed. The tesseract api provides several page segmentation modes if you want to run OCR on only a small region or in different orientations, etc.
# #
# # Here's a list of the supported page segmentation modes by tesseract -
# #
# # 0    Orientation and script detection (OSD) only.
# # 1    Automatic page segmentation with OSD.
# # 2    Automatic page segmentation, but no OSD, or OCR.
# # 3    Fully automatic page segmentation, but no OSD. (Default)
# # 4    Assume a single column of text of variable sizes.
# # 5    Assume a single uniform block of vertically aligned text.
# # 6    Assume a single uniform block of text.
# # 7    Treat the image as a single text line.
# # 8    Treat the image as a single word.
# # 9    Treat the image as a single word in a circle.
# # 10    Treat the image as a single character.
# # 11    Sparse text. Find as much text as possible in no particular order.
# # 12    Sparse text with OSD.
# # 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
# #
# # To change your page segmentation mode, change the ```--psm``` argument in your custom config string to any of the above mentioned mode codes.
#
# # ### Detect orientation and script
# #
# # You can detect the orientation of text in your image and also the script in which it is written.
#
# # In[12]:
#
#
# # Plot original image
#
# image = cv2.imread(IMG_DIR + 'hitchhikers-rotated.png')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.figure(figsize=(16,12))
# plt.imshow(rgb_img)
# plt.title('HITCHHIKERS - ROTATED')
# plt.show()
#
#
# # In[13]:
#
#
# # Get angle and script
#
# osd = pytesseract.image_to_osd(image)
# angle = re.search('(?<=Rotate: )\d+', osd).group(0)
# script = re.search('(?<=Script: )\w+', osd).group(0)
# print("angle: ", angle)
# print("script: ", script)
#
#
# # ### Playing around with the config
# #
# # By making minor changes in the config file you can
# # - specify language
# # - detect only digits
# # - whitelist characters
# # - blacklist characters
# # - work with multiple languages
#
# # In[14]:
#
#
# # Plot original image
#
# image = cv2.imread(IMG_DIR + 'digits-task.jpg')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.imshow(rgb_img)
# plt.title('SAMPLE TABLE')
# plt.show()
#
#
# # In[15]:
#
#
# # Original tesseract output with english language sepcified
#
# custom_config = r'-l eng --oem 3 --psm 6'
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # In[16]:
#
#
# # Output with outputbase digits
#
# custom_config = r'--oem 3 --psm 6 outputbase digits'
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # In[17]:
#
#
# # Output with a whitelist of characters (here, we have used all the lowercase characters from a to z only)
#
# custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz --psm 6'
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # In[18]:
#
#
# # Output without the blacklisted characters (here, we have removed all digits)
#
# custom_config = r'-c tessedit_char_blacklist=0123456789 --psm 6'
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # In[19]:
#
#
# # working with multiple languages
#
# # Plot original image
#
# image = cv2.imread(IMG_DIR + 'greek-thai.png')
# b,g,r = cv2.split(image)
# rgb_img = cv2.merge([r,g,b])
# plt.figure(figsize=(8,16))
# plt.imshow(rgb_img, cmap = 'gray')
# plt.title('MULTIPLE LANGUAGE IMAGE')
# plt.show()
#
#
# # In[20]:
#
#
# # Output with only english language specified
#
# custom_config = r'-l eng --oem 3 --psm 6'
# print(pytesseract.image_to_string(image, config=custom_config))
#
#
# # In[21]:
#
#
# # Output with all languages specified
#
# custom_config = r'-l grc+tha+eng --oem 3 --psm 6'
# print(pytesseract.image_to_string(image, config=custom_config))

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
    # print(pytesseract.image_to_string(image, config=custom_config))
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
# ocr('H:\Downloads\ocr-with-tesseract-master\images\invoice-sample.jpg','H:\Downloads\ocr-with-tesseract-master\test.pdf', 'txt')
# ocr_pdf('H:\Downloads\sample.pdf','H:\Downloads\ocr-with-tesseract-master\sample.xml', 'xml')
