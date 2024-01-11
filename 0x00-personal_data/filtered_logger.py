#!/usr/bin/env python3
"""A function called filter_datum that returns the log message obfuscated
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ uses regex to replace occurences of certain fled values """
    return re.sub(r'(\b(?:{}))=(.*?)(?={}|$)'.format('|'.join(fields),
                  re.escape(separator)), lambda match: match.group(1)
                  + '=' + redaction, message)
