from flaskr import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Режим отладки из переменной окружения
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Хост для привязки: по умолчанию 0.0.0.0 для Docker
    host = os.environ.get('FLASK_HOST', '0.0.0.0')# nosec - нужно для Docker

    # Порт (тоже можно сделать настраиваемым для гибкости)
    port = int(os.environ.get('FLASK_PORT', 5000))

    app.run(debug=debug_mode, host=host, port=port)
