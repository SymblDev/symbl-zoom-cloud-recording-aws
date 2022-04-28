import os
import boto3
import time
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

class ZoomDynamoDB(object):
    
    def __init__(self, region_name):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        logging.basicConfig()
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
    
    def query_by_Id(self, id, table_name):
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'id': id})
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            if 'Item' in response:
                return response['Item']
            else:
                return None
        
    def query_by_status_not_complete(self, table_name):
        try:
            table = self.dynamodb.Table(table_name)
            fe = Key('status').eq('') | Key('status').eq('scheduled') | Key('status').eq('in_progress') | Key('status').eq('failed')
            response = table.scan(
                FilterExpression=fe)
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            if 'Items' in response:
                return response['Items']
            else:
                return None
        
    def query_by_meetingId(self, meeting_id, table_name):
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'meeting_id': int(meeting_id)})
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            if 'Item' in response:
                return response['Item']
            else:
                return None
            
    def query_by_jobId(self, job_id, table_name):
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'job_id': job_id})
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
        else:
            if 'Item' in response:
                return response['Item']
            else:
                return None
                
    def query(self, meeting_id, table_name):
        table = self.dynamodb.Table(table_name)
        try:
            response = table.get_item(Key={'meeting_uuid': meeting_id})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']
        
    def save(self, table_name, item):
        try:
            table = self.dynamodb.Table(table_name)
            response = table.put_item(Item=item)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True
            else:
                return False
        except ClientError as error:
            print(error)
            return False
        except BaseException as error:
            print("Unknown error while putting item: " + error)
            return False