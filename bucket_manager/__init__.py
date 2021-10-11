from flask import Flask
from bucket_manager.filter import datetimeformat, file_size, file_type

app = Flask(__name__)
app.secret_key = 'secret'

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['file_size'] = file_size


from bucket_manager import routes