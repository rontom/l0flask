# import itsdangerous for sending data to untrusted environments
from itsdangerous import TimestampSigner, URLSafeSerializer, SignatureExpired, BadSignature
from config import SECRET_KEY

class crypto:
    def __init__(self):
        self.secret_key = SECRET_KEY
    
    # encrypt
    def encrypt(self, payload, timestamp=False):
        result = ''
        s1 = URLSafeSerializer(self.secret_key)
        result = s1.dumps(payload)
        if(timestamp == True):
            s2 = TimestampSigner(self.secret_key)
            result = s2.sign(result)
        return result
    
    # decrypt
    def decrypt(self, payload, timestamp=False):
        result = None
        ts_error = None
        if(payload == None):
            ts_error = 'data is not valid.'
        else:
            if(timestamp == True):
                s1 = TimestampSigner(self.secret_key)
                try:
                    # 3600 seconds in an hour
                    result = s1.unsign(payload, max_age=3600)
                except SignatureExpired:
                    ts_error = 'timestamp has expired.'
                except BadSignature:
                    ts_error = 'data is not valid.'
        if(ts_error == None):
            try:
                s2 = URLSafeSerializer(self.secret_key)
                result = s2.loads(result)
            except BadSignature:
                result = 'data is not valid.'
        else:
            result = ts_error
        return result