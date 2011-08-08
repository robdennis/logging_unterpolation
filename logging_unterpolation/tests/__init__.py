import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

if sys.version_info >= (3,):
    # Python 3.x case (io does exist in 2.7, but better to use the 2.x case):
    #http://bugs.python.org/issue8025
    from io import StringIO
else:
    # Python 2.x case
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


class BaseLoggerTestCase(unittest.TestCase):
    """
    base class for testing the patching of the logging module to support
    PEP-3101 formatting strings. This class does no patching of the logging
    method
    """
    maxDiff = None
    def setUp(self):
        """
        Setup a string buffer to capture log output, subclasses overriding this
        setUp should import and patch logging in the appropriate manner
        to guarantee the existence of the self.logger property
        """

        self.buffer = StringIO()


    def assertLogOutput(self, expected, msg, *args):
        """
        :param expected: the expected log output
        :param msg: the (preformatted) message to pass to the logging statement
        :param args: the arguments to pass the logging statement
        """

        self.make_buffered_logger().info(msg, *args)
        self.buffer.flush()
        # log messages always end in a carriage return, so account for that
        self.assertEqual(self.buffer.getvalue(), expected + '\n')

    def make_buffered_logger(self, buffer=None, name='test_log'):
        """
        return a new logger instance, with the buffer set to buffer
        :param buffer: a StringIO instance, if None (default), will use
            self.buffer
        :param name: the name of the log (default 'test_log')
        :return: logger instance with the handler set to stream to buffer
        """
        # if this has already been patched, this additional import won't do
        # anything, which is fine
        import logging

        if buffer is None:
            buffer = self.buffer

        log_format = logging.Formatter('%(message)s')
        log_handler = logging.StreamHandler(self.buffer)
        _log = logging.getLogger(name)
        log_handler.setFormatter(log_format)
        _log.addHandler(log_handler)
        _log.setLevel(logging.DEBUG)

        return _log

    def test_basic_message(self):
        """
        test that a message with no formatting works as expected
        """
        expected = msg = 'hello world!'
        self.assertEqual(expected, msg)
        self.assertLogOutput(expected, msg)

    def test_modulo_syntax(self):
        """
        test that a message with a format using %-syntax works as exoected
        """

        expected = 'hello world!'
        msg = '%s %s!'
        args = ('hello', 'world')

        self.assertEqual(expected, msg % args)
        self.assertLogOutput(expected, msg, *args)

    def test_pep3101_syntax(self):
        """
        test that using str.format syntax fails as expected when unpatched
        """

        expected = 'hello world!'
        msg = '{0} {1}!'
        args = ('hello', 'world')

        self.assertEqual(expected, msg.format(*args))
        # since the message SHOULD be equal, as shown in the previous assertion
        # if this assertion fails, then formatting the message didn't work
        # (which is expected in this case)
        with self.assertRaises(AssertionError):
            self.assertLogOutput(expected, msg, *args)


class PatchedTestsMixin(object):
    """
    A mix-in class for tests that should be overridden, and additionally run
    when the logging module is patched
    """

    def test_pep3101_syntax(self):
        """
        override the base to show that it does work as expected
        """

        expected = 'hello world!'
        msg = '{0} {1}!'
        args = ('hello', 'world')

        self.assertEqual(expected, msg.format(*args))
        self.assertLogOutput(expected, msg, *args)