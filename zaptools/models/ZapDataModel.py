class ZapDataModel():

    zap_id :str
    zap_adapter: str
    event : str
    payload : any

    def __init__(self, zap_id:str, zap_adapter:str, event:str, payload:any) -> None:
        self.zap_id      = zap_id
        self.zap_adapter = zap_adapter
        self.event       = event
        self.payload     = payload
    
    @classmethod
    def fromJsonDict(cls ,jsonDict: dict):
        instance             = cls.__new__(cls)
        instance.zap_id      = jsonDict["zapId"]
        instance.zap_adapter = jsonDict["zapAdapter"]
        instance.event       = jsonDict["event"]
        instance.payload     = jsonDict["payload"]
        return instance


    def toJsonDict(self):
        return {
            "zapId"      : self.zap_id,
            "zapAdapter" : self.zap_adapter,
            "event"      : self.event,
            "payload"    :self.payload
        }
        