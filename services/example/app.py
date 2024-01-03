import time
from datetime import datetime

from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return f'Hello World! {datetime.now().isoformat()}\n'
