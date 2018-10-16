# PySampleModelCreator

**CREATE A SIMPLE MODEL AND STORE IT TO AZURE BLOB STORAGE**
*an example python app*

The related blog article can be found [here](https://jannehansen.com/).

*do once: pip3 install -r requirements.txt*

This small file emulates your actual machine learning model cretion.
My model is just a numpy array, the idea is of course that you
can replace my model with any real model you are working on. The
app content in short is:

1. Create your model.
2. Store the result to a local file
3. Copy the local file to Azure Blob Storage

In the next step (the PyFlaskApp), we use your stored model 
to publish a REST API for other applications to call.
