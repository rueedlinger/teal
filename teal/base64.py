import base64

from teal.model import Document, Data, DataEncoding


class Base64:
    def __init__(self):
        pass

    def encode(self, data, filename):
        encoded = base64.b64encode(data)

        return Document.parse_obj(
            {
                "name": filename,
                "data": Data.parse_obj(
                    {"encoding": DataEncoding.base64, "content": encoded}
                ),
            }
        )
