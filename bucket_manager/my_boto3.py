from boto3 import client,resource
from botocore.exceptions import ClientError
import os.path
import boto3


s3_client = client('s3')
s3_resource = resource('s3')


def fetch_all_buckets():
    try:
        return s3_client.list_buckets()
    except ClientError as err:
        return err


def fetch_bucket_details(bucket_name):
    try:
        response = s3_client.list_objects(Bucket=bucket_name)
        folders_list = set()
        if "Contents" in  response:
            for obj in response['Contents']:
                folders_list.add(obj['Key'].split('/',1)[0]+"/")
        bucket_name = response['Name']
        return folders_list, bucket_name 
    except ClientError as err:
        return err


def fetch_folder_details(bucket_name,folder_name):
    try:

        files_list = ['']
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix = folder_name)
        folder_list = [f["Key"]for f in response["Contents"]]
        for path in folder_list:
            files_list.append(os.path.basename(path))
        return response , files_list
    except ClientError as err:
        return err


def upload_file(file_name,bucket,key, args=None):
    try:
        return s3_client.upload_fileobj(file_name,bucket,key, ExtraArgs=args) 
    except  ClientError as err:
        return err


def delete_file(bucket,key):

    try:
        return s3_client.delete_object(Bucket=bucket, Key=key)
    except  ClientError as err:
        return err

def rename_file(bucket_name,folder_name,new_name,old_name):
    try:
        copy_source = {
            "Bucket": bucket_name,
            "Key" : old_name
        }
        otherkey = new_name
        print(old_name)
        s3_resource.meta.client.copy(copy_source,bucket_name,otherkey)
        response =  delete_file(bucket_name,old_name)
        return  response
    except ClientError as err:
        return err

# copy a file from on bucket to another

def copy_to_bucket(source_bucket,source_key,otherbucket,otherkey):
    try:
        copy_source = {
                "Bucket": source_bucket,
                "Key" : source_key
            }
        response = s3_resource.meta.client.copy(copy_source,otherbucket,otherkey)
        return response
    except ClientError as err:
        return err

# to create folder

def create_folder(bucket_name,dir_name):
        try:
           return s3_client.put_object(Bucket=bucket_name, Body='', Key=dir_name)
        except ClientError as err:
            return err

# to delete folder

def delete_folder(bucket_name, dir_name): 
      try:
          return s3_resource.Bucket(bucket_name).objects.filter(Prefix=dir_name).delete()
      except ClientError as err:
            return err

def register(access_id , access_key):
    try:
        client = boto3.client(
            's3',
            aws_access_key_id = access_id,
            aws_secret_access_key=  access_key
        )
        status = client.list_buckets()
        if status['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return "You have enter wrong keys"
    except:
         return "You have enter wrong keys"