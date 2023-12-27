import paramiko
import uuid
import hashlib
import hmac
from datetime import datetime

# DB configurate
DATABASE = 'databaseName'
USER = 'user'
PASSWORD = 'password'
HOST = 'host'
HOSTNAME = 'hostname'
PORT = '1234'

# ULR for DEV
URL = 'https://reqres.io'

secret_key = 'secret key'

# Header configurate for request
XUSER_ID = 'X-UserId'
XUSER_ID_VALUE = 'userId'

XORDERID = 'X-orderId'
XORDERID_VALUE = f'{uuid.uuid4()}'

XDATE = 'X-Date'
XDATE_VALUE = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

XORDER_REQUEST = 'X-OrderRequest'

message = f'{XDATE_VALUE}:{XORDERID_VALUE}'.encode('utf-8')
XORDER_REQUEST_VALUE = hmac.new(secret_key.encode('utf-8'), message, hashlib.sha256).hexdigest()

HEADERS_CONFIG = {XUSER_ID: XUSER_ID_VALUE, XORDERID: XORDERID_VALUE, XDATE: XDATE_VALUE, XORDER_REQUEST: XORDER_REQUEST_VALUE, "Content-Type": "application/json"}