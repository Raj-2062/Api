import random
import string
import datetime

def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def is_code_expired(created_at, minutes=30):
    return (datetime.datetime.utcnow() - created_at).total_seconds() > minutes * 60
