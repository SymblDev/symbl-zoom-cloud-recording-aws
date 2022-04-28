import json
import time
import os
import io
import uuid
import boto3
import requests
from lib import symbl
from lib import dynamodb
from lib import s3

app_id = os.environ['SYMBL_APP_ID']
app_secret = os.environ['SYMBL_APP_SECRET']
queue_url = os.environ['SNS_SYMBL_ZOOM_QUEUE']
webhook_url = os.environ['SYMBL_WEBHOOK_URL']
s3_bucket_output = os.environ['S3_OUTPUT_BUCKET_NAME']
region = os.environ['DYNAMO_DB_REGION']
recordings_table = os.environ['DYNAMO_DB_RECORDINGS_TABLE']
recordings_jobs_table = os.environ['DYNAMO_DB_RECORDINGS_JOBS_TABLE']
recordings_jobs_count_table_name = os.environ['DYNAMO_DB_RECORDINGS_JOBS_COUNT_TABLE']
concurrency_count = int(os.environ['CONCURRENCY_COUNT'])
sleep_time = int(os.environ['SLEEP_TIME'])
        
def lambda_handler(event, context):
    
    print('Inside of submitZoomRecordingToSymbl');
    
    sqs = boto3.client('sqs')
    
    symbl_instance = symbl.Symbl(app_id, app_secret)
    accessToken = symbl_instance.get_access_token()
    print('Access Token: '+ accessToken)
    
    print(event['Records'])
    
    for record in event['Records']:
        
        # Update the job count recordings
        if(check_concurrency_and_increment_counter() == False):
            time.sleep(sleep_time)
            continue
        
        message_body = record['body']
        receipt_handle = record['receiptHandle']
        print(receipt_handle)
    
        message_attributes = record['messageAttributes']
        uniqueId = message_attributes['UniqueId']['stringValue']
        print('Unique Id: '+ uniqueId)
        
        # Get Dynamo DB info 
        dynamodb_instance = dynamodb.ZoomDynamoDB(region)
        item = dynamodb_instance.query(uniqueId, recordings_table)
        
        print(item)
        
        audio_url = f's3://{s3_bucket_output}/{uniqueId}/output.m4a'
        s3_file_path = f'{uniqueId}/output.m4a'
        s3_instance = s3.S3Helper()
        
        print('S3 Bucket: '+ s3_bucket_output)
        print('S3 Path: '+ s3_file_path)
        
        s3_presigned_url = s3_instance.create_presigned_url(s3_bucket_output, s3_file_path)
        
        print(s3_presigned_url)
        
        response = symbl_instance.post_audio_url(accessToken, item, s3_presigned_url, webhook_url)
    
        if(response != None):
            jobId = response['jobId']
            conversationId = response['conversationId']
            
            # Update job recordings
            update_job_recordings_table(uniqueId, jobId, conversationId)
            
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print('Received and deleted message: %s' % str(message_body))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from submitZoomRecordingToSymbl Lambda!')
    }

def update_job_recordings_table(uniqueId, jobId, conversationId):
    
    dynamodb_instance = dynamodb.ZoomDynamoDB(region)
    item = dynamodb_instance.query_by_jobId(jobId, recordings_jobs_table)
    print(item)
    
    if(item != None):
        item['conversation_id'] = conversationId
        item['meeting_uuid'] = uniqueId
        dynamodb_instance.save(recordings_jobs_table, item)
    else:  
        item = {
            'meeting_uuid': uniqueId,
            'job_id': jobId,
            'conversation_id': conversationId,
            'status': ''
        }
        dynamodb_instance.save(recordings_jobs_table, item)
        
def check_concurrency_and_increment_counter():
    dynamodb_instance = dynamodb.ZoomDynamoDB(region)
    countItem = dynamodb_instance.query_by_Id(1, recordings_jobs_count_table_name)
    print(countItem)
    
    if(countItem != None):
        total_count = int(countItem['count'])
        
        if(total_count < concurrency_count):
            total_count = total_count + 1
            countItem['count'] = total_count
            save_response = dynamodb_instance.save(recordings_jobs_count_table_name, countItem)
            print('Total count: '+ str(total_count))
            print('save on increment_counter')
            return save_response
        else:
            print('exceeding the concurrency limit')
            return False
    else:
         dynamodb_instance.save(recordings_jobs_count_table_name, {'id': 1, 'count': 1})
         return True
         