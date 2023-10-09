from typing import Any

from ihcsdk.ihccontroller import IHCController

from homeassistant.components.cover import CoverDeviceClass, CoverEntity
from homeassistant.const import CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, IHC_CONTROLLER
from .ihcdevice import IHCDevice


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the IHC binary sensor platform."""
    if discovery_info is None:
        return
    devices = []
    for name, device in discovery_info.items():
        ihc_id = device["ihc_id"]
        product_cfg = device["product_cfg"]
        product = device["product"]
        # Find controller that corresponds with device id
        controller_id = device["ctrl_id"]
        ihc_controller: IHCController = hass.data[DOMAIN][controller_id][IHC_CONTROLLER]
        sensor = IhcCover(
            ihc_controller,
            controller_id,
            name,
            ihc_id,
            product_cfg.get(CONF_TYPE),
            product,
        )
        devices.append(sensor)
    add_entities(devices)


class IhcCover(IHCDevice, CoverEntity):
    """Representation of IHC Cover (garage door, blinds, etc.)."""

    def __init__(
        self,
        ihc_controller: IHCController,
        controller_id: str,
        name: str,
        ihc_id: int,
        device_class: str,
        product=None,
    ) -> None:
        """Initialize the IHC binary sensor."""
        super().__init__(ihc_controller, controller_id, name, ihc_id, product)
        self._state = None
        self._device_class = device_class

    @property
    def device_class(self) -> CoverDeviceClass:
        """Return the class of this sensor."""
        return self._device_class

    @property
    def is_closed(self) -> bool:
        return True

    @property
    def is_closing(self) -> bool:
        return False

    @property
    def is_opening(self) -> bool:
        return False

    def open_cover(self, **kwargs: Any) -> None:
        pass

    async def async_open_cover(self, **kwargs: Any) -> None:
        pass

    def close_cover(self, **kwargs: Any) -> None:
        pass

    async def async_close_cover(self, **kwargs: Any) -> None:
        pass
