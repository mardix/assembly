

@flasik.extends
def _setup_logger(cls):
    logging_config = app.config.get("LOGGING")
    if not logging_config:
        logging_config = {
            "version": 1,
            "handlers": {
                "default": {
                    "class": app.config.get("LOGGING_CLASS", "logging.StreamHandler")
                }
            },
            'loggers': {
                '': {
                    'handlers': ['default'],
                    'level': 'WARN',
                }
            }
        }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("root")
    app._logger = logger
