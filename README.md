[![Build Status](https://travis-ci.org/robdennis/logging_unterpolation.png?branch=master)](https://travis-ci.org/robdennis/logging_unterpolation)[![Coverage Status](https://coveralls.io/repos/robdennis/logging_unterpolation/badge.png)](https://coveralls.io/r/robdennis/logging_unterpolation)

logging_unterpolation
==========================
logging_unterpolation is a very simple module that will patch python's built-in logging module to accept PEP-3101 compliant string formatting (using the str.format method) as well as falling back to accept the original string interpolation operator (% or 'modulo')

Here's a basic example:

```python
>>> import logging
>>> from logging_unterpolation import patch_logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> logging.debug('test')
DEBUG:root:test
>>> logging.debug('%s', 'test') # example of built-in string interpolation in log messages
DEBUG:root:test
>>> patch_logging()
>>> logging.debug('{0}', 'test') # format syntax not supported unless patched
DEBUG:root:test
```

