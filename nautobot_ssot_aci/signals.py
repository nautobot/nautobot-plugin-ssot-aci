"""Post Migrate Welcome Wizard Script."""
from nautobot_ssot_aci.constant import PLUGIN_CFG

# from django.contrib.contenttypes.models import ContentType
import logging

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


def aci_create_custom_field(apps, **kwargs):
    """Add custom field NodeId."""
    cf_model = apps.get_model("extras", "CustomField")
    logger.info(f"Creating Custom Field: node-id")
    cf_model.objects.update_or_create(
        name="node-id",
        label="Node Id",
        description="Node ID pulled from ACI fabric by SSoT plugin",
        filter_logic="loose",
        weight=100,
        type="integer",
    )
    ct = apps.get_model("contenttypes", "ContentType")
    ct_obj = ct.objects.get(model="device")
    ct_obj.custom_fields.set(objs=[cf_model.objects.get(name="node-id")])
    ct_obj.save()
