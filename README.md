# PublishMLModel

This tiny python example shows a simple workflow on how to publish your machine learning models
for other applications to use with REST API. To run the samples you'll need an Azure subscription.

## Contents of this repo

[PySampleModelCreator](PySampleModelCreator/) creates a simple machine learning model (fake one this time),
and stores it to Azure Blob Storage for publishing.

[PyFlaskApp](PyFlaskApp/) is a flask application which reads the model from Blob Storage and
then sets up a flask server to respond to incoming http(s) REST api calls.

## Read more!

The related blog article can be found on:
https://jannehansen.com/publish-ml-model/ (English)



