from __future__ import annotations

import aiohttp
import async_timeout

DEFAULT_TIMEOUT = 5

class SimonGoApi:
    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self._host = host.rstrip("/")
        self._session = session

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"http://{self._host}{path}"

    async def get(self, path: str) -> bool:
        url = self._url(path)
        try:
            with async_timeout.timeout(DEFAULT_TIMEOUT):
                async with self._session.get(url) as resp:
                    return resp.status == 200
        except Exception:
            return False

    # Common helpers (switch)
    async def switch_on(self) -> bool: return await self.get("/s/1")
    async def switch_off(self) -> bool: return await self.get("/s/0")
    async def switch_toggle(self) -> bool: return await self.get("/s/2")
    async def switch_for_time(self, seconds: int) -> bool:
        return await self.get(f"/s/1/forTime/{seconds}/ns/0")

    # Switch D
    async def switch_d_set(self, channel: int, on: bool) -> bool:
        return await self.get(f"/s/{channel}/" + ("1" if on else "0"))
    async def switch_d_toggle(self, channel: int) -> bool:
        return await self.get(f"/s/{channel}/2")
    async def switch_d_for_time(self, channel: int, seconds: int) -> bool:
        return await self.get(f"/s/{channel}/1/forTime/{seconds}/ns/0")

    # Dimmer
    async def dimmer_set_hex(self, hex_value: str) -> bool:
        return await self.get(f"/s/{hex_value}")
    async def dimmer_inc(self, step: int) -> bool:
        return await self.get(f"/s/inc/{step}")
    async def dimmer_dec(self, step: int) -> bool:
        return await self.get(f"/s/dec/{step}")
    async def dimmer_off(self) -> bool:
        return await self.get("/s/00")
    async def dimmer_full(self) -> bool:
        return await self.get("/s/FF")
    async def dimmer_effect(self, effect: int, seconds: int | None = None) -> bool:
        return await self.get(f"/s/x/{effect}" + (f"/forTime/{seconds}" if seconds else ""))

    # RGBW
    async def rgbw_set_hex(self, rrggbbww: str) -> bool:
        return await self.get(f"/s/{rrggbbww}")
    async def rgbw_effect(self, effect: int) -> bool:
        return await self.get(f"/s/x/{effect}")

    # Shutter / Venetian
    async def shutter_up(self) -> bool: return await self.get("/s/u")
    async def shutter_down(self) -> bool: return await self.get("/s/d")
    async def shutter_stop(self) -> bool: return await self.get("/s/s")
    async def shutter_toggle(self) -> bool: return await self.get("/s/n")
    async def shutter_favorite(self) -> bool: return await self.get("/s/f")
    async def shutter_set_position(self, pos: int) -> bool:
        return await self.get(f"/s/p/{pos}")
    async def shutter_set_tilt(self, percent: int) -> bool:
        return await self.get(f"/s/t/{percent}")

    # Rollergate
    async def roller_open(self) -> bool: return await self.get("/s/o")
    async def roller_close(self) -> bool: return await self.get("/s/c")
    async def roller_stop(self) -> bool: return await self.get("/s/s")
    async def roller_toggle(self) -> bool: return await self.get("/s/n")
    async def roller_vent(self) -> bool: return await self.get("/s/w")
    async def roller_set_position(self, pos: int) -> bool:
        return await self.get(f"/s/p/{pos}")

    # Gate / Door pulses
    async def gate_pulse1(self) -> bool: return await self.get("/s/p")
    async def gate_pulse2(self) -> bool: return await self.get("/s/s")

    # Thermo
    async def thermo_off(self) -> bool: return await self.get("/s/0")
    async def thermo_on(self) -> bool: return await self.get("/s/1")
    async def thermo_boost(self) -> bool: return await self.get("/s/3")
    async def thermo_set_raw(self, raw: int) -> bool:
        return await self.get(f"/s/t/{raw}")
