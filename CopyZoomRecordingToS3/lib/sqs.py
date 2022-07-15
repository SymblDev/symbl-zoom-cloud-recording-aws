import boto3
import json
import logging

class SQS(object):
    
    def __init__(self, region_name):
        self.region_name = region_name
    
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