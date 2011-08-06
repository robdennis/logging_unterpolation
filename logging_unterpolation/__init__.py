# Copyright (c) 2011 Rob Dennis. See LICENSE for details

import logging

def patch_logging():
    logging.LogRecord = FormattingLogRecord



class FormattingLogRecord(logging.LogRecord):
    def getMessage(self):
        """
        Return the message for this LogRecord.

        Return the message for this LogRecord after merging any user-supplied
        arguments with the message. Will attempt string formatting using the
        formatting method, with fallback behavior to using string interpolation
        as a backup
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

        def _fallback_to_interpolation(_msg):
            """
            convenience method to fallback to the original behavior of string
            interpolation

            :param _msg: the message to interpolate using the % operator
            :return: _msg % self.args
            """
            return _msg % self.args

        if self.args:
            original_msg = msg
            try:
                msg = msg.format(*self.args)
            except Exception:
                # fall back to original formatting
                msg = _fallback_to_interpolation(msg)

            if msg == original_msg:
                # there must have been no string formatting methods
                # used, given the presence of args without a change in the msg
                msg = _fallback_to_interpolation(msg)

        return msg