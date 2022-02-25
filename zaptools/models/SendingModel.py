class SendingModel():

    zap_id :str
    zap_adapter: str
    event : str
    payload : any

    def __init__(self, zap_id:str, zap_adapter:str, event:str, payload:any) -> None:
        self.zap_id  = zap_id
        self.zap_adapter = zap_adapter
        self.event = event
        self.payload = payload
    
    def toJsonDict(self):
        return {
            "zapId" : self.zap_id,
            "zapAdapter" : self.zap_adapter,
            "event" : self.event,
            "payload" :self.payload
        }
        