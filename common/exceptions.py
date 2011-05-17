class AbstractClassMethodException(Exception):
    def __str__(self):
        return 'Abstract Class method must be implemented in subclass'
    
class LocationException(Exception):
    pass    