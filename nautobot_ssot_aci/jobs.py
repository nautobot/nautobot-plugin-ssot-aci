"""Jobs for ACI SSoT plugin."""
from distutils.util import strtobool
from django.templatetags.static import static
from django.urls import reverse
from nautobot.extras.jobs import BooleanVar, ChoiceVar, Job
from nautobot_ssot.jobs.base import DataMapping, DataSource
from diffsync import DiffSyncFlags
from diffsync.exceptions import ObjectNotCreated
from nautobot_ssot_aci.diffsync.adapters.aci import AciAdapter
from nautobot_ssot_aci.diffsync.adapters.nautobot import NautobotAdapter
from nautobot_ssot_aci.constant import PLUGIN_CFG

name = "Cisco ACI SSoT"  # pylint: disable=invalid-name, abstract-method

aci_creds = {}
for key in PLUGIN_CFG["apics"]:
    subkey = key[key.rfind("_") + 1 :].lower()  # noqa: E203
    aci_creds.setdefault(subkey, {})
    if "USERNAME" in key:
        aci_creds[subkey]["username"] = PLUGIN_CFG["apics"][key]
    if "PASSWORD" in key:
        aci_creds[subkey]["password"] = PLUGIN_CFG["apics"][key]
    if "URI" in key:
        aci_creds[subkey]["base_uri"] = PLUGIN_CFG["apics"][key]
    if "VERIFY" in key:
        aci_creds[subkey]["verify"] = bool(strtobool(PLUGIN_CFG["apics"][key]))
    if "SITE" in key:
        aci_creds[subkey]["site"] = PLUGIN_CFG["apics"][key]
    if "STAGE" in key:
        aci_creds[subkey]["stage"] = PLUGIN_CFG["apics"][key]
    if "TENANT" in key:
        aci_creds[subkey]["tenant_prefix"] = PLUGIN_CFG["apics"][key]


class AciDataSource(DataSource, Job):  # pylint: disable=abstract-method
    """ACI SSoT Data Source."""

    apic_choices = [(key, key) for key in aci_creds]

    apic = ChoiceVar(choices=apic_choices, label="Select APIC")

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
            DataMapping("Interface", None, "Interface", reverse("dcim:interface_list")),
            DataMapping("VRF", None, "VRF", reverse("ipam:vrf_list")),
        )

    def sync_data(self):
        """Method to handle synchronization of data to Nautobot."""
        apic = self.kwargs["apic"]
        self.log_info(message=f"Connecting to APIC {apic} ")
        aci_adapter = AciAdapter(job=self, sync=self.sync, client=aci_creds[apic])
        self.log_info(message=f"Loading data from APIC {apic} ")
        aci_adapter.load()
        self.log_info(message="Connecting to Nautobot...")
        nb_adapter = NautobotAdapter(job=self, sync=self.sync, client=aci_creds[apic])
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
