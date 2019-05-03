import os
from .utils.ml import MLProcess
from flask import Flask, current_app, send_file, jsonify, request

from .api import api_bp
from .client import client_bp
import pandas as pd


app = Flask(__name__, static_folder='../dist/static')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024
app.register_blueprint(api_bp)
# app.register_blueprint(client_bp)

from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

@app.route('/')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@app.route('/api/uploadfile', methods=["POST"])
def fileupload():
  try:
    file = request.files['file']
    _HERE = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(_HERE, "logs")
    if not os.path.exists(path):
      os.makedirs(path)
    # save(f, os.path.join(path, f.filename))
    MLProcess(file)
    data = pd.read_csv(os.path.join(path, 'dataset.csv'))
    return jsonify({"data": data.to_json(orient='records')})
  except:
    pass
  return jsonify({"done": False})
