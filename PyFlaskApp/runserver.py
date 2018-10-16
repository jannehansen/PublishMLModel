"""
---------------------------------------------
HOW TO OPERATIONALIZE PUBLISHED MODEL:
SAMPLE PYTHON FLASK APPLICATION
---------------------------------------------
This app shows how to load pre-trained
model from azure blob storage, 
Initialize the flask app once with the model,
and start serving callers with REST API.
---------------------------------------------
Licence: MIT, Janne Hansen 2018
"""

#imports
from os import environ

from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

import json

from azure.storage.blob import BlockBlobService, PublicAccess
import numpy as np

# Globals

# This is my fake model file in Azure Blob Storage
model_file = "my_model_on_azure.npy"

# This is my fake "model" for demo purposes
# In this demo, it's just pickled numpy array.
my_fake_model = None

# ---------------------------------------------------
# BEGIN: YOU NEED TO CHANGE THESE 
# ---------------------------------------------------

# These are keys and container name to access Azure blob storage
# Modify these to match your azure storage account!

storagename = "mystorageaccountnamehere"
storagekey = "mystorageaccountkeyhere"
storagecontainer = "mycontainernamehere"

# CHANGE: Directory, where you can write local files.

# Depending on which environment you are running this,
# you need to change the directory where you can write local files.

# CASE 1. Running directly with python3 command
# local_model_file = "/home/[username]/"+model_file

# CASE 2. When running on container on your local machine
# The path points to dir inside your container image
# local_model_file = "/app/"+model_file

# CASE 3. When running on Azure Web App for Containers, 
# the runtime allows you ONLY to access directories under /home.
local_model_file = "/home/"+model_file

# ---------------------------------------------------
# END: YOU NEED TO CHANGE THESE 
# ---------------------------------------------------

#############################################
# FLASK STUFF
#############################################

app = Flask(__name__)

# Just that we have a start page for the web application
@app.route("/")

# It's a good convention to always define this empty route method, 
# just that you can test and see that your application is 
# actually running and responding when called with no parameters.

def hello():
    # https://www.tutorialspoint.com/flask/flask_templates.htm
    return render_template("hello.html"),200

# The actual API method
@app.route("/api/v1/fake")
def fakeApi():

    retdict ={} 

    try:
        print("FAKE API CALL")
        input_string = request.args.get("input","")
        print("input: "+input_string)
        print("my_fake_model: "+str(my_fake_model))

        index = int(input_string)
        predicted_value = my_fake_model[index]

        response = {
            'input':request.args.get("input",""),
            'predicted_value':str(predicted_value)
        } 
        
        retdict['response']=response

    except Exception as e:
        msg = "Bad Request (400): "+str(e)
        print(msg)
        return msg,400
    
    retJson = str(retdict).replace('\'','"')
    print("retjson :"+retJson)

    resp = make_response(retJson)
    resp.headers['content-type']="application/json"

    # http://www.flaskapi.org/api-guide/status-codes/#successful-2xx
    return resp, 200

#############################################
# Initialize the application
#############################################
# Azure blob handling samples can be found from:
# https://docs.microsoft.com/fi-fi/azure/storage/blobs/storage-quickstart-blobs-python
#############################################


# This loads files from azure blob storage to local
def load_files():

    print("--> load_files()")

    block_blob_service = BlockBlobService(account_name=storagename, account_key=storagekey) 
    block_blob_service.get_blob_to_path(storagecontainer, model_file, local_model_file)

    print("<-- load_files()")

# This Initializes my model once when app starts.
# The model is kept in global variable.
def initialize_model():

    print("--> initialize_model()")

    # we store the model in global variable, so others can 
    # use it after we exit from this function.
    
    global my_fake_model
    my_fake_model = np.load(local_model_file,mmap_mode=None,allow_pickle=True,fix_imports=True,encoding="ASCII")
    print("Testing, my pickled in fake model: "+str(my_fake_model))

    print("<-- initialize_model()")

#############################################
# MAIN
#############################################

if __name__=='__main__':

    print("--> main()")

    # Load files, and initialize the model
    load_files()
    initialize_model()

    # And then run the flask app
    app.run(debug=False,host='0.0.0.0',port=5000)

    print("<-- main()")

#############################################
# END OF FILE
#############################################
