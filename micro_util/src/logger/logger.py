import os
import logging.config


log_config_path = "config/log_config.py"
log_config = os.path.exists(log_config_path)
if log_config:
    # For change log configuration create config/log_config.py and add LOGGING={}.
    from config.log_config import LOGGING
else:
    print("Loading default log config.")
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'key_value': {
                'format': 'timestamp:%(asctime)s pid:%(process)d thread:%(threadName)s loglevel:%(levelname)s module:%(module)s file:%(filename)s line:%(lineno)d - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'key_value',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'gunicorn.error': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'app': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            }
        },
    }

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("app")
print("initialized", logger)
