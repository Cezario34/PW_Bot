import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ErrorLogFile(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR

formatter_1 = logging.Formatter(fmt='[%(asctime)s] - %(message)s')

error_file = logging.FileHandler('error.log', 'w', encoding='utf-8')
error_file.setLevel(logging.ERROR)
error_file.addFilter(ErrorLogFile())
error_file.setFormatter(formatter_1)

stdout = logging.StreamHandler()
stdout.setLevel(logging.INFO)
stdout.setFormatter(formatter_1)

logger.addHandler(stdout)
logger.addHandler(error_file)