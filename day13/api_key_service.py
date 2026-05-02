import uuid


class ApiKeyService:
    def __init__(self):
        self.api_keys = set()

    def generate_api_key(self):
        key = str(uuid.uuid4())
        self.api_keys.add(key)
        return key

    def is_valid_key(self, key):
        return key in self.api_keys