from waitress import serve
import logging

from services.streaming import app

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

serve(app, host='0.0.0.0', port=8080)
