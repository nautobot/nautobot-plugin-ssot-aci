"""Jobs for ACI SSoT plugin."""

from django.templatetags.static import static
from django.urls import reverse
from nautobot.extras.jobs import BooleanVar, Job
from nautobot_ssot.jobs.base import DataMapping, DataSource
from nautobot_ssot_aci.diffsync.adapters.aci import AciAdapter
from nautobot_ssot_aci.diffsync.adapters.nautobot import NautobotAdapter
from diffsync import DiffSyncFlags
from diffsync.exceptions import ObjectNotCreated

name = "Cisco ACI SSoT"  # pylint: disable=invalid-name

class AciDataSource(DataSource, Job):
    """ACI SSoT Data Source."""

    debug = BooleanVar(description="Enable for verbose debug logging.")

    class Meta:  # pylint: disable=too-few-public-methods
        """Information about the Job."""

        name = "Cisco ACI Data Source"
        data_source = "ACI"
        data_source_icon = static("nautobot_ssot_aci/aci.png")
        description = "Sync information from ACI to Nautobot"

    @classmethod
    def data_mappings(cls):
        """Shows mapping of models between ACI and Nautobot."""
        return (
            DataMapping("Tenant", None, "Tenant", reverse("tenancy:tenant_list")),
            DataMapping("Node Type", None, "Device Role", reverse("dcim:devicerole_list")),
            DataMapping("Node", None, "Device", reverse("dcim:device_list")),
            DataMapping("Model", None, "Device Type", reverse("dcim:devicetype_list")),
            DataMapping("Controller/Leaf/Spine OOB Mgmt IP", None, "IP Address", reverse("ipam:ipaddress_list")),
            DataMapping("Subnet", None, "Prefix", reverse("ipam:prefix_list")),
            DataMapping("Interface", None, "Interface", reverse("dcim:interface_list"))
        )

    def sync_data(self):
        """Method to handle synchronization of data to Nautobot."""
        self.log_info(message="Connecting to ACI")
        aci_adapter = AciAdapter(job=self, sync=self.sync)
        self.log_info(message="Loading data from ACI...")
        aci_adapter.load()
        self.log_info(message="Connecting to Nautobot...")
        nb_adapter = NautobotAdapter(job=self, sync=self.sync)
        self.log_info(message="Loading data from Nautobot...")
        nb_adapter.load()
        self.log_info(message="Performing diff of data between ACI and Nautobot.")
        flags = DiffSyncFlags.CONTINUE_ON_FAILURE
        # Below flag prevents deletion of objects that exist in Nautobot, but not ACI.
        flags |= DiffSyncFlags.SKIP_UNMATCHED_DST
        diff = nb_adapter.diff_from(aci_adapter, flags=flags)
        self.sync.diff = diff.dict()
        self.sync.save()
        self.log_info(message=diff.summary())
        if not self.kwargs["dry_run"]:
            self.log_info(message="Performing data synchronization from ACI to Nautobot.")
            try:
                nb_adapter.sync_from(aci_adapter, flags=flags)
            except ObjectNotCreated as err:
                self.log_debug(f"Unable to create object. {err}")
            self.log_success(message="Sync complete.")

jobs = [AciDataSource]

