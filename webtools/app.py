import csv
import tempfile
import os
import io
from io import StringIO
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, request, send_file, flash, redirect
from zipfile import ZipFile

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "webtools.config.DevelopmentConfig")
app.config.from_object(env_config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/csv/merge", methods=("POST",))
def merge():
    if 'file' not in request.files:
        flash("Please upload a file")
        return redirect(url_for('index'))

    file = request.files['file']
    if not file or not file.filename:
        flash("Please upload a file")
        return redirect(url_for('index'))
    if not file.filename.endswith(".zip"):
        flash("File must be a ZIP archive.")
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    fieldnames = []
    data = []
    with tempfile.TemporaryDirectory() as tmpdir:
        upload_name = os.path.join(tmpdir, filename)
        file.save(upload_name)
        with ZipFile(upload_name) as zipfile:
            for zipinfo in zipfile.infolist():
                with zipfile.open(zipinfo) as csvfile:
                    reader = csv.DictReader(io.TextIOWrapper(csvfile))
                    fieldnames.extend(f for f in reader.fieldnames if f not in fieldnames)
                    data.extend(reader)

    data_file = io.TextIOWrapper(io.BytesIO(), write_through=True)
    writer = csv.DictWriter(data_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    data_file.seek(0)
    return send_file(data_file.detach(), attachment_filename=f"merged.csv", as_attachment=True)
