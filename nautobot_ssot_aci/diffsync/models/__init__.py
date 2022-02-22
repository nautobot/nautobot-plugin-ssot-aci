"""Initialize models for Nautobot and ACI."""
from .nautobot import NautobotTenant, NautobotDevice, NautobotDeviceRole, NautobotDeviceType, NautobotInterfaceTemplate, NautobotInterface, NautobotPrefix, NautobotIPAddress

__all__ = [
    "NautobotTenant", "NautobotDevice", "NautobotDeviceRole", "NautobotDeviceType", "NautobotInterfaceTemplate", "NautobotInterface", "NautobotPrefix", "NautobotIPAddress"
]