import boto3
import logging
import requests
from botocore.exceptions import ClientError

class S3Helper(object):

        
    """ https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html """
    def create_presigned_url(self, bucket_name, object_name, expiration=604800):
        s3_client = boto3.client('s3')
        
        try:
            Params = {
                'Bucket': bucket_name,
                'Key': object_name
            }
            response = s3_client.generate_presigned_url('get_object',
                Params=Params,
                ExpiresIn=expiration,
                HttpMethod="GET")
        except ClientError as e:
            print('error: '+ e)
            logging.error(e)
            return None
    
        # The response contains the presigned URL
        return response