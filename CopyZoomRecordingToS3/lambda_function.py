import json
import os
import io
import uuid
import boto3
from lib import s3
from lib import sns
from lib import ffmpeg
from lib import dynamodb
from subprocess import call
from datetime import datetime

region_name = os.environ['DYNAMO_DB_REGION']
concurrency_count = int(os.environ['CONCURRENCY_COUNT'])
s3_input_bucket_path = os.environ['S3_INPUT_BUCKET_NAME']
s3_output_bucket_path = os.environ['S3_OUTPUT_BUCKET_NAME']
recordings_table_name = os.environ['DYNAMO_DB_RECORDINGS_TABLE']
recordings_jobs_count_table_name = os.environ['DYNAMO_DB_RECORDINGS_JOBS_COUNT_TABLE']
sns_zoom_symbl_queue = os.environ['SNS_SYMBL_ZOOM_QUEUE']
zoom_jwt_token = os.environ['ZOOM_JWT_TOKEN']
    
def lambda_handler(eventBody, context):
    
    print(eventBody)
    processEvent(eventBody)
                
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from copyZoomRecordingToS3 Lambda!')
    }

def get_by_meeting_uuid(meeting_uuid):
    dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
    item = dynamodb_instance.query_by_meeting_uuid(meeting_uuid, recordings_table_name)
    return item

def processEvent(jsonData):
    
    payload_obj = jsonData["payload"]["object"]
    
    meeting_topic = ''
    unique_id = payload_obj["uuid"].replace("==","").replace("/","").replace("\\","").replace("+","").replace("-","")
        
    can_save = False
    recordings_count = 0
    participants = []
    
    ZoomDynamoDB = dynamodb.ZoomDynamoDB(region_name)
    
    file_index = 1
    
    for item in payload_obj["participant_audio_files"]:
        recordings_count = recordings_count + 1
        file_name = str(item["file_name"]).split("-")[1][1:]
        file_type = item["file_type"]
        download_url = item["download_url"]
        participant_audio_file_id = item["id"]
        status = item["status"]
        meeting_topic = payload_obj["topic"]
        
        print("download_url:",download_url)
        print("file_name:",file_name)
        print("status:", status)
    
        if(status == "completed") :
            participants.append(file_name)
            print("Saving audio to S3")
            s3Helper = s3.S3Helper()
            s3_response = s3Helper.save(zoom_jwt_token, file_index, download_url, s3_input_bucket_path, unique_id)
            
            if s3_response != "":
                can_save = True
                file_index = file_index + 1
   
    if(can_save) :

        item = {
            'meeting_uuid': unique_id,
            'account_id': payload_obj["account_id"],
            'host_id': payload_obj["host_id"],
            'host_email': payload_obj["host_email"],
            'topic': payload_obj["topic"],
            'start_time': payload_obj["start_time"],
            's3_input_bucket_path': str(unique_id),
            's3_output_bucket_path': '',
            'participants': participants,
            'created_date': str(datetime.now()),
            'updated_date': ''
        }
        
        print(item)
        ZoomDynamoDB.save(recordings_table_name, item)
        
        try:
            if(recordings_count > 1):
                """ merge audio"""
                custom_ffmpeg = ffmpeg.FFMPEG()
                custom_ffmpeg.merge_and_upload_audio(s3_output_bucket_path, unique_id)
            else:
                s3_instance = boto3.client('s3')
                output_file = f'/tmp/{s3_response}'
                s3_instance.upload_file(output_file, s3_output_bucket_path, unique_id + '/output.m4a')
            
            item['s3_output_bucket_path'] = unique_id
            item['updated_date'] = str(datetime.now())
            
            ZoomDynamoDB.save(recordings_table_name, item)
            
            publish_message_to_queue(s3_output_bucket_path, unique_id)
        
        except BaseException as error:
            print("error: " + str(error))
        
    call('rm -rf /tmp/*', shell=True)
    return
    
def publish_message_to_queue(bucket, unique_id):
    
    message_to_publish = f'Initiate Recordings to Sybml with the Meeting UUID: {unique_id}'
    sns_instance = sns.SNS(region_name)
    sns_instance.publish_to_queue(sns_zoom_symbl_queue, message_to_publish, bucket, unique_id)
    print('Successfully published a message to queue')
 