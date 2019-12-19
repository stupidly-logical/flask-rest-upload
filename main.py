import os
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import threading

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

STATUSES = ['READY', 'UPLOADING', 'PAUSED', 'STOPPED', 'UPLOADED']

STATUS = STATUSES[0]

e = threading.Event()

def is_stopped():
    global STATUS
    return 1 if STATUS == STATUSES[3] else 0

def is_paused():
    global STATUS
    return 1 if STATUS == STATUSES[2] else 0

def is_uploading():
    global STATUS
    return 1 if STATUS == STATUSES[1] else 0

def is_uploaded():
    global STATUS
    return 1 if STATUS == STATUSES[4] else 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/status', methods=['GET', 'POST', 'PUT'])
def get_status():
    global STATUS
    resp = jsonify({'status': STATUS})
    resp.status_code = 201
    return resp

@app.route('/pause', methods=['GET', 'POST', 'PUT'])
def pause_upload():
    global STATUS
    if STATUS != STATUSES[1]:
        print('Pause not required', STATUS)
        resp = jsonify({'message': 'Pause not required'})
        resp.status_code = 201
        return resp
    e.clear()
    STATUS = STATUSES[2]
    print(STATUS)
    resp = jsonify({'message': 'File upload paused'})
    resp.status_code = 201
    return resp

@app.route('/resume', methods=['GET', 'POST', 'PUT'])
def resume_upload():
    global STATUS
    if STATUS != STATUSES[2]:
        print('Not required', STATUS)
        resp = jsonify({'message': 'Resume not required'})
        resp.status_code = 201
        return resp
    e.set()
    STATUS = STATUSES[1]
    print(STATUS)
    resp = jsonify({'message': 'File upload resumed'})
    resp.status_code = 201
    return resp

@app.route('/stop', methods=['GET', 'POST', 'PUT'])
def stop_upload():
    global STATUS
    if STATUS != STATUSES[1] and STATUS != STATUSES[2]:
        print('Stop not required', STATUS)
        resp = jsonify({'message': 'Already Stopped'})
        resp.status_code = 201
        return resp
    e.set()
    STATUS = STATUSES[3]
    print('Stopping')
    resp = jsonify({'message':'Stopping'})
    resp.status_code = 201
    return resp

@app.route('/upload', methods=['GET', 'POST', 'PUT'])
def start_upload():
    global STATUS
    if STATUS == STATUSES[1]:
        resp = jsonify({'message': 'Wait for upload to complete'})
        resp.status_code = 400
        return resp
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    print('here1')
    file = request.files['file']
    print('here2')
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filestream = file.stream
        e.set()
        flag = 1
        STATUS = STATUSES[1]
        print("Uplaoding file...")
        with open(filepath, 'wb') as newfile:
            for line in filestream:
                e.wait()
                if STATUS == STATUSES[3]:
                    flag = 0
                    break
                print(line, sep='')             # comment this, this exists for debugging
                newfile.write(line)
        if flag == 0:
            STATUS = STATUSES[3]
            os.remove(filepath)
            print("File upload was stopped")
            resp = jsonify({'message': 'File upload was stopped'})
            resp.status_code = 201
            return resp
        STATUS = STATUSES[0]
        print("File uploaded")
        resp = jsonify({'message': 'File uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route('/', methods=['GET', 'POST', 'PUT'])
def root():

    global STATUS
    resp = jsonify({'message': 'welcome','status': STATUS})
    resp.status_code = 201
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
