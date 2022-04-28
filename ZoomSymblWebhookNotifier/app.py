import json
import boto3

def lambda_handler(event, context):
    
    eventBodyString = event['body']
    print(eventBodyString)
    
    if(eventBodyString == None):
        return
    
    print('Invoking the zoomSymblWebhook lambda')
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='zoomSymblWebhook', 
                     InvocationType='Event',
                     Payload=eventBodyString)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from zoomSymblWebhookNotifier!')
    }
