import boto3
import uuid
import logging
import shutil
import requests
from lib import ffmpeg
from botocore.exceptions import ClientError

class S3Helper(object):

    def read(self, bucket, s3_path):
        bucket_list = []
        for file in my_bucket.objects.filter(Prefix = s3_path):
            file_name=file.key
            bucket_list.append(file.key)
        return bucket_list
    
    def save(self, jwt_token, file_index, download_url, bucket, s3_path):
        s3 = boto3.client('s3')
        
        formatted_download_url = download_url + '?access_token='+ jwt_token
        print(formatted_download_url)
        response = requests.get(formatted_download_url)
        
        if response.status_code==200:
            
            try:
                unique_filename = str(file_index) + '.m4a'
                local_filename = self.download_file(formatted_download_url, unique_filename)
                
                print('Local filename: '+ local_filename)
                print('S3 Bucket: '+ bucket)
                
                # do ffmpeg probe
                custom_ffmpeg = ffmpeg.FFMPEG()
                custom_ffmpeg.probe_file(local_filename)
                
                # uploads the file to s3
                s3.upload_file(local_filename, bucket, s3_path + '/' + unique_filename)
                print(f'File uploaded')
                
            except ClientError as e:
                logging.error(e)
                print(f'File not uploaded')
                return ""
            except Exception as e:
                logging.error(e)
                print(f'File not uploaded')
                return ""
                
            return unique_filename
        else:
            print("Cannot parse url")
        
        return ""

    def download_file(self, url, unique_filename):
        local_filename = '/tmp/'+ unique_filename
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    
        return local_filename