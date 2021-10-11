from typing import NoReturn
import boto3
import uuid
import logging
import os.path

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


''' 
To create new bucket 
'''
def create_bucket_name(bucket_prefix):
    #to get generate unique bucketname
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, region = None):
    session = boto3.session.Session()
    #if user won't provide region use the curent location
    try:

        if region is None:
            current_region = session.region_name
            bucket_name = create_bucket_name(bucket_prefix)
            bucket_response = s3_client.create_bucket(
                                                Bucket=bucket_name,
                                                CreateBucketConfiguration={
                                                'LocationConstraint': current_region})
        else:
            bucket_name = create_bucket_name(bucket_prefix)
            bucket_response = s3_client.create_bucket(
                                                Bucket=bucket_name,
                                                CreateBucketConfiguration={
                                                'LocationConstraint': region
                                                })
        return bucket_name, bucket_response
    except ClientError as err:
        logging.error(err)
        return err

# to call create fucntion
# created_bucket_name , created_response = create_bucket(bucket_prefix='third')

'''
to fetch all buckets available
'''

def fetch_all_buckets():
    try:
        return s3_client.list_buckets()
    except ClientError as err:
        return err

# an = fetch_all_buckets()
# for i in an["Buckets"]:
#     print(i['Name'])
# list = [ x['Name'] for x in an['Buckets']]
# print(list)
'''
to fetch contents from bucket
'''
def fetch_bucket_details(bucket_name):
    try:
        return s3_resource.Bucket(bucket_name)
    except:
        return "err happened while fetching data"

"""bucket_con = fetch_bucket_details('seconda774d653-df35-4e60-891c-7f5c68697e3f')
     
for obj in bucket_con.objects.all():
    key = obj.key
    body = obj.get() 
    if key == 'musics/':
        print("hello")
        print(body)         

"""

# --------------------------
# fetching only dirs
def fetch_bucket_dir(bucket_name):
        response = s3_client.list_objects(Bucket=bucket_name)
        if "Contents" not in  response:
            print("nothing")
        print(response)
        s_list = set()
        for obj in response['Contents']:
            s_list.add(obj['Key'].split('/',1)[0]+"/")
        print(response["Name"])
# bucket_con = fetch_bucket_dir('firstbucketf874d40f-0334-4e25-8b48-d894ffaa6610')

# ----------------------------


'''
to create directory
need to add bucket
'''
def create_directory(dir_name = None):
    
    if dir_name != None:
        try:
           return s3_client.put_object(Bucket='seconda774d653-df35-4e60-891c-7f5c68697e3f', Body='', Key=dir_name)
        except:
            return "err happed while creating dir"
    else:

        return "you have not given any name"

#print(create_directory('docs/'))

'''
to delete folder
'''

def delete_directory(dir_name=None):
    if dir_name != None:
      folder_bucket = s3_resource.Bucket('seconda774d653-df35-4e60-891c-7f5c68697e3f')
      try:
          return folder_bucket.objects.filter(Prefix=dir_name).delete()
      except:
          return "client err"
    else:
        return "you are not menstioned any name"
  
#print(delete_directory('musics/'))
#

'''
to upload file
'''
def upload_file(file_name,bucket,key, args=None):
        return s3_resource.meta.client.upload_file(file_name,bucket,key, ExtraArgs  = args) 
    
    
# print(upload_file('/home/sigmoid/Pictures/aws.png','seconda774d653-df35-4e60-891c-7f5c68697e3f',key = "img/" ,args={'ACL':'public-read'}))
#need to mension the folder also in key to save to parictlar folder 

'''--------------------------------------------------------------
to delete file from folder
'''
def delete_file(bucket,key):

    return s3_client.delete_object(Bucket=bucket,Key=key)

# print(delete_file("seconda774d653-df35-4e60-891c-7f5c68697e3f","img/Screenshot from 2021-09-28 06-51-11.png"))

'''
to rename file 

'''
def rename_file(bucket_name,folder_name,new_name,old_name):
    copy_source = {
            "Bucket": bucket_name,
            "Key" : old_name
        }
    otherkey = folder_name + new_name
    s3_resource.meta.client.copy(copy_source,bucket_name,otherkey)
    delete_file(bucket_name,old_name)

    return  
  
# print(rename_file(bucket_name='seconda774d653-df35-4e60-891c-7f5c68697e3f',folder_name="img/",new_name="pleaserename.png",old_name="img/newaws.png"))






#--------------------------------------------------------------------------------

"""
to copy from one s3 to another
"""

def copy_to_bucket_(source_bucket,source_key,otherbucket,otherkey):
    
    copy_source = {
            "Bucket": source_bucket,
            "Key" : source_key
        }
    response = s3_resource.meta.client.copy(copy_source,otherbucket,otherkey)
    return response

#print(copy_to_bucket_(source_bucket='seconda774d653-df35-4e60-891c-7f5c68697e3f',source_key='img/Screenshot from 2021-10-09 16-56-23.png',
 #S                                  otherbucket='thirdd299c5fb-9433-4eeb-b6e7-8d80b0ad913a',otherkey='imges/Screenshot from 2021-10-09 16-56-23.png'))
"""
fetching files name
"""
def fetch_folder_details(bucket_name,dir_name):
    bucket = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix =dir_name,
            MaxKeys=100 )
    folders_list = [f["Key"]for f in bucket["Contents"]]
    for p in folders_list:
      print(os.path.basename(p))
    print(folders_list)
# fetch_folder_details(bucket_name='seconda774d653-df35-4e60-891c-7f5c68697e3f',dir_name='img/')

# print(type(ans["Name"]))
# for con in ans["Contents"]:
#     print(con["Key"])

# def fetch_bucket_d(bucket_name):
#     return s3_client.list_parts(bucket_name)
   
# print(fetch_bucket_d("seconda774d653-df35-4e60-891c-7f5c68697e3f"))



# --------------
# for fetching file in dir

def fetch_folder_details(bucket_name,prefix):
        response = s3_client.list_objects_v2(Bucket=bucket_name,Prefix = prefix)
        return response

# print(fetch_folder_details("seconda774d653-df35-4e60-891c-7f5c68697e3f","img/"))
    
def register():
    try:
        client = boto3.client(
            's3',
            aws_access_key_id = 'AKIAZNRXXDUUDOHYIIMW',
            aws_secret_access_key=  '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'
        )
        status = client.list_buckets()
        if status['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Yes")
        else:
            print("no")
    except:
        print("You have enter wrong keys")

print(register())
