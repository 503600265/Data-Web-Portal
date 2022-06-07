from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import SelectMultipleField, RadioField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, length
from app import app
from app.models import Users


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField('Username', default='Enter Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class SingleFileUploadForm(FlaskForm):
    data_file = FileField('Upload Data',
                          validators=[
                              FileRequired(),
                              FileAllowed(app.config['ALLOWED_EXTENSIONS'],
                                          'Only {' + ", ".join(app.config['ALLOWED_EXTENSIONS']) + "} files allowed!")
                          ])
    submit = SubmitField('Upload')


class ToolSelectForm(FlaskForm):
    selection = RadioField("What do you want to do with your data?",default='ocr',
                           choices = [('ocr','OCR Documents'),('toparquet','Convert to Parquet'),
                                      ('tohdfs',"Upload Data to HDFS"),('tos3','Upload Data to S3')],
                           validate_choice=True)
    submit = SubmitField('Submit Job')


class ConvertForm(FlaskForm):
    submit = SubmitField('Convert Data')
