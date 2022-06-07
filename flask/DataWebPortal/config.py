import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    UPLOAD_PATH = 'Data/Uploads/'
    OUTPUT_PATH = 'Data/Output/'
    ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv', '.json', '.xml', '.jpg', '.jpeg',
                          '.gif', '.png', '.xls', '.xlsx', '.tiff', '.svg', '.parquet',
                          '.tsv', '.dat', '.doc', '.docx', '.html']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'DataWebPortal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
