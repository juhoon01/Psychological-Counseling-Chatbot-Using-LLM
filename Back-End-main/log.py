import logging
import logging.config
import os

if not os.path.exists('logs'):
    os.makedirs('logs', exist_ok=True)

# 로깅 설정 파일 경로
logging_config_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_config_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
