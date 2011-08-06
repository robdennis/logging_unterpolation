logging_unterpolation
==============================

logging_unterpolation is a very simple module that will patch the built-in logging module to accept PEP-3101 compliant string formatting (using the str.format method) as well as falling back to accept the original string interpolation operator (% or 'modulo')

Here's a basic example:

    >>> import logging
    from logging_unterpolation import patch_logging
    patch_logging()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('test')
    DEBUG:root:test
    logging.debug('%s', 'test')
    DEBUG:root:test
    logging.debug('{0}', 'test')
    DEBUG:root:test