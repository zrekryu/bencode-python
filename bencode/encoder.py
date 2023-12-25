from typing import Dict, List, Optional, Union

class Encoder:
    """Encodes Python data types into bencode format."""
    
    def __init__(self: "Encoder", encoding: Optional[str] = "utf-8") -> None:
        """
        Initialize Encoder.
        
        Parameters:
            - encoding (str, optional): Encoding for bencode string. (default: "utf-8")
        """
        self.encoding = encoding
    
    def encode_integer(self: "Encoder", value: int, encoding: Optional[str] = None) -> bytes:
        """
        Encode an integer into bencode format.
        
        Parameters:
            - value (int): Integer to be encoded.
            - encoding (str, optional): Encoding for bencode string. (default: None)
        
        Raises:
            - TypeError: If the value is not an integer.
        
        Returns:
            bytes: Encoded bencode integer.
        
        Example:
            >>> from bencode.encoder import Encoder
            >>> encoder = Encoder()
            >>> encoder.encode_integer(42)
            b'i42e'
        """
        if not isinstance(value, int):
            raise TypeError(f"Value must be an integer")
        return f"i{value}e".encode(encoding if encoding else self.encoding)
    
    def encode_string(self: "Encoder", value: str, encoding: Optional[str] = None) -> bytes:
        """
        Encode a string into bencode format.
        
        Parameters:
            - value (str): String to be encoded.
            - encoding (str, optional): Encoding for bencode string. (default: None)
        
        Returns:
            bytes: Encoded bencode string.
        
        Example:
            >>> from bencode.encoder import Encoder
            >>> encoder = Encoder()
            >>> encoder.encode_string("spam")
            b'4:spam'
        """
        return f"{len(value)}:{value}".encode(encoding if encoding else self.encoding)
    
    def encode_list(self: "Encoder", value: List, encoding: Optional[str] = None, skip_unknown_types: Optional[bool] = False) -> bytes:
        """
        Encode a list into bencode format.
        
        Parameters:
            - value (List): List to be encoded.
            - encoding (str, optional): Encoding for bencode string. (default: None)
            - skip_unknown_types (bool): Whether to skip encoding unknown types. (default: False)
        
        Returns:
            bytes: Encoded bencode list.
        
        Example:
            >>> from bencode.encoder import Encoder
            >>> encoder = Encoder()
            >>> encoder.encode_list([42, "spam"])
            b'li42e4:spame'
        """
        result = b"l"
        for item in value:
            result += self.encode_value(item)
        return result + b"e"
    
    def encode_dictionary(self: "Encoder", value: Dict, encoding: Optional[str] = None, skip_unknown_types: Optional[bool] = False) -> bytes:
        """
        Encode a dictionary into bencode format.
        
        Parameters:
            - value (Dict): Dictionary to be encoded.
            - encoding (str, optional): Encoding for bencode string. (default: None)
            - skip_unknown_types (bool): Whether to skip encoding unknown types. (default: False)
        
        Returns:
            bytes: Encoded bencode dictionary.
        
        Example:
            >>> from bencode.encoder import Encoder
            >>> encoder = Encoder()
            >>> encoder.encode_dictionary({"key": "value"})
            b'd3:foo3:bare'
        """
        result = b"d"
        for k, v in value.items():
            result += self.encode_value(k)
            result += self.encode_value(v)
        return result + b"e"
    
    def encode_value(
        self: "Encoder",
        value: Union[int, bytes, List, Dict],
        encoding: Optional[str] = None,
        skip_unknown_types: Optional[bool] = False
        ) -> None:
        """
        Encode a Python data type into bencode format.
        
        Parameters:
            - value (Union[int, str, List, Dict]): Value to be encoded.
            - encoding (str, optional): Encoding for bencode string. (default: None)
            - skip_unknown_types (bool): Whether to skip encoding unknown types. (default: False)
        
        Raises:
            - ValueError: If the value type is not supported.
        
        Returns:
            bytes: Encoded bencode value.
        """
        if isinstance(value, int):
            return self.encode_integer(value, encoding)
        elif isinstance(value, str):
            return self.encode_string(value, encoding)
        elif isinstance(value, list):
            return self.encode_list(value, encoding)
        elif isinstance(value, dict):
            return self.encode_dictionary(ValueError, encoding)
        else:
            if not skip_unknown_types:
                raise ValueError(f"Invalid bencode type: {type(value)}")