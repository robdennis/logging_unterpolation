import logging
from logging_unterpolation import patch_logging

patch_logging()

logging.basicConfig(level=logging.DEBUG)


logging.debug('test')
logging.debug('%s', 'test')
logging.debug('{0}', 'test')