import logging
import argparse  # Добавлено!
from flaskr import create_app
import os
import sys

# Отключаем логи запросов Werkzeug
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    args = parser.parse_args()
    
    port = args.port
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # nosec
    
    print(f"🚀 Starting Flask on {host}:{port} (debug={debug_mode})")
    app.run(debug=debug_mode, host=host, port=port)
