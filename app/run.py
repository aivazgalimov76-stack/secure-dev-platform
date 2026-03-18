from flaskr import create_app

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    # Запускаем сервер
    app.run(debug=True, host='0.0.0.0', port=5000)
