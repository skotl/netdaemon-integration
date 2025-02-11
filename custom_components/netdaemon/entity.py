"""NetDaemon entity."""
from awesomeversion import AwesomeVersion
from homeassistant.const import __version__ as HA_VERSION
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_ICON,
    ATTR_UNIT,
    DOMAIN,
    INTEGRATION_VERSION,
    NAME,
    ND_ID,
)


class NetDaemonEntity(CoordinatorEntity):
    """NetDaemon entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{ND_ID}_{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if not self.entity_id:
            return None
        return self._coordinator.data[self.entity_id][ATTR_UNIT]

    @property
    def icon(self):
        """Return the icon."""
        if not self.entity_id:
            return None
        return self._coordinator.data[self.entity_id][ATTR_ICON]

    @property
    def device_info(self):
        """Return device information about NetDaemon."""
        info = {
            "identifiers": {(DOMAIN, ND_ID)},
            "name": NAME,
            "sw_version": INTEGRATION_VERSION,
            "manufacturer": "netdaemon.xyz",
        }
        # LEGACY can be removed when min HA version is 2021.12
        if AwesomeVersion(HA_VERSION) >= "2021.12.0b0":
            # pylint: disable=import-outside-toplevel
            from homeassistant.helpers.device_registry import DeviceEntryType

            info["entry_type"] = DeviceEntryType.SERVICE
        else:
            info["entry_type"] = "service"
        return info

    @property
    def extra_state_attributes(self):
        """Return attributes for the sensor."""
        attributes = {"integration": DOMAIN}
        if self.entity_id and self._coordinator.data[self.entity_id][ATTR_ATTRIBUTES]:
            for attr in self._coordinator.data[self.entity_id][ATTR_ATTRIBUTES]:
                attributes[attr] = self._coordinator.data[self.entity_id][
                    ATTR_ATTRIBUTES
                ][attr]
        return attributes

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)
