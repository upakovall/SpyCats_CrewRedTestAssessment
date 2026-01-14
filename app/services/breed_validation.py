import time
import httpx

class BreedValidator:
    def __init__(self, api_key: str | None):
        self.api_key = api_key
        self._cache: dict[str, tuple[bool, float]] = {}  # breed -> (ok, expires_at)

    async def is_valid_breed(self, breed: str) -> bool:
        b = breed.strip().lower()
        now = time.time()

        cached = self._cache.get(b)
        if cached and cached[1] > now:
            return cached[0]

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.thecatapi.com/v1/breeds", headers=headers)
            r.raise_for_status()
            breeds = r.json()

        ok = any((item.get("name", "").strip().lower() == b) for item in breeds)
        self._cache[b] = (ok, now + 6 * 60 * 60)  # 6 часов
        return ok
