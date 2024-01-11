#!/usr/bin/env python3
"""A function called filter_datum that returns the log message obfuscated
"""

import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ uses regex to replace occurences of certain fled values """
    return re.sub(r'(\b(?:{}))=(.*?)(?={}|$)'.format('|'.join(fields),
                  re.escape(separator)), lambda match: match.group(1)
                  + '=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = list(fields)

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records
        """
        word = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, word, self.SEPARATOR)
