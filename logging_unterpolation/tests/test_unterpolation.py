from logging_unterpolation.tests import BaseLoggerTestCase, PatchedTestsMixin

# PatchedTestsMixin must go first to override the base methods
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
        


