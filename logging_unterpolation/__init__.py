# Copyright (c) 2011 Rob Dennis. See LICENSE for details

import sys
import logging

def patch_logging():
    """
    patch the logging LogRecord based on the python version calling the patch
    method
    """
    if sys.version_info >= (2, 6,) and sys.version_info <= (2, 7,):
        logging.LogRecord = Python26FormattingLogRecord
    elif sys.version_info >= (3, 2,):
        # there's a misdirection done making:
        # _logRecordFactory = LogRecord
        # which means we need to patch both
        logging._logRecordFactory = Python32FormattingLogRecord
        logging.LogRecord = Python32FormattingLogRecord
    elif sys.version_info < (2, 6,):
        # python versions before 2.6 don't have the string format syntax and 
        # shouldn't be patched
        pass
    else:
        logging.LogRecord = FormattingLogRecord


# this class overrides te getMessage method, which does change between
# python versions, so there are subclasses for any special cases
class FormattingLogRecord(logging.LogRecord):
    """
    Overriding LogRecord to support PEP-3101 style string formatting
    """
    def _getUnterpolatedMessage(self, msg):
        """
        Returns the formatted string, will first attempt str.format and will
        fallback to msg % self.args as it was originally
        Broken out to support reusing the reformatting logic in all
        the special case-handling subclassed of FormattingLogRecord
        """
        original_msg = msg
        if isinstance(self.args, dict):
            # special case handing for unpatched logging supporting
            # statements like:
            # logging.debug("a %(a)d b %(b)s", {'a':1, 'b':2})
            args = (self.args,)
        else:
            # typical case where the LogRecord init didn't do anything
            # to the passed arguments
            args = self.args

        try:
            msg = msg.format(*args)
        except UnicodeEncodeError:
            # This is most likely due to formatting a non-ascii string argument
            # into a bytestring, which the %-operator automatically handles
            # by casting the left side (the "msg" variable) in this context
            # to unicode. So we'll do that here

            if sys.version_info >= (3, 0,):
                # this is most likely unnecessary on python 3, but it's here
                # for completeness, in the case of someone manually creating
                # a bytestring
                unicode_type = str
            else:
                unicode_type = unicode

            # handle the attempt to print utf-8 encoded data, similar to
            # %-interpolation's handling of unicode formatting non-ascii
            # strings
            msg = unicode_type(msg).format(*args)

        except ValueError:
            # From PEP-3101, value errors are of the type raised by the format
            # method itself, so see if we should fall back to original
            # formatting since there was an issue
            if '%' in msg:
                msg = msg % self.args
            else:
                # we should NOT fall back, since there's no possible string
                # interpolation happening and we want a meaningful error
                # message
                raise

        if msg == original_msg and '%' in msg:
            # there must have been no string formatting methods
            # used, given the presence of args without a change in the msg
            # fall back to original formatting, including the special case
            # for one passed dictionary argument
            msg = msg % self.args

        return msg

    # copy + pasted from python source, splitting out the 'un'teroplation
    # to a separate method
    def getMessage(self):
        """
        Return the message for this LogRecord.

        Return the message for this LogRecord after merging any user-supplied
        arguments with the message.

        Will attempt string formatting using
        PEP-3101 formatting syntax, with fallback behavior to using string
        interpolation
        """
        if not logging._unicode: #if no unicode support...
            msg = str(self.msg)
        else:
            msg = self.msg
            if not isinstance(msg, str):
                try:
                    msg = str(self.msg)
                except UnicodeError:
                    msg = self.msg      #Defer encoding till later

        if self.args:
            msg = self._getUnterpolatedMessage(msg)

        return msg


# Python26 had a different getMessage method, apparently re-written for py27
class Python26FormattingLogRecord(FormattingLogRecord):
    def getMessage(self):
        """
        Return the message for this LogRecord.

        Return the message for this LogRecord after merging any user-supplied
        arguments with the message.
        """
        if not hasattr(logging.types, "UnicodeType"): #if no unicode support...
            msg = str(self.msg)
        else:
            msg = self.msg
            if type(msg) not in (logging.types.UnicodeType,
                                 logging.types.StringType):
                try:
                    msg = str(self.msg)
                except UnicodeError:
                    msg = self.msg      #Defer encoding till later
        if self.args:
            msg = self._getUnterpolatedMessage(msg)
        return msg


# Python32 has a new getMessage method and I'm assuming this is the way forward
class Python32FormattingLogRecord(FormattingLogRecord):
    def getMessage(self):
        """
        Return the message for this LogRecord.

        Return the message for this LogRecord after merging any user-supplied
        arguments with the message.
        """
        msg = str(self.msg)
        if self.args:
            msg = self._getUnterpolatedMessage(msg)
        return msg
