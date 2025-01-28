from flask import Flask
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicializar la aplicación Flask
app = Flask(__name__)

# Importar rutas (esto asegura que las rutas se registren al inicializar la app)
from app.router import *