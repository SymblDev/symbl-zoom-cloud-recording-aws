import json
import requests
import logging
        
class SymblInsights(object):
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.responses = {
            401: 'Unauthorized. Please generate a new access token.',
            404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
            500: 'Something went wrong! Please contact support@symbl.ai'
        }
        
    def get_summary(self, conversation_id):
        url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/summary"
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers)
        
        if(response.status_code == 200):
            # Successful API execution
            print("summary => " + str(response.json()['summary'])) 
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None

        return response.json()['summary']
        
    def get_follow_ups(self, conversationId):
        url = f"https://api.symbl.ai/v1/conversations/{conversationId}/follow-ups"
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code == 200:
            # Successful API execution
            print("followUps => " + str(response.json()['followUps']))  # followUps object containing followUp id, text, type, score, messageIds, entities, from, assignee, phrases
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None

        return response.json()['followUps']
        
    def get_action_items(self, conversationId):
        url = f"https://api.symbl.ai/v1/conversations/{conversationId}/action-items"
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code == 200:
            # Successful API execution
            print("actionItems => " + str(response.json()['actionItems']))  # actionsItems object containing actionItem id, text, type, score, messageIds, phrases, definitive, entities, assignee
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None

        return response.json()['actionItems']
        
    def get_questions(self, conversationId):
        url = f"https://api.symbl.ai/v1/conversations/{conversationId}/questions"
     
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("GET", url, headers=headers)
        
        if response.status_code == 200:
            # Successful API execution
            print("questions => " + str(response.json()['questions']))  # questions object containing question id, text, type, score, messageIds,entities
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None

        return response.json()['questions']
        
    def get_topics(self, conversationId):
        url = f"https://api.symbl.ai/v1/conversations/{conversationId}/topics"
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        params = {
            'sentiment': True,  # <Optional, boolean| Give you sentiment analysis on each topic in conversation.>
            'parentRefs': True,  # <Optional, boolean| Gives you topic hierarchy.>
        }
        
        response = requests.request("GET", url, headers=headers, params=json.dumps(params))
        
        if response.status_code == 200:
            # Successful API execution
            print("topics => " + str(response.json()['topics']))  # topics object containing topics id, text, type, score, messageIds, sentiment object, parentRefs
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None

        return response.json()['topics']
        
    def get_transcript(self, conversation_id):
        
        url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/transcript"
        
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'contentType': 'text/markdown',  # <Required | contentType of response>
            'createParagraphs': True,
            # <Optional, boolean| This boolean parameter specifies whether or not the transcription for the Conversation should be broken down into logical paragraphs.>
            'phrases': {"highlightOnlyInsightKeyPhrases": True, "highlightAllKeyPhrases": True},
            # <Optional, object| This is a json field which accepts two values highlightOnlyInsightKeyPhrases and highlightAllKeyPhrases. Both variables accepts boolean format.>
            'showSpeakerSeparation': True,
            # <Optional, boolean| When set to true, response will generate the transcript with each sentence separated by Speaker who spoke that sentence.>
        }
        
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        
        if(response.status_code == 200):
            # Successful API execution
            print("transcript => " + str(response.json()['transcript']))  # Containing markdown payload and contentType
        elif response.status_code in responses.keys():
            print(responses[response.status_code])  # Expected error occurred
            return None
        else:
            print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
            return None
            
        return response.json()['transcript']