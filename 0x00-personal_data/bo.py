#!/usr/bin/env python3

"""PII Obfuscation"""

from typing import List
import logging
import re
from mysql.connector import connection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscate sensitive data"""
    temp = message
    for field in fields:
        temp = re.sub(field + "=.*?" + separator, field + "=" + redaction + separator, temp)
    return temp

def get_logger() -> logging.Logger:
    """Create & configure logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

def get_db() -> connection.MySQLConnection:
    """Connect to MySQL"""
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

class RedactingFormatter(logging.Formatter):
    """Custom log formatter"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter incoming logs"""
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)

def main() -> None:
    """Retrieve & log user data"""
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
