from flask import request, Blueprint, redirect, url_for
import os
import shutil  
import pathlib
import time
from api.service.response import response
from api.service.errorhandling import ErrorHandling

file_view = Blueprint('file_view', __name__, url_prefix="/api/v3/")

start = None

UPLOAD_DIR = "/home/divum/Desktop/FlaskJWT/uploads/"
COPY_DIR = "/home/divum/Desktop/FlaskJWT/CopiedFiles/"
EXTENSION_DIR = "/home/divum/Desktop/FlaskJWT/FileExtensions/"

@file_view.route('/upload', methods=['POST'])
async def upload_blob():
    try:
        global start
        start = time.time()
        if 'blob' not in request.files:
            return ErrorHandling.hanlde_bad_request('No blob part in the request')
            
        files = request.files.getlist("blob")
    
        for file in files: 
            if file.filename == '':
                return ErrorHandling.hanlde_bad_request('File name is empty !!')
              
            file.save(UPLOAD_DIR + file.filename)
        
        return redirect(url_for('file_view.file_upload'))
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))
    

@file_view.route("/file_copyandmove")
def file_upload():
    try:
        source_directory = UPLOAD_DIR
        files = os.listdir(source_directory)
    
        for file in files:
            
            source = os.path.join(source_directory,file)
            destination = os.path.join(COPY_DIR,file)
            shutil.copy(source, destination)
    
            file_extension = pathlib.Path(source_directory + file).suffix
            
            source = os.path.join(source_directory, file)
    
            if file_extension == '':
                continue
            
            destination_directory = os.path.join(EXTENSION_DIR, file_extension[1:])
            destination = os.path.join(destination_directory, file)
    
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory, exist_ok=True)
            
            shutil.move(source, destination)    
    
        end = time.time()
        total = end - start
        total_time = round(total,4)
        return response.function(f'Executed in {total_time} seconds')
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))

@file_view.route("/copy_files")
def copy_from_local_folder():
    try:
        files = os.listdir(UPLOAD_DIR)
    
        for file in files:
            source = os.path.join(UPLOAD_DIR,file)
            destination = os.path.join(COPY_DIR,file)
            shutil.copy(source, destination)
    
        return response.function("File Copied")
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))


async def copying_file(source, destination, file):
    try:
        shutil.copy(source, destination)
        file_extension = pathlib.Path(source).suffix
    
        if file_extension == '':
            return ErrorHandling.hanlde_bad_request("No Extension found for the file")
    
        destination_directory = os.path.join(EXTENSION_DIR, file_extension[1:])
        destination = os.path.join(destination_directory, file)
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory, exist_ok=True)
        await moving_file(source, destination)
        return response.function("File Operation Done Successfully")
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))

async def moving_file(source, destination):
    try:
        shutil.move(source, destination)
        return response.function("File moved Successfully")
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))
    
async def file_handling():
    try:
        source_directory = UPLOAD_DIR
    
        files = os.listdir(source_directory)
    
        for file in files:
            source = os.path.join(source_directory, file)
            desti = os.path.join(COPY_DIR, file)
    
            copying_file(source, desti, file)
    
        return response.function("File handled SuccessFully")
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))

@file_view.route('/async_upload', methods=['POST'])
async def upload_file():
    try:
        start = time.time()
        if 'blob' not in request.files:
            return ErrorHandling.hanlde_bad_request("Blob not in the request")
    
        files = request.files.getlist("blob")
    
        for file in files:
            if file.filename == '':
                return ErrorHandling.hanlde_bad_request('File name is empty !!')
    
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            file.save(file_path)
    
        await file_handling()
        
        end = time.time()
        total = end - start
        total_time = round(total,4)
        return response.function(str(f'Executed in {total_time} seconds'))
    
    except Exception as e:
        return ErrorHandling.handle_server_request(str(e))