from flaskr import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Используем debug только в разработке, не в продакшене
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # Для продакшена используем только localhost
    host = '127.0.0.1' if not debug_mode else '0.0.0.0'
    
    app.run(debug=debug_mode, host=host, port=5000)
