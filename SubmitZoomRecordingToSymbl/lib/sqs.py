import boto3

class SQS(object):
    
    def get_messages(self, queue_url):
        sqs_client = boto3.client('sqs')
    
        messages = []
    
        while True:
            resp = sqs_client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10
            )
    
            try:
                messages.extend(resp['Messages'])
            except KeyError:
                break
            
        return messages