# Plugin nautobot-ssot-aci

TODO: Write plugin documentation, the outline here is provided as a guide and should be expanded upon.  If more detail is required you are encouraged to expand on the table of contents (TOC) in `mkdocs.yml` to add additional pages.

This Single Source of Truth (SSoT) Plugin for [Nautobot](https://github.com/nautobot/nautobot) provides the ability to synchronize objects from a Cisco ACI fabric to Nautobot. It eliminates the need to manually enter information in Nautobot that is present in the Cisco APIC controller, such as device model/serial numbers, Leaf/Spine/Controller IP addressing, and more. Below is the list of items that are currently synchronized:

| **ACI**                                       	| **Nautobot**                  	|
|-----------------------------------------------	|-------------------------------	|
| Tenant                                        	| Tenant                        	|
| Node Type (Leaf/Spine/Controller/FEX)            	| Device Role                   	|
| Node (Leaf/Spine/Controller/FEX)                 	| Device                        	|
| Model                                         	| Device Type                   	|
| Management IP address (Leaf/Spine/Controller) 	| IP Address                    	|
| Bridge Domain Subnet                          	| Prefix, IP Address                |
| Interfaces                                    	| Interface Template, Interface 	|
|

## Screenshots
![image](https://user-images.githubusercontent.com/6945229/155608142-c1882882-4706-4af4-bc60-524c88f0bf48.png)
![image](https://user-images.githubusercontent.com/6945229/155608556-22eade64-8289-4e20-82a4-e2f4e15809f4.png)
![image](https://user-images.githubusercontent.com/6945229/155609055-1d93335b-53b1-4fd8-bf1b-58d64b970f1e.png)
![image](https://user-images.githubusercontent.com/6945229/155609222-c720f23f-4af8-4659-a5af-83bc69466d07.png)
![image](https://user-images.githubusercontent.com/6945229/155609612-34bdcfea-bde2-4924-8de0-3cf74796d744.png)
![image](https://user-images.githubusercontent.com/6945229/155609826-d3938767-6287-4626-94a3-aea4fd758204.png)
![image](https://user-images.githubusercontent.com/6945229/155610226-799c79de-719b-44af-9a07-2aaabfea5510.png)


## Description

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

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
```python
PLUGINS_CONFIG = {
    "nautobot_ssot_aci": {
        # URL and credentials should be configured as environment variables on the host system
        'aci_url': os.getenv("NAUTOBOT_ACI_URL"),
        'aci_username': os.getenv("NAUTOBOT_ACI_USERNAME"),
        'aci_password': os.getenv("NAUTOBOT_ACI_PASSWORD"),
        'aci_verify': os.getenv("NAUTOBOT_ACI_VERIFY_SSL"),
        # Tag which will be created and applied to all synchronized objects.
        'tag': 'NTC_ACI',
        'tag_color': 'FF3333',
        # Manufacturer name. Specify existing, or a new one with this name will be created.
        'manufacturer_name': 'Cisco',
        # Exclude any tenants you would not like to bring over from ACI.
        'ignore_tenants': ['common', 'mgmt', 'infra'],
        # Enter a prefix to be prepended to the tenant, for example the name of the ACI fabric.
        # A prefix to append to the front of a tenant name.  Set to None if no prefix is desired. 
        'tenant_prefix': 'ntc_aci',
        # The below value will appear in the Comments field on objects created in Nautobot
        'comments': 'Created by ACI SSoT Plugin',
        # Site to associate objects. Specify existing, or a new site with this name will be created.
        'site': 'Data Center'
    }
}
```

Some of the above settings can be omitted, and if omitted the below defaults will take effect:
```python
default_settings = {'tag': 'ACI',
                        'tag_color': 'FF3333',
                        'manufacturer_name': 'Cisco',
                        'site': 'Data Center'
                        }
                        
```
The APIC URL and credentials should be created as environment variables on the host system, for example:

```bash
export NAUTOBOT_ACI_URL="https://aci.cloud.networktocode.com"
export NAUTOBOT_ACI_USERNAME="admin"
export NAUTOBOT_ACI_PASSWORD="not_so_secret_password"
export NAUTOBOT_ACI_VERIFY_SSL="False"
```
> Alternatively, if using the [Docker Development Environment](#docker), the URL and credentials should be defined in `development/creds.env`.  See the example in `development\creds.example.env`.  
## Configuration

## Usage

## API

## Views

## Models
