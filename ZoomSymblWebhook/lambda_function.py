import json
import os
import io
import uuid
import boto3
from lib import s3
from lib import dynamodb
from lib import gmail
from lib import experience
from lib import symbl
from lib import symblInsights

region_name = os.environ['DYNAMO_DB_REGION']
recordings_insight_table = os.environ['DYNAMO_DB_RECORDINGS_INSIGHTS']
recordings_table = os.environ['DYNAMO_DB_RECORDINGS_TABLE']
recordings_jobs_table_name = os.environ['DYNAMO_DB_RECORDINGS_JOBS_TABLE']
recordings_jobs_count_table_name = os.environ['DYNAMO_DB_RECORDINGS_JOBS_COUNT_TABLE']
concurrency_count = int(os.environ['CONCURRENCY_COUNT'])
s3_bucket_output = os.environ['S3_OUTPUT_BUCKET_NAME']
gpass = os.environ['GPASS']
gmailId = os.environ['GMAILID']
app_id = os.environ['SYMBL_APP_ID']
app_secret = os.environ['SYMBL_APP_SECRET']
    
def lambda_handler(event, context):
    
    job_id = event['id']
    job_status = event['status']
    
    print('id: '+ job_id)
    print('job status: '+ job_status)
    
    symbl_instance = symbl.Symbl(app_id, app_secret)
    accessToken = symbl_instance.get_access_token()
    
    save_on_dynamo_db(job_id, job_status)
       
    if(job_status == "completed"):
        decrement_counter()
        item = fetch_and_send_email(accessToken, job_id)
        if(item != None):
            conversation_id = item['conversation_id']
            save_insights(accessToken, conversation_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from zoomSymblWebhook!')
    }
    
def save_insights(accessToken, conversation_id):
    
    dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
    
    symblInsight_instance = symblInsights.SymblInsights(accessToken)
    
    topics = symblInsight_instance.get_topics(conversation_id)
    questions = symblInsight_instance.get_questions(conversation_id)
    actionItems = symblInsight_instance.get_action_items(conversation_id)
    followUps = symblInsight_instance.get_follow_ups(conversation_id)
    summary = symblInsight_instance.get_summary(conversation_id)
    transcript = symblInsight_instance.get_transcript(conversation_id)
    
    item = {
        'conversation_id': str(conversation_id),
        'topics': str(topics),
        'questions': str(questions),
        'action_items': str(actionItems),
        'follow_ups': str(followUps),
        'summary': str(summary),
        'transcript': str(transcript)
    }
    
    print(item)
    
    dynamodb_instance.save(recordings_insight_table, item)
    print('Insights saved successfully!')

def decrement_counter():
    dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
    countItem = dynamodb_instance.query_by_Id(1, recordings_jobs_count_table_name)
    print(countItem)
    
    if(countItem != None):
        total_count = int(countItem['count'])
        if(total_count > 0):
            total_count = total_count - 1
            countItem['count'] = total_count
            save_response = dynamodb_instance.save(recordings_jobs_count_table_name, countItem)
            print('Total count: '+ str(total_count))
            print('save on decrement_counter')
            return save_response
    
def fetch_and_send_email(access_token, job_id):
    dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
    item = dynamodb_instance.query_by_jobId(job_id, recordings_jobs_table_name)
    
    if(item != None):
        conversation_id = item['conversation_id']
        uniqueId = item['meeting_uuid']
        
        s3_file_path = f'{uniqueId}/output.m4a'
        s3_instance = s3.S3Helper()
        s3_presigned_url = s3_instance.create_presigned_url(s3_bucket_output, s3_file_path)
             
        experience_url = get_experience_ui(access_token, conversation_id, s3_presigned_url)
        print(experience_url)
        
        dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
        recording_item = dynamodb_instance.query(uniqueId, recordings_table)
    
        if(recording_item != None):
            host_email = recording_item['host_email']
            topic = recording_item['topic']
            print(host_email)
            print(topic)
            
            if(gpass != ''):
                symblInsight_instance = symblInsights.SymblInsights(access_token)
                summary = symblInsight_instance.get_summary(conversation_id)
                send_email(experience_url, host_email, topic, summary)
            
    return item

def get_experience_ui(access_token, conversation_id, s3_presigned_url):
    
    experience_instance = experience.SybmlExperiece(access_token)
    response = experience_instance.get_video_summary_ui(conversation_id, s3_presigned_url)
    
    if(response != None):
        return response['url']
    
    return ""

def send_email(url, host_email, topic, summary):
    gmail_instance = gmail.Gmail()
    
    summary_text = ''
    for summary_item in summary:
        summary_text = summary_text + '<p>' + summary_item['text'] + '</p>'
    
    body = f'<h4>Here is the Summary of Conversation</h4><p>{summary_text}</p><h4>Meeting Insights</h4>{url}'
    gmail_instance.send_email(gmailId, gpass, host_email, topic, body)

def save_on_dynamo_db(job_id, job_status):
    
     # Get Dynamo DB info 
    dynamodb_instance = dynamodb.ZoomDynamoDB(region_name)
    item = dynamodb_instance.query_by_jobId(job_id, recordings_jobs_table_name)
    
    if(item != None):
        item['status'] = job_status
        dynamodb_instance.save(recordings_jobs_table_name, item)
    else:  
        item = {
            'job_id': job_id,
            'status': job_status
        }
        dynamodb_instance.save(recordings_jobs_table_name, item)