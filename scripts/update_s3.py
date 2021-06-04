import requests 
import json
import time
import os
import pandas # csv
import boto3 # AWS

from lib import times, s3utils, scrape

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
MIN_YEAR = int(os.environ.get('MIN_YEAR'))
MAX_YEAR = times.get_current_year()
THE_FORBIDDEN_GENRE_1=os.environ.get('THE_FORBIDDEN_GENRE_1')
THE_FORBIDDEN_GENRE_2=os.environ.get('THE_FORBIDDEN_GENRE_2')


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
    for year in range(MIN_YEAR, MAX_YEAR):
        for season in SEASONS:
            s3_data_objects = s3_client.list_objects(
                Bucket=AWS_DATA_BUCKET_NAME,
                Delimiter='/',
                MaxKeys=1,
                Prefix=str(year)+'/'+season+'/'
            )
            s3_data_contents = s3_data_objects.get('Contents', [])

            if not s3_data_contents:
                print('Data Bucket Is Empty')
                anime_ids = scrape.retrieve_anime_ids(year, season)
                
                for anime_id in anime_ids:
                    anime_data = scrape.retrieve_anime_data(anime_id)

                    # Filter out the forbidden genres
                    genres_dict_list = anime_data.get("genres", [])
                    genres = [x.get("name", '') for x in genres_dict_list]
                    if THE_FORBIDDEN_GENRE_1 in genres or THE_FORBIDDEN_GENRE_2 in genres:
                        continue
                    
                    return

            else:
                print('Data Bucket Is NOT Empty')


if __name__ == "__main__":
    main()