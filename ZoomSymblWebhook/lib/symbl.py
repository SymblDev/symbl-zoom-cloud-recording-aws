import json
import requests
import logging
        
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