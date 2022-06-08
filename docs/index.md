# Nautobot SSoT ACI - Nautobot plugin for synchronizing with Cisco ACI

Nautobot SSoT ACI is a plugin for [Nautobot](https://github.com/nautobot/nautobot) allowing synchronization of data from Cisco ACI into Nautobot.

This plugin is built on top of the [Nautobot Single Source of Truth (SSoT)](https://github.com/nautobot/nautobot-plugin-ssot) plugin. SSoT plugin enables Nautobot to be the aggregation point for data coming from multiple systems of record (SoR).

To accomplish the synchronization of data, the SSoT ACI plugin communicates with the Cisco ACI controller, the Application Policy Infrastructure Controller (APIC). The APIC provides a central point of administration for the ACI fabric via a web dashboard or REST API.

The SSoT ACI plugin eliminates the need for manually adding objects to Nautobot that have been automatically discovered by the Cisco APIC controller.  This includes information such as device model/serial numbers, node management IP addressing, and more.

In addition any changes to the ACI fabric are reflected in Nautobot when the synchronization process is executed.

Examples of ACI changes synchronized into Nautobot:

- New devices that were registered to the fabric are added to Nautobot.
- Devices decommissioned from the fabric are removed from Nautobot.
- Management IP addresses of devices added to the ACI fabric are created in Nautobot.
- Subnets and gateway addresses of bridge domains created in ACI are added to Nautobot as prefixes and IP addresses.
- Prefixes and IP addresses associated with removed ACI bridge domains are deleted from Nautobot.
- ACI interface description additions and updates are carried over to interface descriptions in Nautobot.

The below list shows object types that are currently synchronized and how they map between systems.

| **ACI**                                       	| **Nautobot**                  	|
|-----------------------------------------------	|-------------------------------	|
| Tenant                                        	| Tenant                        	|
| Node (Leaf/Spine/Controller)                  	| Device                        	|
| Model                                         	| Device Type                   	|
| Management IP address (Leaf/Spine/Controller) 	| IP Address                    	|
| Bridge Domain Subnet                          	| Prefix, IP Address              |
| Interfaces                                    	| Interface 	                    |
| VRFs                                            | VRFs                            |

## Contributing

Pull requests are welcomed and automatically built and tested against multiple versions of Python and multiple versions of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.


## Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)
