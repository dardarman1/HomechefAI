import logging
import google.cloud.logging
import os


client = google.cloud.logging.Client()
client.setup_logging(log_level=logging.DEBUG)

from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug = True)