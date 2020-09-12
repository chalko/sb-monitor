# flask_web/app.py

from flask import Flask
import requests
import json
import requests_cache

requests_cache.install_cache()

app = Flask(__name__)

@app.route('/')
def hello_world():
    r=requests.get("http://192.168.100.1")
    return r.text
