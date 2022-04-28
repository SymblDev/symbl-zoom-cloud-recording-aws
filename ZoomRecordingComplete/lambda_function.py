import json
import boto3

def lambda_handler(event, context):
    
    eventBody = event['body']
    eventBodyString = str(eventBody)
    print(eventBodyString)
    
    print('Invoking the copyZoomRecordingToS3 lambda')
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='copyZoomRecordingToS3', 
                     InvocationType='Event',
                     Payload=eventBodyString)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from ZoomRecordingComplete!')
    }
