#!/usr/bin/env python3
""" a function called filter_datum that returns the log message obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
    """ uses regex to replace occurences of certain fled values """
    return re.sub(r'(\b(?:{}))=(.*?)(?={}|$)'.format(
                  '|'.join(fields), re.escape(separator)),
                  lambda match: match.group(1) + '=' + redaction,
                  message)
