## Installation and Configuration

The plugin is available as a Python package in PyPI and can be installed with pip

```shell
pip install nautobot-ssot-aci
```

> The plugin is compatible with Nautobot 1.2.0 and higher

To ensure Nautobot SSoT for Cisco ACI is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-ssot-aci` package:

```no-highlight
# echo nautobot-ssot-aci >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your `nautobot_config.py`

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_ssot_aci"]
```

In addition, the plugin behavior can be controlled with the following list of settings.

| Setting Name<br>(* required) | Type | Example | Description |
|---|:---:|---|---|
| apics* | _Environment<br>Variable_ | `export NAUTOBOT_APIC_BASE_URI_NTC='https://apic.networktocode.com'` | URL and Credentials configured as environment <br>variables on the host system. |
| tag* | _String_ | `"tag": "ACI"` | Tag which is created and applied to all <br>synchronized objects. |
| tag_color* | _String_ | `"tag_color": "0047AB"` | Hex color code used for the tag. |
| tag_up* | _String_ | `"tag_up": "UP"` | Tag indicating the state applied to synchronized <br>interfaces. |
| tag_up_color* | _String_ | `"tag_up_color": "008000"` | Tag color applied to the "UP" tag on interface <br>status. |
| tag_down* | _String_ | `"tag_down": "DOWN"` | Tag indicating the state applied to synchronized <br>interfaces. |
| tag_down_color* | _String_ | `"tag_down_color": "FF3333"` | Tag color applied to the "DOWN" tag on interface <br>status. |
| manufacturer_name* | _String_ | `"manufacturer_name": "Cisco"` | Manufacturer name. Specifically existing, or a new <br>one with this name will be created. |
| ignore_tenants* | _List[String]_ | `"ignore_tenants": ["common", "mgmt", "infra"]` | List of ACI Tenants that should not be synchronized<br>from APIC. |
| comments* | _String_ | `"comments": "Created by ACI SSoT Plugin"` | Comment added to synchronized objects. |

```python
PLUGINS_CONFIG = {
    "nautobot_ssot": {
        "hide_example_jobs": True,
    },
    "nautobot_ssot_aci": {
        # URL and credentials should be configured as environment variables on the host system
        "apics": {x: os.environ[x] for x in os.environ if "APIC" in x},
        # Tag which will be created and applied to all synchronized objects.
        "tag": "ACI",
        "tag_color": "0047AB",
        # Tags indicating state applied to synchronized interfaces.
        "tag_up": "UP",
        "tag_up_color": "008000",
        "tag_down": "DOWN",
        "tag_down_color": "FF3333",
        # Manufacturer name. Specify existing, or a new one with this name will be created.
        "manufacturer_name": "Cisco",
        # Exclude any tenants you would not like to bring over from ACI.
        "ignore_tenants": ["common", "mgmt", "infra"],
        # The below value will appear in the Comments field on objects created in Nautobot
        "comments": "Created by ACI SSoT Plugin",
    }
```

Some of the above settings can be omitted, and if omitted the below defaults will take effect:
```python
default_settings = {"tag": "ACI",
                   "tag_color": "FF3333",
                   "manufacturer_name": "Cisco",
                   }                    
```

The APIC URL and credentials should be created as environment variables on the host system. 

Multiple APIC instances can be configured for synchronization and this is achieved by using a `_` character and identifier appended to  the names of environment variables. In the example below this APIC will be called `NTC`.  Instead of `NTC` you could, for example,  use   `CHCG01` to identify an APIC instance in your Chicago facility.


```bash
export NAUTOBOT_APIC_BASE_URI_NTC=https://aci.cloud.networktocode.com
export NAUTOBOT_APIC_USERNAME_NTC=admin
export NAUTOBOT_APIC_PASSWORD_NTC=not_so_secret_password
export NAUTOBOT_APIC_VERIFY_NTC=False
export NAUTOBOT_APIC_SITE_NTC="NTC ACI"
export NAUTOBOT_APIC_TENANT_PREFIX_NTC="NTC_ACI"
```

Each environment variable above contains the string `NTC` at the end, which serves as an identifier for the APIC. This can be any string of characters that you would like to use to identify the APIC in your environment. The identifier is used to select APIC from the SSoT dashboard when initiating a synchronization job:

![image](https://user-images.githubusercontent.com/6945229/162986635-fd537a5f-9fa1-4a82-95fa-af60fa07d6c2.png)

### Nautobot Objects Affected by Settings

A Site will be created in Nautobot with the name specified in the `NAUTOBOT_APIC_SITE` environment variable and resources created by the plugin will be assigned to this site. 

Tenants imported from ACI will be prepended with the unique name specified by the corresponding `TENANT_PREFIX` variable. This uniquely identifies tenants which might have the same name, but belong to two different APIC clusters. 

### Configuring Device Templates

In order to create a new Device Type in Nautobot that maps to a specific model of ACI leaf or spine switch, a `YAML` file needs to be provided for that model. This allows the SSoT plugin to create a Device Type, including an Interface Template that has the ports and transceiver types (ex. 10GE SFP+) as specified in the YAML file.  The files should be placed in `nautobot_ssot_aci/diffsync/device-types`, and should match the model name as it appears in the ACI  Fabric Membership area of the APIC dashboard.  For example,  given a Model name of `N9K-C9396PX` as shown below,  the YAML file should be named `N9K-C9396PX.yaml`.  

![APIC Fabric Dashboard](https://user-images.githubusercontent.com/6945229/156404496-b3f570aa-fa6b-40bc-9cfc-dcaaff55f459.png)

There are examples of YAML files for a few common switch models in `nautobot_ssot_aci/diffsync/device-types`,  and several additional can be downloaded [here](https://github.com/netbox-community/devicetype-library/tree/master/device-types/Cisco). 
