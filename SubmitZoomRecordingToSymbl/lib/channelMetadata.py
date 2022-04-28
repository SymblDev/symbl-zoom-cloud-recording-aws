class ChannelMetadata: 
    def __init__(self, channel, speaker): 
        self.channel = channel 
        self.speaker = speaker
        
    def encode(self):
        return self.__dict__
        
class Speaker: 
    def __init__(self, name, email): 
        self.name = name 
        self.email = email
    
    def encode(self):
        return self.__dict__