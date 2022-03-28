"""Base Shared Models for Cisco ACI integration with SSoT plugin."""
from typing import List, Optional
from diffsync import DiffSyncModel


class Tenant(DiffSyncModel):
    """Tenant model for DiffSync."""

    _modelname = "tenant"
    _identifiers = ("name",)
    _attributes = ("description", "comments")

    name: str
    description: Optional[str]
    comments: Optional[str]


class Vrf(DiffSyncModel):
    """VRF model for DiffSync."""

    _modelname = "vrf"
    _identifiers = ("name", "tenant")
    _attributes = ("description", "rd")

    name: str
    tenant: str
    description: Optional[str]
    rd: Optional[str]


class DeviceType(DiffSyncModel):
    """DeviceType model for DiffSync."""

    _modelname = "device_type"
    _identifiers = (
        "model",
        "manufacturer",
        "part_nbr",
    )
    _attributes = (
        "comments",
        "u_height",
    )
    _children = {
        "interface_template": "interface_templates",
    }

    model: str
    manufacturer: str
    part_nbr: str
    comments: Optional[str]
    u_height: Optional[int]

    interface_templates: List["InterfaceTemplate"] = []


class DeviceRole(DiffSyncModel):
    """DeviceRole model for DiffSync."""

    _modelname = "device_role"
    _identifiers = ("name",)
    _attributes = ("description",)

    name: str
    description: Optional[str]


class Device(DiffSyncModel):
    """Device model for DiffSync."""

    _modelname = "device"
    _identifiers = (
        "name",
        "device_type",
        "device_role",
        "serial",
    )
    _attributes = ("comments", "node_id", "pod_id")
    _children = {
        "interface": "interfaces",
    }

    name: str
    device_type: str
    device_role: str
    serial: str
    comments: Optional[str]
    interfaces: List["Interface"] = []
    node_id: Optional[int]
    pod_id: Optional[int]


class InterfaceTemplate(DiffSyncModel):
    """InterfaceTemplate model for DiffSync."""

    _modelname = "interface_template"
    _identifiers = (
        "device_type",
        "name",
        "type",
    )
    _attributes = (
        "u_height",
        "description",
        "mgmt_only",
    )

    name: str
    device_type: str
    type: str
    u_height: Optional[int]
    description: Optional[str]
    mgmt_only: Optional[bool]


class IPAddress(DiffSyncModel):
    """IPAddress model for DiffSync."""

    _modelname = "ip_address"
    _identifiers = (
        "address",
        "status",
        "vrf",
        "tenant",
    )
    _attributes = (
        "description",
        "device",
        "interface",
    )

    address: str
    status: str
    vrf: str
    description: Optional[str]
    device: Optional[str]
    interface: Optional[str]
    tenant: str


class Prefix(DiffSyncModel):
    """Prefix model for DiffSync."""

    _modelname = "prefix"
    _identifiers = (
        "prefix",
        "tenant",
        "status",
    )
    _attributes = ("description", "vrf")

    prefix: str
    status: str
    tenant: str
    description: Optional[str]
    vrf: Optional[str]


class Interface(DiffSyncModel):
    """Interface model for DiffSync."""

    _modelname = "interface"
    _identifiers = (
        "name",
        "device",
    )
    _attributes = ("description", "gbic_sn", "gbic_vendor", "gbic_type", "gbic_model", "state")

    name: str
    device: str
    description: Optional[str]
    gbic_sn: Optional[str]
    gbic_vendor: Optional[str]
    gbic_type: Optional[str]
    gbic_model: Optional[str]
    state: Optional[str]
