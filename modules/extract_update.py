from . import state
import zipfile
import os

def extractor():
    filename = state.user_os + ".zip"
    if zipfile.is_zipfile(filename):
        print("valid zip detected")
    else:
        print('Invalid zip detected')
        return
    print("Extracting to:", os.getcwd())
    with zipfile.ZipFile(filename, 'r') as zip:
        zip.extractall()