from typing import List, Dict, Optional, Tuple, Union

from .exceptions import (
    InvalidInteger,
    InvalidString,
    InvalidList,
    InvalidDictionary
    )

class Decoder:
    """Decodes bencode data."""
    def __init__(self: "Decoder", encoding: Optional[str] = None) -> None:
        """
        Initialize Decoder.

        Parameters:
            - encoding (str, optional): Encoding for bencode string. (default: None)
        """

        self.encoding = encoding
    
    def decode_integer(self: "Decoder", value: bytes, pos: int = 0) -> Tuple[int, int]:
        """
        Decode an bencode integer.
        
        Parameters:
            - value (bytes): a bencode integer in bytes format.
            - pos (int, optional): position index from where to start parsing integer. (default: 0)
        
        Raises:
            - InvalidInteger: if bencoded integer is invalid.
            - ValueError: if integer is invalid.
        
        Returns:
            Tuple[int, int]: a tuple of integer and next position.
        
        Example:
            >>> from bencode.decoder import Decoder
            >>> decoder = Decoder()
            >>> decoder.decode_integer(b"i42e")
            (42, 4)
        """
        start_index = value.find(b"i", pos)
        if start_index == -1:
            raise InvalidInteger("Integer start 'i' not found")
        
        end_index = value.find(b"e", pos)
        if end_index == -1:
            raise InvalidInteger("Interger end 'e' not found")
        
        if value[start_index+1:start_index+2] == b"0" and start_index+2 != end_index:
            raise InvalidInteger(f"Integer cannot start with leading zero (postion: {start_index+1})")
        elif value[start_index+1:start_index+2] == b"-" and value[start_index+2:start_index+3] == b"0":
            raise InvalidInteger(f"Negative zero is not allowed (position: {start_index+1})")
        
        integer = value[start_index+1:end_index]
        try:
            return (int(integer), end_index+1)
        except ValueError:
            raise InvalidInteger(f"Invalid integer: {integer} is not a valid integer (position: {start_index+1})")
    
    def decode_string(self: "Decoder", value: bytes, pos: int = 0) -> Tuple[Union[bytes, str], int]:
        """
        Decode a bencode string.
        
        Parameters:
            - value (bytes): A bencode string in bytes format.
            - pos (int, optional): Position index from where to start parsing string. (default: 0)
        
        Raises:
            - InvalidString: If bencoded string is invalid.
            - ValueError: If string length is invalid.
        
        Returns:
            Tuple[Union[bytes, str], int]: A tuple of decoded string and next position.
        
        Example:
            >>> from bencode.decoder import Decoder
            >>> decoder = Decoder()
            >>> decoder.decode_string(b"4:spam")
            (b"spam", 6)
        """
        colon = value.find(b":", pos)
        if colon == -1:
            raise InvalidString("String colon not found")
        elif value[pos:pos+1] == b"-":
            raise InvalidString("Negative length of string not allowed")
        
        try:
            length = int(value[pos:colon])
        except ValueError:
            raise InvalidString(f"Invalid length integer for string: {value[pos:colon]}")
        
        end_index = colon+1+length
        content = value[colon+1:end_index]
        
        if len(content) < length:
            raise InvalidString(f"String length is lesser than {length}")
        
        if self.encoding:
            content = content.decode(self.encoding)
        
        return (content, end_index)
    
    def decode_list(self: "Decoder", value: bytes, pos: int = 0) -> Tuple[List, int]:
        """
        Decode a bencode list.
        
        Parameters:
            - value (bytes): A bencode list in bytes format.
            - pos (int, optional): Position index from where to start parsing list. (default: 0)
        
        Raises:
            - InvalidList: If bencoded list is invalid.
        
        Returns:
            Tuple[List, int]: A tuple of decoded list and next position.
        
        Example:
            >>> from bencode.decoder import Decoder
            >>> decoder = Decoder()
            >>> decoder.decode_list(b"l4:spami42ee")
            ([b'spam', 42], 12)
        """
        start_index = value.find(b"l", pos)
        if start_index == -1:
            raise InvalidList("List start 'l' not found")
        
        items = []
        curr_index = start_index+1
        while value[curr_index:curr_index+1] != b"e":
            curr_char = value[curr_index:curr_index+1]
            if curr_char == b"":
                raise InvalidList("List end 'e' not found")
            
            item, curr_index = self.decode_value(value, curr_index)
            if item is None:
                raise InvalidList(f"Invalid list item: {curr_char}")
            items.append(item)
        return (items, curr_index+1)
    
    def decode_dictionary(self: "Decoder", value: bytes, pos: int = 0) -> Tuple[Dict, int]:
        """
        Decode bencode data.
        
        Parameters:
            - value (bytes): Bencode data in bytes format.
        
        Raises:
            - ValueError: If the bencode data is invalid.
        
        Returns:
            Union[int, bytes, str, Dict, List]: Decoded bencode data.
        
        Example:
            >>> from bencode.decoder import Decoder
            >>> decoder = Decoder()
            >>> decoder.decode_dictionary(b"d3:bar4:spam3:fooi42ee")
            ({b'bar': b'spam', b'foo': 42}, 22)
        """
        start_index = value.find(b"d", pos)
        if start_index == -1:
            raise InvalidDictionary("Dictionary start 'd' not found")
        
        items = {}
        curr_index = start_index+1
        while value[curr_index:curr_index+1] != b"e":
            curr_char = value[curr_index:curr_index+1]
            if curr_char == b"":
                raise InvalidDictionary("Dictionary end 'e' not found")
            
            # key of the dict
            if curr_char == b"i":
                k, curr_index = self.decode_integer(value, curr_index)
            elif b"0" <= curr_char <= b"9":
                k, curr_index = self.decode_string(value, curr_index)
            else:
                raise InvalidDictionary(f"Invalid dictionary key: {curr_char}")
            
            # value of the key
            curr_char = value[curr_index:curr_index+1]
            v, curr_index = self.decode_value(value, curr_index)
            if v is None:
                raise InvalidDictionary(f"Invalid dictionary value of the key: {curr_char}")
            
            items[k] = v
        return (items, curr_index+1)
    
    def decode(self: "Decoder", value: bytes) -> Union[int, bytes, str, Dict, List]:
        """
        Decode bencode data.
        
        Parameters:
            - value (bytes): Bencode data in bytes format.
        
        Raises:
            - ValueError: If the bencode data is invalid.
        
        Returns:
            Union[int, bytes, str, Dict, List]: Decoded bencode data.
        
        Example:
            >>> from bencode.decoder import Decoder
            >>> decoder = Decoder()
            >>> decoder.decode(b"i42e4:spamli42eed3:foo3:bare")
            [42, b'spam', [42], {b'foo': b'bar'}]
        """
        curr_index = 0
        items = []
        while value[curr_index:curr_index+1] != b"":
            curr_char = value[curr_index:curr_index+1]
            
            item, curr_index = self.decode_value(value, curr_index)
            if item is None:
                raise ValueError(f"Invalid bencode type: {curr_char}")
            
            items.append(item)
        return items if len(items) > 1 else items[0]
    
    def decode_value(self: "Decoder", value: bytes, index: Optional[int] = 0) -> Tuple[Union[int, bytes, str, List, Dict], int]:
        """
        Decode a bencode value.
        
        Parameters:
            - value (bytes): Bencode value in bytes format.
            - index (int, optional): Index position in the bencode data. (default: 0)
        
        Returns:
            Tuple[Union[int, bytes, str, List, Dict], int]: A tuple of decoded value and next position.
        """
        character = value[index:index+1]
        if character == b"i":
            return self.decode_integer(value, index)
        elif b"0" <= character <= b"9":
            return self.decode_string(value, index)
        elif character == b"l":
            return self.decode_list(value, index)
        elif character == b"d":
            return self.decode_dictionary(value, index)
        else:
            return (None, None)