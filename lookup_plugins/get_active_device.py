from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    """Extension to the base looup."""

    def run(self, terms, variables=None, **kwargs):
        """Variabele terms contains a list with supplied parameters.

        - devices  -> The F5 device list from which the active device is selected
        """
        # Sufficient parameters
        if len(terms) < 1:
            raise AnsibleError(
                "Insufficient parameters. Need: 'devices'."
            )

        # Get the parameters
        devices = terms[0]

        if not isinstance(devices, list):
            raise AnsibleError("Input 'devices' must be a list")
        if not len(devices) == 2:
            raise AnsibleError("Input 'devices' should be list of 2 device objects")
        for device in devices:
            if not isinstance(device, dict) or not device.get("management_address", None) or not device.get("failover_state", None):
                raise AnsibleError("All input devices in the 'devices' list must be a valid f5 device object")

        for device in devices:
            if device.get("failover_state").lower() == "active":
                result = {
                    "address": device.get("management_address"),
                    "device": device
                }
                return result

        raise AnsibleError("No active address found")
