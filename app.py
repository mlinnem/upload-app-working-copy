from flask import Flask, render_template, request
import ibm_boto3
from ibm_botocore.client import Config
import os

app = Flask(__name__)

# IBM Cloud Object Storage credentials and configurations
COS_ENDPOINT = 'https://s3.us-south.cloud-object-storage.appdomain.cloud'  # Adjust based on your region
COS_API_KEY_ID = 'KN3Xj0AxrrMUGYa2M9TEMqo7SAJEBn_ETZyLO8nKWgzn'
COS_INSTANCE_CRN = 'crn:v1:bluemix:public:cloud-object-storage:global:a/0bb4d59c58f057ca240dd82f9bf0ca02:01f8f5ba-bf99-41a6-9514-bf20e75a4c9f::'
COS_BUCKET_NAME = 'upload-app-bucket-9000'

# Create a COS client
cos = ibm_boto3.client("s3",
                       ibm_api_key_id=COS_API_KEY_ID,
                       ibm_service_instance_id=COS_INSTANCE_CRN,
                       config=Config(signature_version="oauth"),
                       endpoint_url=COS_ENDPOINT)

@app.route('/')
def index():
    # Render the HTML upload form
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request contains the file part
    if 'file' not in request.files:
        return "No file part in the request"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected"
    
    if file:
        try:
            # Read the file content
            file_content = file.read()
            
            # Upload the file content to IBM Cloud Object Storage using put_object
            cos.put_object(Bucket=COS_BUCKET_NAME, Key=file.filename, Body=file_content)
            
            return f"File {file.filename} uploaded successfully to IBM Cloud Object Storage!"
        except Exception as e:
            return f"Error uploading file: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
