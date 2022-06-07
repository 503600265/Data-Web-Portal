import os
import sys
import argparse
import subprocess

def set_up(paths, list_dir):
    if list_dir == "list":
        if not os.path.isdir(paths):
            sys.exit("Input directory is not a directory or does not exist")

        path_list = []
        with open(paths,'r') as f:
            for line in f.readlines():
                if line.split('.')[-1].lower().strip() == "pdf":
                    path_list.append(line.strip())
    else:
        if not os.path.isfile(paths):
            sys.exit("File list file is not a file or does not exist")
        path_list = []
        for root, dir, files in os.walk(paths):
            for f in files:
                if f.split('.')[-1].lower().strip() == "pdf":
                    path_list.append(os.path.join(root,f))

    path_dict = dict()
    path_dict['full_path'] = path_list
    path_dict['basename'] = [os.path.basename(x) for x in path_list]
    return path_dict

def output_setup(files, loc, suffix = ""):
    if not os.path.isdir(loc):
        os.makedirs(loc)

    output_basenames = [os.path.splitext(x)[0]+suffix+".pdf" for x in files['basename']]
    output_fullpaths = [os.path.join(loc,x) for x in output_basenames]

    output_dict = dict()
    output_dict['full_path'] = output_fullpaths
    output_dict['basename'] = output_basenames
    return output_dict

def ocr_doc(inpdf, outpdf, rot_conf = None, out_type =None, DPI = None):
    arg_list = []
    if DPI:
        ocr_dpi = DPI
        arg_list = arg_list+['--oversample',DPI]
    else:
        ocr_dpi = None

    if rot_conf:
        rotation_conf = rot_conf
    else:
        rotation_conf = 3
    arg_list = arg_list + ['--rotate-pages-threshold',rotation_conf]

    if out_type:
        output = out_type
    else:
        output = "pdfa"
    arg_list = arg_list + ['--output_type',output]

    return_info = subprocess.run(['ocrmypdf', '--rotate-pages','--deskew', '--remove_background',
                                  '--clean','--skip-text'] + arg_list + [inpdf, outpdf],
                                 capture_output=True)
    return return_info

def main(args):
    # Set up input file list
    if not ((args.input_dir) & (args.file_list)):
        print("Error: Need to specify the files to be OCRd using either, --input_dir or --file_list arguments.")
        sys.exit(0)
    if ((args.input_dir) & (args.file_list)):
        print("Error: Need to specify exactly one of --input_dir or --file_list")
        sys.exit(0)
    if args.file_list:
        infile_dict = set_up(args, "list")
    else:
        infile_dict = set_up(args,"dir")

    # Set up output directory and output file names
    if args.output_dir:
        if not args.suffix:
            outfile_dict = output_setup(infile_dict, loc = args.output_dir)
        else:
            outfile_dict = output_setup(infile_dict, loc = args.output_dir, suffix = args.suffix)
    else:
        if not args.suffix:
            outfile_dict = output_setup(infile_dict, loc=args.input_dir, suffix = "_ocr")
        else:
            outfile_dict = output_setup(infile_dict, loc=args.input_dir, suffix=args.suffix)

    # OCR the Documents
    for infile, outfile in zip(infile_dict['full_path'],outfile_dict['full_path']):
        ocr_doc(infile, outfile, rot_conf=args.rotate_thresh, out_type=args.out_type, DPI=args.DPI)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(prog="OCR Documents",
                                              description="Convert Non-Searchable PDF to Searchable PDF")
    argument_parser.add_argument('-h', '--help',
                                 help="Print help for script")

    argument_parser.add_argument('-i', '--input_dir',
                                 help="The directory containing the raw PDF files that will be converted")

    argument_parser.add_argument('-f', '--file_list',
                                 help="If you would prefer to specify a list of files in a text file with each \
file on a seperate line, this will work in place of the --input_dir argument.")

    argument_parser.add_argument('-o', '--output_dir',
                                 help="The location where you would like the output file(s). If not specified, \
will create files with _ocr appended to the end of the filename in the same directory as the file.")

    argument_parser.add_argument('-d', '--DPI',
                                 help="The DPI you would like the tool to use during conversion, the default does it \
automatically, but a higher DPI can sometimes improve results")

    argument_parser.add_argument('-r', '--rotate_thresh',
                                 help="The confidence threshold for rotating pages, which is how ratio of how \
likely the program believes the page needs to be rotated vs. how likely it believes the page does not. The default \
is 5.0 because a lower rotation threshold can work better with difficult documents, but this can make also \
unintentional rotations happen. If documents are being rotated too often, increase this value to 7.5 or 10, or \
if they aren't decrease to 2 or 3.")

    argument_parser.add_argument('-t', '--out_type',
                                 help="The output type/format of your outputted PDF file. The default is PDF-2/A \
compliance format, but speicifying just 'pdf' will make it convert to standard pdf compliance, however the compression \
of standard pdf tends to be worse than PDF-2/A, so some of your files could get a little (or sometimes a lot) \
larger after OCR in standard format")

    argument_parser.add_argument('-s', '--suffix',
                                 help="The suffix you would like appended to your files, if you would like one at all. \
If no output directory specified, this argument would override the _ocr suffix, otherwise OCRd documents will be put in \
the directory specified by output_dir, with this suffix appended.")
    arguments = argument_parser.parse_args()
    main(arguments)