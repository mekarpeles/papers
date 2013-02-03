from datetime import datetime

def str2datetime(s, fmt="%a %b %d %H:%M:%S %Y"):
    """Converts str timestamp to datetime"""
    return s if type(s) is datetime else \
        datetime.strptime(s, fmt)
