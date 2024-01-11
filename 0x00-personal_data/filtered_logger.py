#!/usr/bin/env python3
"""A function called filter_datum that returns the log message obfuscated
"""

import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filters(fields: List[str], redaction: str, message: str,
            separator: str) -> str:
    """Filter values in the log message based on specified fields"""
    return re.sub(r'(\b(?:{}))=(.*?)(?={}|$)'.format('|'.join(fields),
                  re.escape(separator)), lambda match: ' ' + match.group(1)
                  + '=' + redaction, message)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ uses regex to replace occurences of certain fled values """
    return re.sub(r'(\b(?:{}))=(.*?)(?={}|$)'.format('|'.join(fields),
                  re.escape(separator)), lambda match: match.group(1)
                  + '=' + redaction, message)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database
    """
    d_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    d_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    d_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db = os.getenv('PERSONAL_DATA_DB_NAME', '')

    return mysql.connector.connect(
            host=d_host, port=3306,
            user=d_user, password=d_pwd, database=db)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records """
        word = super(RedactingFormatter, self).format(record)
        return filters(self.fields, self.REDACTION, word, self.SEPARATOR)
