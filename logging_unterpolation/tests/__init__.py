# coding=utf-8
from __future__ import with_statement, unicode_literals
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
    # Python 2.x case, explicitly NOT using cStringIO due to unicode edge cases
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
        actual = self.buffer.getvalue()
        # log messages always end in a carriage return, so account for that
        expected += '\n'
        # reset the buffer for future tests
        self.buffer = StringIO()

        self.assertEqual(actual, expected, 'message not expected:'
                                           ' %r != %r' % (actual, expected))

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
        test that a message with a format using %-syntax works as expected
        """


        test_items = [
            ('hello world!', '%s %s!', ('hello', 'world')),
            ('hello world!', '%(word1)s %(word2)s!', dict(word1='hello',
                                                          word2='world')),
            ('Dramatis Personæ', '%s %s', ('Dramatis', 'Personæ'))
        ]
            
        for expected, msg, args in test_items:
            self.assertEqual(expected, msg % args)
            if isinstance(args, dict):
                args = (args,)
            self.assertLogOutput(expected, msg, *args)

        if sys.version_info < (3, 0):
            # special case test for issue #4
            expected, msg, args = ('Dramatis Personæ', b'%s %s', ('Dramatis', 'Personæ'))
            self.assertLogOutput(expected, msg, *args)

    def _pep3101_test(self):
        """
        convenience function for testing pep3101 syntax and allowing test cases
        to assert based on the results
        """

        test_dict = dict(word1='hello', word2='world')
        test_items = [
            ('hello world!', '{0} {1}!', ('hello', 'world')),
            (repr(test_dict), '{0!r}', (test_dict,)),
            ('Dramatis Personæ', '{0} {1}', ('Dramatis', 'Personæ'))
        ]
        
        for expected, msg, args in test_items:
            self.assertEqual(expected, msg.format(*args))
            self.assertLogOutput(expected, msg, *args)

        if sys.version_info < (3, 0):
            # special case test for issue #4
            expected, msg, args = ('Dramatis Personæ', b'{0} {1}', ('Dramatis', 'Personæ'))
            with self.assertRaises(UnicodeEncodeError):
                self.assertEqual(expected, msg.format(*args))
            self.assertLogOutput(expected, msg, *args)

    # there's a separate test for patching on python versions that don't include format
    @unittest.skipIf(sys.version_info < (2,6), 'skipping pep 3101 syntax on old python')
    def test_pep3101_syntax(self):
        """
        test that using str.format syntax fails as expected when unpatched
        """

        with self.assertRaises(AssertionError):
            self._pep3101_test()

class PatchedTestsMixin(object):
    """
    A mix-in class for tests that should be overridden, and additionally run
    when the logging module is patched
    """

    # there's a separate test for patching on python versions that don't include format
    @unittest.skipIf(sys.version_info < (2,6), 'skipping pep 3101 syntax on old python')
    def test_pep3101_syntax(self):
        """
        override the base to show that it does work as expected
        """

        self._pep3101_test()
