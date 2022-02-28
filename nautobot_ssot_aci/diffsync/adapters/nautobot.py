"""Diffsync Adapter for Nautobot."""

import logging
from diffsync import DiffSync
from nautobot.tenancy.models import Tenant
from nautobot.dcim.models import DeviceType, DeviceRole, Device, InterfaceTemplate, Interface
from nautobot.ipam.models import IPAddress, Prefix
from nautobot_ssot_aci.diffsync.models import NautobotTenant
from nautobot_ssot_aci.diffsync.models import NautobotDeviceType
from nautobot_ssot_aci.diffsync.models import NautobotDeviceRole
from nautobot_ssot_aci.diffsync.models import NautobotDevice
from nautobot_ssot_aci.diffsync.models import NautobotInterfaceTemplate
from nautobot_ssot_aci.diffsync.models import NautobotInterface
from nautobot_ssot_aci.diffsync.models import NautobotIPAddress
from nautobot_ssot_aci.diffsync.models import NautobotPrefix


logger = logging.getLogger("rq.worker")


class NautobotAdapter(DiffSync):
    """Nautobot adapter for DiffSync."""

    tenant = NautobotTenant
    device_type = NautobotDeviceType
    device_role = NautobotDeviceRole
    device = NautobotDevice
    interface_template = NautobotInterfaceTemplate
    interface = NautobotInterface
    ip_address = NautobotIPAddress
    prefix = NautobotPrefix

    top_level = [
        "tenant",
        "device_type",
        "device_role",
        "interface_template",
        "device",
        "prefix",
        "ip_address",
        "interface",
    ]

    def __init__(self, *args, job=None, sync=None, **kwargs):
        """Initialize Nautobot.

        Args:
            job (object, optional): Nautobot job. Defaults to None.
            sync (object, optional): Nautobot DiffSync. Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self.job = job
        self.sync = sync

    def load_tenants(self):
        """Method to load Tenants from Nautobot."""
        for nbtenant in Tenant.objects.all():
            _tenant = self.tenant(
                name=nbtenant.name,
                description=nbtenant.description,
                comments=nbtenant.comments,
            )
            self.add(_tenant)

    def load_devicetypes(self):
        """Method to load Device Types from Nautobot."""
        for nbdevicetype in DeviceType.objects.all():
            _devicetype = self.device_type(
                model=nbdevicetype.model,
                part_nbr=nbdevicetype.part_number,
                manufacturer=nbdevicetype.manufacturer.name,
                comments=nbdevicetype.comments,
                u_height=nbdevicetype.u_height,
            )

            self.add(_devicetype)

    def load_interfacetemplates(self):
        """Method to load Interface Templates from Nautobot."""
        for nbinterfacetemplate in InterfaceTemplate.objects.all():
            _interfacetemplate = self.interface_template(
                name=nbinterfacetemplate.name,
                device_type=nbinterfacetemplate.device_type.model,
                type=nbinterfacetemplate.type,
                mgmt_only=nbinterfacetemplate.mgmt_only,
                description=nbinterfacetemplate.description,
            )
            self.add(_interfacetemplate)

    def load_interfaces(self):
        """Method to load Interfaces from Nautobot."""
        for nbinterface in Interface.objects.all():
            _interface = self.interface(
                name=nbinterface.name, device=nbinterface.device.name, description=nbinterface.description
            )
            self.add(_interface)

    def load_deviceroles(self):
        """Method to load Device Roles from Nautobot."""
        for nbdevicerole in DeviceRole.objects.all():
            _devicerole = self.device_role(name=nbdevicerole.name, description=nbdevicerole.description)
            self.add(_devicerole)

    def load_devices(self):
        """Method to load Devices from Nautobot."""
        for nbdevice in Device.objects.all():
            _device = self.device(
                name=nbdevice.name,
                device_type=nbdevice.device_type.model,
                device_role=nbdevice.device_role.name,
                serial=nbdevice.serial,
                comments=nbdevice.comments,
                node_id=nbdevice.custom_field_data["node-id"],
            )
            self.add(_device)

    def load_ipaddresses(self):
        """Method to load IPAddress objects from Nautobot."""
        for nbipaddr in IPAddress.objects.all():
            if nbipaddr.assigned_object:
                device_name = nbipaddr.assigned_object.parent.name
                interface_name = nbipaddr.assigned_object.name
            else:
                device_name = None
                interface_name = None
            if nbipaddr.tenant:
                tenant_name = nbipaddr.tenant.name
            else:
                tenant_name = None
            _ipaddress = self.ip_address(
                address=str(nbipaddr.address),
                status=nbipaddr.status.name,
                description=nbipaddr.description,
                tenant=tenant_name,
                device=device_name,
                interface=interface_name,
            )
            self.add(_ipaddress)

    def load_prefixes(self):
        """Method to load Prefix objects from Nautobot."""
        for nbprefix in Prefix.objects.all():
            _prefix = self.prefix(
                prefix=str(nbprefix.prefix),
                status=nbprefix.status.name,
                description=nbprefix.description,
                tenant=nbprefix.tenant.name,
            )
            self.add(_prefix)

    def load(self):
        """Method to load models with data from Nautbot."""
        self.load_tenants()
        self.load_deviceroles()
        self.load_devicetypes()
        self.load_interfacetemplates()
        self.load_devices()
        self.load_prefixes()
        self.load_ipaddresses()
        self.load_interfaces()
