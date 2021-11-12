import os
import secrets
from django.utils.deconstruct import deconstructible

@deconstructible
class rename:
    def __init__(self,path):
        self.path = path
    
    def __call__(self,instance,filename):
        ext = filename.split('.')[-1]
        hashed = secrets.token_hex(8)
        filename = "%s_%s.%s" % (instance.user.id, hashed, ext)
        return os.path.join(self.path, filename)