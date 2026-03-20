import logging
import logstash
from pythonjsonlogger import jsonlogger
from flask import request, has_request_context

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        if not log_record.get('timestamp'):
            log_record['timestamp'] = record.created
        
        log_record['logger'] = record.name
        log_record['level'] = record.levelname
        
        if has_request_context():
            log_record['ip'] = request.remote_addr
            log_record['method'] = request.method
            log_record['path'] = request.path
            log_record['url'] = request.url
            log_record['user_agent'] = request.user_agent.string
            
            from flask_login import current_user
            if current_user and current_user.is_authenticated:
                log_record['user_id'] = current_user.id
                log_record['username'] = current_user.username

def setup_logging(app):
    # Настраиваем форматтер
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(logger)s %(message)s'
    )
    
    # 1. Консольный вывод (для разработки)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    
    # 2. Logstash handler (отправляет логи в Logstash)
    try:
        logstash_handler = logstash.LogstashHandler(
            host='logstash',
            port=5002,
            version=1
        )
        logstash_handler.setLevel(logging.INFO)
        app.logger.addHandler(logstash_handler)
        app.logger.info("Logstash handler configured", extra={'event': 'logstash_ready'})
        print("✅ Logstash handler configured successfully")
    except Exception as e:
        app.logger.error(f"Failed to setup logstash: {e}")
        print(f"❌ Failed to setup logstash: {e}")
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application started', extra={
        'event': 'app_start',
        'host': app.config.get('HOST', 'unknown'),
        'port': app.config.get('PORT', 5000)
    })
    
    return app.logger
