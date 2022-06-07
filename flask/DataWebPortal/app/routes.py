from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app import app
import subprocess
from app.functions import splitall
from app.forms import ToolSelectForm
from app.models import Users, Jobs, Activity
from werkzeug.utils import secure_filename

import os


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/explore_data')
def explore_data():
    return render_template('explore_data.html', title="Explore")


@app.route('/Data/Uploads/<path:filename>')
def download(filename):
    upload_dir = os.path.join(os.path.dirname(app.root_path), app.config["UPLOAD_PATH"])
    return send_from_directory(upload_dir, filename, as_attachment=True)


@app.route("/convert_data", methods=['GET', 'POST'])
def convert_data():
    if request.method == 'POST':
        upload_directory = os.path.join(os.path.dirname(app.root_path), app.config["UPLOAD_PATH"])

        if request.files['file']:
            uploaded_files = request.files.getlist('file')
#        elif request.files.getlist('file[]'):
#            uploaded_files = request.files.getlist('file[]')
        else:
            flash("Need to select at least one file.")
            return redirect(url_for('convert_data'))

        for uploaded_file in uploaded_files:
            if uploaded_file.filename != '':
                file_name = secure_filename(uploaded_file.filename)
                file_ext = os.path.splitext(file_name)[1].lower()

                if file_ext not in app.config["ALLOWED_EXTENSIONS"]:
                    return "Invalid Extension", 400

                uploaded_file.save(os.path.join(upload_directory, file_name))
        flash("File upload complete!")
        return redirect(url_for('convert_data'))

    files = os.listdir(app.config["UPLOAD_PATH"])
    return render_template('convert_data.html', files=files)


@app.route('/select_tool', methods=['GET', 'POST'])
def select_tool():
    tools = {'ocr':'ocr.py','toparquet':'convert_to_parquet.py',
             'tos3':'upload_to_s3.py','tohdfs':'upload_to_hdfs.py'}
    form = ToolSelectForm()
    if form.validate_on_submit():
        action_script = tools[form.selection.data]
        # subprocess.run(action_script in tmux window or something like that)
        # return the new location of the data
        flash("Performing "+form.selection.data+" on data.")
        return redirect(url_for('select_tool'))
    return render_template('select_tool.html',title="Select Tool", form=form)

@app.route('/ocr_tool', methods=['GET', 'POST'])
def ocr_tool():
    return render_template('ocr_tool.html', title="OCR Tool")

@app.route('/progressPage',methods=['GET','POST'])
def progressPage():
    subprocess.run(['./tmux_scrn_shot.sh'])
    return render_template('progressPage.html',title="Progress")

@app.route('/contact')
def contact_help():
    return render_template('contact.html', title="Contact & Help")
