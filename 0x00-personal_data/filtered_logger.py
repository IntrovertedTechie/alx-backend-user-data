#!/usr/bin/env python3

import re

def filter_datum(fields, redaction, message, separator):
    pattern = r'(?<={}=).*?(?={})'.format(separator.join(fields), re.escape(separator))
    return re.sub(pattern, redaction, message)