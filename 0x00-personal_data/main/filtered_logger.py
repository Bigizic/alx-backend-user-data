#!/usr/bin/env python3
""" a function called filter_datum that returns the log message obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    uses regex to replace occurences of certain fled values
    @param (fields): <list of strings>
    @param (redaction): <str> represents the field to be obfuscated
    @param (message): <str> log line
    @param (separator): <str> represents the character which separates all fields
    Return: new log message
    """
    res = re.search(r'.$', message)
    my_dict = {}

    # delimeter = res.group() if res else None
    delimeter = separator

    if delimeter:
        something = message.split(delimeter)
        for c in something:
            if len(c) > 1:
                k, v = c.split('=')
                my_dict[k] = v

        for key, val in my_dict.items():
            if key in fields:
                my_dict[key] = redaction

        list_ = ''
        for key, val in my_dict.items():
            list_ += key + '=' + val + separator
        return list_
