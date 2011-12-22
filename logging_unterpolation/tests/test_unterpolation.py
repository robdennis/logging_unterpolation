import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from logging_unterpolation.tests import BaseLoggerTestCase, PatchedTestsMixin

# PatchedTestsMixin must go first to override the base methods

class TestPerformaceResults(unittest.TestCase):
    """
    Leverage the unittest harness to have tox output performance data on each python version tested
    """
    @unittest.skipIf(sys.version_info < (2,6), 'not doing performance tests on old versions')
    def test_performance(self):
        """
        Write out performance results to a file
        """
        import logging_unterpolation.tests.performance_results
        

class TestSingleFileImportCase(PatchedTestsMixin, BaseLoggerTestCase):
    """
    Tests that the simplest cases, importing logging and patching within
    the same file, works as expected
    """

    def setUp(self):
        """
        set up the patched logger
        """

        import logging
        from logging_unterpolation import patch_logging
        patch_logging()

        super(TestSingleFileImportCase, self).setUp()
        

class TestHandlingPreFormatPythonPatch(BaseLoggerTestCase):
    
    @unittest.skipUnless(sys.version_info < (2,6), 'skipping old version tests')
    def test_handle_patch_gracefully(self):
        """
        check to make sure that patching on a version of python too
        old to have the str.format method doesn't yield unexpected 
        results
        """
        import logging
        from logging_unterpolation import patch_logging

        patch_logging()
