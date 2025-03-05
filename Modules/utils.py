import io
import re
from .constants import EMAIL_PATTERN

def load_to_memory(file):
    with open(file, 'rb') as memory_file:
        memory_file = io.BytesIO(memory_file.read())
        memory_file.name = file
    
    return memory_file

def validate_link(link):
    if link.startswith("mailto:") or link.startswith("tel:") or link.startswith("sms:"):
        return False

    if re.match(EMAIL_PATTERN, link):
        return False
    
    return True