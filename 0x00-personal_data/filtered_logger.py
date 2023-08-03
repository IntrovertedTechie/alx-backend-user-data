#!/usr/bin/env python3
"""
log_utils.py
"""

import logging
import re
from typing import List
from logging import Logger, StreamHandler
from mysql.connector import connection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates sensitive fields in log message.

    Args:
        fields: List[str]
        redaction: str
        message: str
        separator: str

    Returns:
        str
    """
    return re.sub('(' + '|'.join(fields) + ')=.*?' + separator,
                  r'\1=' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """
    Custom log formatter for redacting sensitive fields.

    Args:
        fields: List[str]

    Methods:
        format(record: logging.LogRecord) -> str
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record with redacted sensitive fields.

        Args:
            record: logging.LogRecord

        Returns:
            str
        """
        return filter_datum(self.fields, self.REDACTION,
                            record.getMessage(), self.SEPARATOR)


def get_logger() -> Logger:
    """
    Returns logger obj.

    Returns:
        Logger
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to secure MySQL server.

    Returns:
        connection.MySQLConnection
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector


def main() -> None:
    """
    Retrieves and logs filtered data from the "users" table.
    """
    db = get_db()
    cursor = db.cursor()

    query = ('SELECT * FROM users;')
    cursor.execute(query)
    fetch_data = cursor.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; ' \
                 'last_login={}; user_agent={};'
        fields = fields.format(*row)
        logger.info(fields)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()