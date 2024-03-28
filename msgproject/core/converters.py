class EndpointsConverter:
    regex = ".*?"
    
    def to_python(self, value):
        return value.split('/')
    
    def to_url(self, value):
        if isinstance(value, str):
            return value
        return '/'.join(value)