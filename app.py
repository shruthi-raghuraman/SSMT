from flask import Flask, render_template
from flask_cors import CORS
import signal
from flask import Flask
from routes.api_calls import *
import sys
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(list_projects, url_prefix="/list_projects")
app.register_blueprint(namespace_cpu_request, url_prefix="/namespace_cpu_request")

def signal_term_handler(signal, frame):
    app.logger.warn('got SIGTERM')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    app.run(host=str(os.environ.get("HOST","localhost")), port=int(os.environ.get("PORT", 8000)))
