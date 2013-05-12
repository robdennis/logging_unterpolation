from logging_unterpolation.tests import BaseLoggerTestCase, PatchedTestsMixin
# TODO: since there's no actual "unpatching" there's no cleanup between tests


class TestSingleFileImportCase(PatchedTestsMixin, BaseLoggerTestCase):
    # PatchedTestsMixin must go first to override the base methods
    """
    Tests that the simplest cases, importing logging and patching within
    the same file, works as expected
    """

    @classmethod
    def setUpClass(cls):
        """
        set up the patched logger
        """

        import logging
        from logging_unterpolation import patch_logging
        patch_logging()

        super(TestSingleFileImportCase, cls).setUpClass()
