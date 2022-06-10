import pandas as pd
class File:
    def _init_(self, name, type):
        self.name = name
        self.type = type

def convert(input, output):
    file_name, file_extension = os.path.splitext("/Users/pankaj/abc.txt")
    type = file_extension
    if file.endswith(".csv"):
        if output_type == 'xlsx':
            csv_to_xlsx()
        if output_type == 'parquet':
            csv_parquet()
    if file.endswith(".parquet"):
        if output_type == 'csv':
            parquet_csv()
    if file.endswith(".txt"):
        if output_type == 'csv':
            txt_csv()
        if output_type == 'xlsx':
            txt_xlsx()
    if file.endswith(".xls"):

    if file.endswith(".json"):
    if file.endswith(".XML"):


[1:14 PM] Douglas Post
csv -> xlsx
csv -> parquet
parquet -> csv
xlsx -> parquet
txt -> csv
txt -> xlsx
xls -> xlsx
json -> csv
json -> xlsx
XML -> json
XML -> csv
XML -> xlsx

[1:15 PM] Douglas Post
From: csv, txt, xlsx, parquet, json, xml, xlsTo: csv, txt, xlsx, parquet, json, xml


def csv_to_xlsx(input_path, output_path):
    read_file = pd.read_csv (r'input_path')
    read_file.to_excel (r'output_path', index = None, header=True)

def csv_parquet(input_path, output_path):
    df = pd.read_csv('example.csv')
    df.to_parquet('output.parquet')

def parquet_csv(input_path, output_path):
    df = pd.read_parquet('filename.parquet')
    df.to_csv('filename.csv')

def xlsx_parquet(input_path, output_path):
    df = pd.DataFrame(pd.read_excel("Test.xlsx"))
    csv = read_file.to_csv ("Test.csv",
                  index = None,
                  header=True)
    csv_parquet(csv, output_path)

def txt_csv():
    read_file = pd.read_csv (r'Path where the Text file is stored\File name.txt')
    read_file.to_csv (r'Path where the CSV will be saved\File name.csv', index=None)

def txt_xlsx():
    txt

def xls_xlsx():


def json_csv():
    df = pd.read_json('export.json', orient='index')
    csv = df.to_csv(index=False)

def json_xlsx():
    df_json = pd.read_json(‘DATAFILE.json’)
    df_json.to_excel(‘DATAFILE.xlsx’)

# def XML_json():
#
# def XML_csv():
#
# def XML_xlsx():



def main()
