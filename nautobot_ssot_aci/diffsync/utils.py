"""ACI Utilities."""
import logging
import re
import yaml

logger = logging.getLogger("rq.worker")

def tenant_from_dn(dn):
    """Match an ACI tenant in the Distiguished Name (DN)."""
    pattern = "tn-[A-Za-z0-9\-]+"  # noqa: W605  # pylint: disable=anomalous-backslash-in-string
    return re.search(pattern, dn).group().replace("tn-", "").rstrip("/")


def ap_from_dn(dn):
    """Match an ACI Application Profile in the Distinguished Name (DN)."""
    pattern = "ap-[A-Za-z0-9\-]+"  # noqa: W605 # pylint: disable=anomalous-backslash-in-string
    return re.search(pattern, dn).group().replace("ap-", "").rstrip("/")

def load_yamlfile(filename):
    """Load a YAML file to a Dict."""
    with open(filename, "r") as fn:
        yaml_file = yaml.safe_load(fn)
    return yaml_file