"""
------------------------------------------------------------------
Create model example python app
------------------------------------------------------------------
do once: pip3 install -r requirements.txt

This small file emulates your actual machine learning model cretion.
My model is just a numpy array, the idea is of course that you
can replace my model with any real model you are working on. The
app content in short is:

1. Create your model.
2. Store the result to a local file
3. Copy the local file to Azure Blob Storage

In the next step (the PyFlaskApp), we use your stored model 
to publish a REST API for other applications to call.
------------------------------------------------------------------
Licence: MIT, Janne Hansen 2018
"""

# imports
from azure.storage.blob import BlockBlobService, PublicAccess
import numpy as np

# Globals
block_blob_service = None

# filenames to use, local file and the copied file to azure
full_path_to_local_file = 'my_local_model.npy'
azure_storage_filename = 'my_model_on_azure.npy'


# ---------------------------------------------------
# BEGIN: YOU NEED TO CHANGE THESE 
# ---------------------------------------------------


# Azure Blob storage name and access key. Container name where my blobs are stored.
# You can get these from Azure portal (portal.azure.com)
# Storage Account / Access Keys - tab in your Azure subscription.

storagename = "mystorageaccountname"
storagekey = "mystorageaccountkey"
storagecontainer = "mycontainername"

# ---------------------------------------------------
# END: YOU NEED TO CHANGE THESE 
# ---------------------------------------------------

#############################################
# SAMPLE METHODS
# ###########################################
# Azure blob handling samples can be found from:
# https://docs.microsoft.com/fi-fi/azure/storage/blobs/storage-quickstart-blobs-python
#############################################

# Intializes only once the connection to Azure Blob Storage
# Stores the "connection" to global blocl_blob_service variable
def sample_init():

    print("--> sample_init()")

    global block_blob_service
    block_blob_service = BlockBlobService(account_name=storagename, account_key=storagekey) 

    # List the blobs in the container just for fun.
    # This is not needed, just for demo purposes...
    print("\nList all blobs in the container")
    generator = block_blob_service.list_blobs(storagecontainer)
    for blob in generator:
        print(blob.name)

    print("<-- sample_init()")

# This uploads the fake model we created to Azure Storage Blob
def upload_model_to_blob():

    print("--> upload_model_to_blob()")

    block_blob_service.create_blob_from_path(storagecontainer, azure_storage_filename, full_path_to_local_file)
    print("Uploaded my local model file to Azure with filename: "+azure_storage_filename)

    print("<-- upload_model_to_blob()")

# This creates my fake model, and stores it as pickle to local file
# Of course you'd replace with your actual model creating code.
def model_creation():

    print("--> model_creation()")

    # create a numpy array to be pickled. This is my fake model
    my_model = np.array([1,2,4,8,16,32,64,128,256])

    print("About to store my model to local file: "+str(my_model))
    np.save(full_path_to_local_file, my_model, allow_pickle=True, fix_imports=True)

    # Just to test that what I stored, can be retrieved also.
    my_loaded_model = np.load(full_path_to_local_file,mmap_mode=None,allow_pickle=True,fix_imports=True,encoding="ASCII")
    print("Testing, my model loaded from local file: "+str(my_loaded_model))

    print("<-- model_creation()")

#############################################
# MAIN
#############################################

if __name__=='__main__':

    print("--> main()")

    # Our little test application contents
    sample_init()
    model_creation()
    upload_model_to_blob()

    print("<-- main()")

#############################################
# END OF FILE
#############################################