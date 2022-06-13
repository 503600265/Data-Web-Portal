import pandas as pd
import openpyxl
import pyarrow
import win32com.client as win32
import xlrd
from pathlib import Path
import json
import xmltodict
from xml2xlsx import xml2xlsx
# class File:
#     def _init_(self, name, type):
#         self.name = name
#         self.type = type
#
def convert(input_dir, output_dir, output_type):
    file_name, file_extension = os.path.splitext(input_dir)
    input_type = file_extension
    if input_type == ".csv":
        if output_type == 'xlsx':
            csv_to_xlsx(input_dir,output_dir)
        if output_type == 'parquet':
            csv_parquet(input_dir,output_dir)
    if input_type = ".parquet":
        if output_type == 'csv':
            parquet_csv(input_dir,output_dir)
    if input_type == ".xlsx":
        if out_type == 'parquet':
            xlsx_parquet(input_dir,output_dir)
    if input_type == ".txt":
        if output_type == 'csv':
            txt_csv(input_dir,output_dir)
        if output_type == 'xlsx':
            txt_xlsx(input_dir,output_dir)
    if input_type == ".xls":
        if output_type == 'xlsx':
            xls_xlsx(input_dir,output_dir)
    if input_type == ".json":
        if output_type == 'csv':
            json_csv(input_dir,output_dir)
        if output_type == 'xlsx':
            json_xlsx(input_dir,output_dir)
    if input_type == ".XML":


#
# [1:14 PM] Douglas Post
# csv -> xlsx
# csv -> parquet
# parquet -> csv
# xlsx -> parquet
# txt -> csv
# txt -> xlsx
# xls -> xlsx
# json -> csv
# json -> xlsx
# XML -> json
# XML -> csv
# XML -> xlsx
#
# [1:15 PM] Douglas Post
# From: csv, txt, xlsx, parquet, json, xml, xlsTo: csv, txt, xlsx, parquet, json, xml


def csv_to_xlsx(input_path, output_path):
    read_file = pd.read_csv (r'{}'.format(input_path))
    read_file.to_excel (r'{}'.format(output_path), index = None, header=True)
# csv_to_xlsx("H:\Downloads\DataWebPortal\cities.csv", "H:\Downloads\DataWebPortal\cities_csv_excel.xlsx" )

def csv_parquet(input_path, output_path):
    df = pd.read_csv(r'{}'.format(input_path))
    df.to_parquet(r'{}'.format(output_path))
# parquet_csv("H:\Downloads\DataWebPortal\cities.parquet", "H:\Downloads\DataWebPortal\cities2.csv" )

def parquet_csv(input_path, output_path):
    df = pd.read_parquet(r'{}'.format(input_path))
    df.to_csv(r'{}'.format(output_path), index = None)
# parquet_csv("H:\Downloads\DataWebPortal\cities2.parquet", "H:\Downloads\DataWebPortal\cities3.csv" )

def xlsx_parquet(input_path, output_path):
    df = pd.read_excel(r'{}'.format(input_path))
    df.to_parquet(r'{}'.format(output_path))
# xlsx_parquet("H:\Downloads\DataWebPortal\cities.xlsx", "H:\Downloads\DataWebPortal\cities3.parquet" )

def txt_csv(input_path, output_path):
    read_file = pd.read_csv (r'{}'.format(input_path))
    read_file.to_csv (r'{}'.format(output_path), index=None)
# txt_csv("H:\Downloads\DataWebPortal\cities.txt", "H:\Downloads\DataWebPortal\cities_txt_csv.csv" )

def txt_xlsx(input_path, output_path):
    read_file = pd.read_csv (r'{}'.format(input_path))
    read_file.to_excel (r'{}'.format(output_path), index = None, header=True)
# txt_xlsx("H:\Downloads\DataWebPortal\cities.txt", "H:\Downloads\DataWebPortal\cities_txt_excel.xlsx" )

def xls_xlsx(input_path,output_path):
    # df = pd.read_excel(r'{}'.format(input_path), header = None)
    # print(df)
    # df.to_excel(r'{}'.format(output_path), index=False, header=False)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(input_path)
    wb.SaveAs(output_path, FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()
# xls_xlsx("H:\Downloads\DataWebPortal\SampleXLSFile_19kb.xls", "H:\Downloads\DataWebPortal\SampleXLSFile_19kb2.xlsx")

def json_csv(input_path, output_path):
    # set path to file
    p = Path(r'{}'.format(input_path))
    # read json
    with p.open('r', encoding='utf-8') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    df.to_csv(r'{}'.format(output_path), index=False, encoding='utf-8')
# json_csv("H:\Downloads\DataWebPortal\sample.json", "H:\Downloads\DataWebPortal\sample3.csv")

def json_xlsx(input_path, output_path):
    df_json = pd.read_json(r'{}'.format(input_path))
    df_json.to_excel(r'{}'.format(output_path))
# json_xlsx("H:\Downloads\DataWebPortal\sample.json", "H:\Downloads\DataWebPortal\sample.xlsx")

def XML_json(input_path, output_path):
    with open(input_path, 'r') as f:
        data_dict = xmltodict.parse(f.read())
        f.close()
    json_data = json.dumps(data_dict)
    with open(output_path, "w") as json_file:
        json_file.write(json_data)
        json_file.close()
# XML_json("H:\Downloads\DataWebPortal\sample.xml", "H:\Downloads\DataWebPortal\sample.json")

# def XML_csv(input_path, output_path):
#
# def XML_xlsx():
#     with open(input_path, 'r') as f:
#         data = f.read()
#         f.close()
#     with open(output_path, "wb") as xlsx_file:
#         xlsx_file.write(xml2xlsx(data))
#         xlsx_file.close()
# XML_json("H:\Downloads\DataWebPortal\sample.xml", "H:\Downloads\DataWebPortal\sample.xlsx")

# def main()
