"""Post Migrate Welcome Wizard Script."""
import logging
from nautobot.extras.choices import CustomFieldTypeChoices
from nautobot_ssot_aci.constant import PLUGIN_CFG

logger = logging.getLogger("rq.worker")


def aci_create_tag(apps, **kwargs):
    """Add a tag."""
    tag = apps.get_model("extras", "Tag")
    logger.info(f"Creating tag: {PLUGIN_CFG.get('tag')}")
    tag.objects.update_or_create(
        name=PLUGIN_CFG.get("tag"),
        slug=PLUGIN_CFG.get("tag").lower().replace(" ", "-"),
        color=PLUGIN_CFG.get("tag_color"),
    )


def aci_create_manufacturer(apps, **kwargs):
    """Add manufacturer."""
    manufacturer = apps.get_model("dcim", "Manufacturer")
    logger.info(f"Creating manufacturer: {PLUGIN_CFG.get('manufacturer_name')}")
    manufacturer.objects.update_or_create(
        name=PLUGIN_CFG.get("manufacturer_name"),
    )


def aci_create_site(apps, **kwargs):
    """Add site."""
    site = apps.get_model("dcim", "Site")
    logger.info(f"Creating Site: {PLUGIN_CFG.get('site')}")
    site.objects.update_or_create(name=PLUGIN_CFG.get("site"))


def device_custom_fields(apps, **kwargs):
    """Creating custom fields for interfaces"""
    ContentType = apps.get_model("contenttypes", "ContentType")
    Device = apps.get_model("dcim", "Device")
    CustomField = apps.get_model("extras", "CustomField")
    logger.info("Creating Device extra fields for PodID and NodeID")

    for device_cf_dict in [
        {
            "name": "pod_id",
            "type": CustomFieldTypeChoices.TYPE_INTEGER,
            "label": "Pod ID",
            "filter_logic": "loose",
            "description": "PodID added by SSoT plugin",
        },
        {
            "name": "node_id",
            "type": CustomFieldTypeChoices.TYPE_INTEGER,
            "label": "Node ID",
            "filter_logic": "loose",
            "description": "NodeID added by SSoT plugin",
        },
    ]:
        field, _ = CustomField.objects.get_or_create(name=device_cf_dict["name"], defaults=device_cf_dict)
        field.content_types.set([ContentType.objects.get_for_model(Device)])


def interface_custom_fields(apps, **kwargs):
    """Creating custom fields for interfaces"""
    ContentType = apps.get_model("contenttypes", "ContentType")
    Interface = apps.get_model("dcim", "Interface")
    CustomField = apps.get_model("extras", "CustomField")
    logger.info("Creating Interface extra fields for GBICs")

    for interface_cf_dict in [
        {
            "name": "gbic_type",
            "type": CustomFieldTypeChoices.TYPE_TEXT,
            "label": "GBIC Type",
            "filter_logic": "loose",
            "description": "GBIC type added by SSoT plugin",
        },
        {
            "name": "gbic_vendor",
            "type": CustomFieldTypeChoices.TYPE_TEXT,
            "label": "GBIC Type",
            "filter_logic": "loose",
            "description": "GBIC vendor added by SSoT plugin",
        },
        {
            "name": "gbic_sn",
            "type": CustomFieldTypeChoices.TYPE_TEXT,
            "label": "GBIC Type",
            "filter_logic": "loose",
            "description": "GBIC S/N added by SSoT plugin",
        },
    ]:
        field, _ = CustomField.objects.get_or_create(name=interface_cf_dict["name"], defaults=interface_cf_dict)
        field.content_types.set([ContentType.objects.get_for_model(Interface)])
