import logging
import boto3
from botocore.exceptions import ClientError

def upload_fileobj(file_obj, file_name):
    """
    Upload a file to an S3 bucket
    
    :param file_obj: File object to upload
    :param file_name: S3 object name that will be saved
    :return: True if file was uploaded, else False
    """
    # load bucket name 
    from manage import app
    bucket_name = app.config['BUCKET_NAME']
    
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(file_obj, bucket_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_file(object_name):
    """
    Delete a image file in S3 by image_uuid

    :Param object_name: String
    :Return: True if successed, else False
    """
    # load bucket name 
    from manage import app
    bucket_name = app.config['BUCKET_NAME']

    # Delete the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_object(object_name):
    """
    Get object in an S3 bucket

    :param object_name: S3 object name.
    :return: file data if successed, else None
    """
    # load bucket name
    from manage import app
    bucket_name = app.config['BUCKET_NAME']

    # get object in the bucket
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=object_name
        )
        file_data = response['Body'].read()
    except ClientError as e:
        logging.error(e)
        return None
    return file_data


# def download_file(object_name, file_name=None):
#     """
#     Download a file in an S3 bucket

#     :param object_name: S3 object name.
#     :param file_name: File name to download. If not specified then object_name is used
#     :return: True if file was downloaded, else False
#     """
#     from manage import app
#     # load bucket name 
#     bucket_name = app.config['BUCKET_NAME']

#     # If S3 file_name was not specified, use object_name
#     if file_name is None:
#         file_name = object_name

#     # Download the file
#     s3_client = boto3.client('s3')
#     try:
#         s3.download_file(bucket_name, object_name, file_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True

# def upload_file(file_name, bucket, object_name=None):
#     """
#     Upload a file to an S3 bucket
    
#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = file_name
    
#     # Upload the file
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True