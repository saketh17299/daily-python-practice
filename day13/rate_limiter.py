import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, limit=5, window_seconds=60):
        self.limit = limit
        self.window = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, api_key):
        now = time.time()
        timestamps = self.requests[api_key]

        # remove old timestamps
        self.requests[api_key] = [
            t for t in timestamps if now - t < self.window
        ]

        if len(self.requests[api_key]) >= self.limit:
            return False

        self.requests[api_key].append(now)
        return True