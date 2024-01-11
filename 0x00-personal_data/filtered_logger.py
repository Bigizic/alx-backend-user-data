#!/usr/bin/env python3
"""Implementation of various functions
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
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        host=d_host, port=3306,
        user=d_user, password=d_pwd, database=db)
    return conn


def main() -> None:
    """ retrieve all rows in the users table
    """
    conn = get_db()
    pii_fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    col = pii_fields.split(',')
    query = f'SELECT {pii_fields} FROM USERS;'
    info_logger = get_logger()

    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for r in rows:
            data = map(lambda x: '{}={}'.format(x[0], x[1]), zip(col, r))
            word = '{};'.format('; '.join(list(data)))
            i = ('user_data', logging.INFO, None, None, word, None, None)
            log_record = logging.LogRecord(*i)
            info_logger.handle(log_record)


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


if __name__ == '__main__':
    main()
