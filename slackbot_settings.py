import os
from boto.s3.connection import S3Connection
API_TOKEN = S3Connection(os.environ['API_TOKEN'])
DEFAULT_REPLY = "でふぉるとの返信"
PLUGINS = ['plugins']