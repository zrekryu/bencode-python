# Bencode
Bencode encoder and decoder written in python.

## Installation
```bash
pip install py-bencode
```

## Usage

### Decoder
Decoding bencode data.
```py
from bencode.decoder import Decoder

decoder = Decoder()
decoded = decoder.decode(b"i42e")
print(decoded) # 42
```

### Encoder
Encoding Python data types into bencode format.
```py
from bencode.encoder import Encoder

encoder = Encoder()
encoded = encoder.encode(42))
print(encoded) # b'i42e'
```

# License
Licensed under the MIT License.