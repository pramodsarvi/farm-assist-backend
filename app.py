from flask import Flask

UPLOAD_FOLDER = 'D:\\VSCODE\\project\\BACK\\'
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'