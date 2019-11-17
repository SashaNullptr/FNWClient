from waitress import serve
import logging
import asyncio
import threading

from services.streaming.backend import app

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

# Local
from services.streaming.lib import StreamingAnalytics
from services.streaming.config import collect_env_vars

def start_analytics():
    asyncio.set_event_loop(asyncio.new_event_loop())
    creds = collect_env_vars("API_ID", "API_HASH", "SESSION")
    analytics_module = StreamingAnalytics(**creds)
    analytics_module.init_client()

def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    serve(app, host='0.0.0.0', port=8080)

analytics_thread = threading.Thread(target=start_analytics,  args=())
analytics_thread.daemon = True
analytics_thread.start()

server_thread = threading.Thread(target=start_server,  args=())
server_thread.daemon = True
server_thread.start()

analytics_thread.join()
server_thread.join()