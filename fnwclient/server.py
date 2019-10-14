from endpoint import app
from waitress import serve
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

serve(app, host='0.0.0.0', port=80)
