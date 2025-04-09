from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    """Extension to the base looup."""

    def run(self, terms, variables=None, **kwargs):
        """Variabele terms contains a list with supplied parameters.

        - hosts    -> The server addresses 
        - devices  -> The F5 device list from which the active device is selected
        """
        # Sufficient parameters
        if len(terms) < 2:
            raise AnsibleError(
                "Insufficient parameters. Need at least: hosts, devices."
            )

        # Get the parameters
        hosts = terms[0]
        devices = terms[1]

        if not isinstance(hosts, str):
            raise AnsibleError("Input 'hosts' must be a string")
        hostlist = [host.strip() for host in hosts.split(',')]
        if not len(hostlist) == 2:
            raise AnsibleError("Input 'hosts' must be a comma separated list of 2 hosts")

        if not isinstance(devices, list):
            raise AnsibleError("Input 'devices' must be a list")
        if not len(devices) == 2:
            raise AnsibleError("Input 'devices' should be list of 2 device objects")
        for device in devices:
            if not isinstance(device, dict) or not device.get("management_address", None) or not device.get("failover_state", None):
                raise AnsibleError("All input devices in the 'devices' list must be a valid f5 device object")
        device_addresses = [device.get("management_address") for device in devices]
        if set(device_addresses) != set(hostlist):
            raise AnsibleError("Listed device addresses do not match input addresses")
        
        for device in devices:
            if device.get("failover_state").lower() == "active":
                result = {
                    "address": device.get("management_address"),
                    "device": device
                }
                return result

        raise AnsibleError("No active address found")
