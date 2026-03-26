import aiohttp
import async_timeout
import logging

_LOGGER = logging.getLogger(__name__)

class DabNetApi:
    def __init__(self, host: str):
        self._host = host

    async def _get_json(self, path: str):
        url = f"http://{self._host}/{path}"
        _LOGGER.debug("DABNet GET %s", url)
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(5):
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    return await resp.json()

    async def _get(self, path: str):
        url = f"http://{self._host}/{path}"
        _LOGGER.debug("DABNet GET %s", url)
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(5):
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    return await resp.text()

    async def get_status(self):
        # Verwacht JSON zoals:
        # {
        #   "power": true,
        #   "playing": true,
        #   "volume": 0.37,
        #   "title": "Track title",
        #   "artist": "Artist",
        #   "mode": "DAB",
        #   "cover": "http://.../cover.jpg",
        #   "clean_title": "Netjes opgeschoonde titel",
        #   "channels": ["NPO Radio 1", "NPO Radio 2", ...]
        # }
        return await self._get_json("api/status")

    async def set_volume(self, volume: float):
        # volume 0.0–1.0
        return await self._get(f"api/volume?set={volume}")

    async def set_power(self, on: bool):
        return await self._get(f"api/power?set={'on' if on else 'off'}")

    async def play(self):
        return await self._get("api/play")

    async def pause(self):
        return await self._get("api/pause")

    async def stop(self):
        return await self._get("api/stop")

    async def set_channel(self, channel: str):
        return await self._get(f"api/channel?set={channel}")

    async def set_sound_mode(self, mode: str):
        return await self._get(f"api/mode?set={mode}")
