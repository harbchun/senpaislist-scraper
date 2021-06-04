import boto3
import uuid

S3_BUCKET_NAME = "senapaislist-images"

def create_bucket(s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    
    bucket_response = s3_connection.create_bucket(
        Bucket=S3_BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': current_region
        }
    )

    return bucket_response

def random_file_prefix(file_name):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    
    return random_file_name


def get_current_season():
    return ''