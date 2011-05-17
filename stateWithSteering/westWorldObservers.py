from Observers import Observer


class LabelObserver(Observer):
    def __init__(self, label):
        self.label = label

    def update(self, value=None):
        if not value:
            return
        
        self.label.SetLabel(str(value))


class LabelItemAttributeObserver(LabelObserver):
    
    def __init__(self, label, attribute):
        LabelObserver.__init__(self, label)
        self.attribute = attribute
    
    def update(self, value=None):
        if not value:
            return
        
        self.label.SetLabel(str(value.attributes[self.attribute]))
