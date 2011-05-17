class StatusManager:
    def __init__(self, **kwargs):
        
        self.statusSites = kwargs
    
    def Announce(self, key, msg):
        if not self.statusSites.has_key(key):
            raise Exception('Key not in statusSites: %s' % key)
        self.HandleAnnouncement(key, msg)
    
    def HandleAnnouncement(self, key, msg):
        raise Exception('HandleAnnouncement must be implemented in StatusManager subclass')

class LabelStatusManager(StatusManager):
    def HandleAnnouncement(self, key, msg):
        self.statusSites[key].SetLabel(msg)

    
    