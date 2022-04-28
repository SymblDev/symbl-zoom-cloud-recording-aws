import os
import json
import requests

class SybmlExperiece(object):
    
 def __init__(self, auth_token):
        self.auth_token = auth_token

 def get_text_summary_ui(self, conversation_id):
     
    url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/experiences"
    
    payload = json.dumps({
      "name": "verbose-text-summary"
    })
    
    headers = {
      'x-api-key': f'{self.auth_token}',
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {self.auth_token}'
    }
    
    print(url)
    print(headers)
    print(payload)
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

 def get_video_summary_ui(self, conversation_id, videoUrl):
     
    url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/experiences?validateUrl=false"
    
    payload = json.dumps({
      "name": "video-summary",
      "videoUrl": videoUrl,
      "summaryURLExpiresIn": 0
    })
    
    headers = {
      'x-api-key': f'{self.auth_token}',
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {self.auth_token}'
    }
    
    print(url)
    print(headers)
    print(payload)
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()