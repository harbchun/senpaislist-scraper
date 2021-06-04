import requests 
import json
import time
import os
import pandas # csv
import boto3 # AWS
 
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# AWS variables
AWS_DATA_BUCKET_NAME = os.environ.get('AWS_DATA_BUCKET_NAME')
AWS_IMAGES_BUCKET_NAME = os.environ.get('AWS_IMAGES_BUCKET_NAME')
AWS_SECRET_KEY_ID = os.environ.get('AWS_SECRET_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_REGION = os.environ.get('AWS_BUCKET_REGION')

# const variables
SEASONS = ['spring', 'summer', 'fall', 'winter']
START_YEAR = 2010


# Creating the low level functional client
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_SECRET_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_BUCKET_REGION
)
# Creating the high level object oriented interface
s3_resource = boto3.resource(
    's3',
    aws_access_key_id = AWS_SECRET_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_BUCKET_REGION
)

# Create s3 bucket objects
s3_data_object = s3_client.list_objects(
    Bucket=AWS_DATA_BUCKET_NAME
)
s3_images_object = s3_client.list_objects(
    Bucket=AWS_IMAGES_BUCKET_NAME
)

# get the contents inside of the bucket
s3_data_contents = s3_data_object.get('Contents', [])
s3_images_contents = s3_images_object.get('Contents', [])

def main():
    if not s3_data_contents:
        print('Data Bucket Is Empty')
    else:
        print('Data Bucket Is NOT Empty')

if __name__ == "__main__":
    main()