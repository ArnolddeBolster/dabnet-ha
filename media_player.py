from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.components.media_player.const import (
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_HOST, CONF_NAME

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]

    name = entry.data.get(CONF_NAME)
    host = entry.data.get(CONF_HOST)

    async_add_entities(
        [DabNetMediaPlayer(coordinator, api, entry.entry_id, name, host)],
        True,
    )

class DabNetMediaPlayer(CoordinatorEntity, MediaPlayerEntity):
    _attr_should_poll = False

    _attr_supported_features = (
        MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, coordinator, api, entry_id, name, host):
        super().__init__(coordinator)
        self._api = api
        self._attr_unique_id = f"dabnet_{host}"
        self._attr_name = name
        self._entry_id = entry_id
        self._host = host

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=self._attr_name,
            manufacturer="DAB Net",
            model="DAB Net Receiver",
        )

    # ---- STATE & ATTRIBUTES ----

    @property
    def state(self):
        data = self.coordinator.data or {}
        if not data.get("power", True):
            return MediaPlayerState.OFF
        if data.get("playing"):
            return MediaPlayerState.PLAYING
        return MediaPlayerState.PAUSED

    @property
    def volume_level(self):
        data = self.coordinator.data or {}
        return data.get("volume")

    @property
    def is_volume_muted(self):
        data = self.coordinator.data or {}
        return data.get("muted", False)

    @property
    def media_title(self):
        data = self.coordinator.data or {}
        return data.get("title")

    @property
    def media_artist(self):
        data = self.coordinator.data or {}
        return data.get("artist")

    @property
    def sound_mode(self):
        data = self.coordinator.data or {}
        return data.get("mode")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        # Hier kun je direct je button-card sensoren op baseren:
        # sensor.room1_clean_title_2 -> clean_title
        return {
            "clean_title": data.get("clean_title"),
        }

    @property
    def entity_picture(self):
        data = self.coordinator.data or {}
        return data.get("cover")

    @property
    def source_list(self):
        data = self.coordinator.data or {}
        return data.get("channels") or []

    @property
    def source(self):
        data = self.coordinator.data or {}
        return data.get("current_channel")

    # ---- COMMANDS ----

    async def async_turn_on(self):
        await self._api.set_power(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self):
        await self._api.set_power(False)
        await self.coordinator.async_request_refresh()

    async def async_set_volume_level(self, volume: float):
        await self._api.set_volume(volume)
        await self.coordinator.async_request_refresh()

    async def async_mute_volume(self, mute: bool):
        # Als je API geen mute heeft, kun je hier eventueel volume onthouden
        # en naar 0 zetten. Voor nu: noop of implementeren als endpoint.
        pass

    async def async_media_play(self):
        await self._api.play()
        await self.coordinator.async_request_refresh()

    async def async_media_pause(self):
        await self._api.pause()
        await self.coordinator.async_request_refresh()

    async def async_media_stop(self):
        await self._api.stop()
        await self.coordinator.async_request_refresh()

    async def async_select_source(self, source: str):
        await self._api.set_channel(source)
        await self.coordinator.async_request_refresh()
