import boto3
import json
import logging

class SNS(object):
    
    def __init__(self, region_name):
        self.region_name = region_name
        
    def publish_message(self, arn, subject, message):
        client = boto3.client('sns', region_name=self.region_name)
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            Subject=subject,
            MessageStructure='json'
        )
        
    def publish_to_queue(self, queue_url, message_to_publish, bucket, unique_id):
        sqs = boto3.client('sqs')
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'UniqueId': {
                    'DataType': 'String',
                    'StringValue': unique_id
                },
                'Bucket': {
                    'DataType': 'String',
                    'StringValue': bucket
                }
            },
            MessageBody=(
                message_to_publish
            )
        )
        
        print(response['MessageId'])