#!/usr/bin/env python3
""" Protecting Personally Identifiable Information (PII) """

import logging
import re
from typing import List
from mysql.connector import connection
from os import environ

# List of PII fields to obfuscate
PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')

# Function to obfuscate sensitive PII data in the log message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message with sensitive fields obfuscated."""
    pattern = r'(?<={}=).*?(?={})'.format(separator.join(fields), re.escape(separator))
    return re.sub(pattern, redaction, message)

# Function to configure and return the logger


def get_logger() -> logging.Logger:
    """Returns a configured logger object."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

# Function to establish a connection to the MySQL database
def get_db() -> connection.MySQLConnection:
    """Connects to the MySQL server using environmental variables."""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    connector = connection.MySQLConnection(
        user=root,
        password=root,
        host=db_host,
        database=db_name)
    return connector

# Custom Formatter class to redact sensitive PII data in logs
class RedactingFormatter(logging.Formatter):
    """Custom formatter to redact sensitive fields in log records."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"


    def __init__(self, fields: List[str]):
        """Initializes the RedactingFormatter class instance."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records to redact sensitive fields."""
        return filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)

# Main function to retrieve user data from the database and log it with redacted PII
def main() -> None:
    """
    Connect to the database using get_db
    and retrieve all rows in the users table, logging each row with redacted PII.
    """
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)

    cur.close()
    db.close()

if __name__ == "__main__":
    main()
