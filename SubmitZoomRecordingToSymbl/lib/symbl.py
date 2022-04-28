import json
import requests
import logging
from lib import channelMetadata

class Payload(object):
    
    def __init__(self, url, name, webhookUrl, channelMetadata):
        self.url = url
        self.name = name
        self.webhookUrl = webhookUrl
        self.channelMetadata = channelMetadata
    
    def encode(self):
        return self.__dict__
        
class Symbl(object):
    
    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret
    
    def get_access_token(self):
        accessToken = ''
        
        payload = {
            "type": "application",
            "appId": self.appId,
            "appSecret": self.appSecret
        }
    
        headers = {
            'Content-Type': 'application/json'
        }
        
        responses = {
            400: 'Bad Request! Please refer docs for correct input fields.',
            401: 'Unauthorized. Please generate a new access token.',
            404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
            429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
            500: 'Something went wrong! Please contact support@symbl.ai'
        }
        
        url = "https://api.symbl.ai/oauth2/token:generate"
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            # Successful API execution
            accessToken = response.json()['accessToken']
            print("accessToken => " + accessToken)  # accessToken of the user
            print("expiresIn => " + str(response.json()['expiresIn']))  # Expiry time in accessToken
        elif response.status_code in responses.keys():
            print(responses[response.status_code], response.text)  # Expected error occurred
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

        return accessToken
        
    def build_channel_metadata(self, participants):
        channelMetadataCollection = []
        speaker_count = 0
        
        for participant in participants:
            speaker_count = speaker_count + 1
            email = ''.join(participant.split()) + '@email.com'
            speaker_instance = channelMetadata.Speaker(participant, email)
            channelMetadata_instance = channelMetadata.ChannelMetadata(speaker_count, speaker_instance)
            channelMetadataCollection.append(channelMetadata_instance)
            
        return channelMetadataCollection

        
    def post_audio_url(self, access_token, item, audio_url, webhook_url):
        url = "https://api.symbl.ai/v1/process/audio/url"
        
        channelMetadataCollection = self.build_channel_metadata(item['participants'])

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        
        enable_speaker_separation = True
        
        payload = {
            'url': audio_url,
            'name': item['topic'],
            'webhookUrl': webhook_url,
            'channelMetadata': channelMetadataCollection,
            'enableSeparateRecognitionPerChannel': enable_speaker_separation
        }
       
        responses = {
            400: 'Bad Request! Please refer docs for correct input fields.',
            401: 'Unauthorized. Please generate a new access token.',
            404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
            429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
            500: 'Something went wrong! Please contact support@symbl.ai'
        }
        
        data = json.dumps(payload, default=lambda o: o.encode())
        print(data)
        
        response = requests.request("POST", url, headers=headers, data=data)
        
        if response.status_code == 201:
            # Successful API execution
            conversationId = response.json()['conversationId']
            jobId = response.json()['jobId']
            print("conversationId => " + conversationId)  # ID to be used with Conversation API.
            print("jobId => " + jobId)  # ID to be used with Job API.
            return {
                "conversationId": conversationId,
                "jobId": jobId
            }
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None
