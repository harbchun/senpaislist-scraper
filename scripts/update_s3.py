import requests 
import json
import time
import os
import pickle
import urllib.request

import pandas # csv
import boto3 # AWS
from dotenv import load_dotenv

from lib import times, s3utils, scrape

load_dotenv()

# AWS variables
AWS_DATA_BUCKET_NAME = os.environ.get('AWS_DATA_BUCKET_NAME')
AWS_IMAGES_BUCKET_NAME = os.environ.get('AWS_IMAGES_BUCKET_NAME')
AWS_SECRET_KEY_ID = os.environ.get('AWS_SECRET_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_REGION = os.environ.get('AWS_BUCKET_REGION')

# const variables
SEASONS = ['spring', 'summer', 'fall', 'winter']
MIN_YEAR = int(os.environ.get('MIN_YEAR'))
MAX_YEAR = times.get_current_year()
THE_FORBIDDEN_GENRE_1=os.environ.get('THE_FORBIDDEN_GENRE_1')
THE_FORBIDDEN_GENRE_2=os.environ.get('THE_FORBIDDEN_GENRE_2')
DIR_JSON = os.getcwd()+'/files/json'
FILE_EXTENSION_JSON = '.json'
DIR_JPG = './files/jpg'
FILE_EXTENSION_JPG = '.jpg'

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

def main():
    for year in range(MIN_YEAR, MAX_YEAR):
        for season in SEASONS:
            # get the object 
            s3_data_objects = s3_client.list_objects(
                Bucket=AWS_DATA_BUCKET_NAME,
                Delimiter='/',
                MaxKeys=1,
                Prefix=str(year)+'/'+season+'/'
            )
            s3_data_contents = s3_data_objects.get('Contents', []) # files from the data bucket
            anime_ids = scrape.retrieve_anime_ids(year, season) # list of anime ids from this year & season from Jikan api
            
            if not s3_data_contents:
                print('Data Bucket Is Empty')
                
                for anime_id in anime_ids:
                    anime_data = scrape.retrieve_anime_data(anime_id) # Jikan api json reponse for this anime

                    # filter out the forbidden genres
                    genres_dict_list = anime_data.get("genres", [])
                    genres = [x.get("name", '') for x in genres_dict_list]
                    if THE_FORBIDDEN_GENRE_1 in genres or THE_FORBIDDEN_GENRE_2 in genres:
                        continue
                            
                    # FILE
                    random_file_name = s3utils.random_uuid()
                    anime_data['file_id'] = random_file_name

                    # !!! I HAVE DECIDED TO PUT THIS INTO A SEPRATE SCRIPT !!!
                    # IMAGE
                    # random_image_id = s3utils.random_uuid()
                    # anime_data['image_id'] = random_image_id # save the image id to the JPG file
                    # anime_image_url = anime_data['image_url']
                    # urllib.request.urlretrieve(anime_image_url, DIR_JPG+random_file_name+FILE_EXTENSION_JPG) # save locally
                    # s3_client.upload_file(DIR_JPG+random_file_name+FILE_EXTENSION_JPG, AWS_IMAGES_BUCKET_NAME, str(year)+'/'+season+'/'+random_file_name+FILE_EXTENSION_JPG)
                    # # remove the jpg file once it is done uploaded
                    # os.remove(DIR_JPG+random_file_name+FILE_EXTENSION_JPG)

                    # temporarily create the json file 
                    random_anime_id = s3utils.random_uuid()
                    anime_data['anime_id'] = random_anime_id
                    with open(DIR_JSON+random_file_name+FILE_EXTENSION_JSON, 'w') as s3_file:
                        json.dump(anime_data, s3_file)
                    s3_client.upload_file(DIR_JSON+random_file_name+FILE_EXTENSION_JSON, AWS_DATA_BUCKET_NAME, str(year)+'/'+season+'/'+random_file_name+FILE_EXTENSION_JSON)
                    # remove the json file once it is done uploaded
                    os.remove(DIR_JSON+random_file_name+FILE_EXTENSION_JSON)

            else:
                print('Data Bucket Is NOT Empty')


if __name__ == "__main__":
    main()