class InvalidInteger(Exception):
    """Exception raised for invalid bencode integer."""
    pass

class InvalidString(Exception):
    """Exception raised for invalid bencode string."""
    pass

class InvalidList(Exception):
    """Exception raised for invalid bencode list."""
    pass

class InvalidDictionary(Exception):
    """Exception raised for invalid bencode dictionary."""
    pass