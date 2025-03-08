from flask import Flask, send_from_directory
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#app = Flask(__name__)
app = Flask(__name__, static_folder='../frontend', static_url_path='/')

from app.router import *

