#!/usr/bin/env python3

"""Protecting PII - A program to obfuscate and log sensitive user data."""

from typing import List
import logging
import re
from mysql.connector import connection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscate sensitive data in the log message."""
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)
    return temp

def get_logger() -> logging.Logger:
    """Create and configure a logger object for user data."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

def get_db() -> connection.MySQLConnection:
    """Connect to the MySQL server using environmental variables."""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    connector = connection.MySQLConnection(
        user=root,
        password="",
        host=db_host,
        database=)
    return connector

class RedactingFormatter(logging.Formatter):
    """Custom log formatter to redact sensitive data in logs."""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the RedactingFormatter with the list of fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records."""
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)

def main() -> None:
    """Retrieve user data from the database and log it."""
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; ' \
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        logger.info(fields)

    cur.close()
    db.close()

if __name__ == "__main__":
    main()
