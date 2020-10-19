import json
import base64


class Packet:
    def __init__(self, data=None, timestamp=None, id=None):
        if data is None:
            data = b''
        self.data = data
        self.timestamp = timestamp
        self.id = id

    def pack(self):
        info = {
            'id': self.id,
            'timestamp': self.timestamp,
            'has_frame': len(self.data) != 0
        }

        info = json.dumps(info).encode('utf-8')

        packet = self.data + info
        packet = packet + len(info).to_bytes(4, byteorder='big')

        return packet
