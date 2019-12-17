from flask import Flask
import os
import errno

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
try:
    os.makedirs(UPLOAD_FOLDER)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 * 1024