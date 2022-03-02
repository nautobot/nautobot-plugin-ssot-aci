# Nautobot SSoT for Cisco ACI

This Single Source of Truth (SSoT) Plugin for [Nautobot](https://github.com/nautobot/nautobot) provides the ability to synchronize objects from a Cisco ACI fabric to Nautobot. It eliminates the need to manually enter information in Nautobot that is present in the Cisco APIC controller, such as device model/serial numbers, Leaf/Spine/Controller IP addressing, and more. Below is the list of items that are currently synchronized:

| **ACI**                                       	| **Nautobot**                  	|
|-----------------------------------------------	|-------------------------------	|
| Tenant                                        	| Tenant                        	|
| Node Type (Leaf/Spine/Controller)             	| Device Role                   	|
| Node (Leaf/Spine/Controller)                  	| Device                        	|
| Model                                         	| Device Type                   	|
| Management IP address (Leaf/Spine/Controller) 	| IP Address                    	|
| Bridge Domain Subnet                          	| Prefix, IP Address              |
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

### Device Templates
In order to create a new Device Type in Nautobot that maps to a specific model of ACI leaf or spine switch, a `YAML` file needs to be provided for that model. This allows the SSoT plugin to create a Device Type, including an Interface Template that has the ports and tranceiver types (ex. 10GE SFP+) as specified in the YAML file.  The files should be placed in `nautobot_ssot_aci/diffsync/device-types`, and should be named as the model information would appear in the ACI Fabric Membership area of the APIC dashboard.  For example,  given a Model name of `N9K-C9396PX` as shown below,  the YAML file should be named `N9K-C9396PX.yaml`.  

![image](https://user-images.githubusercontent.com/6945229/156404496-b3f570aa-fa6b-40bc-9cfc-dcaaff55f459.png)

There are already YAML files for a few common switch models in `nautobot_ssot_aci/diffsync/device-types`,  and several additional can be downloaded [here](https://github.com/netbox-community/devicetype-library/tree/master/device-types/Cisco). 


## Usage
The plugin can be used by navigating to **Plugins > Dashboard** in Nautobot.  Then click on **Cisco ACI Data Source**.
![image](https://user-images.githubusercontent.com/6945229/155611179-8d39b79b-8c35-4a74-a871-2ebbc36a2b94.png)
 
From the **Cisco ACI Data Source** page, you can view historical synchronization jobs, or click **Sync Now** to begin a synchronization job. 

![image](https://user-images.githubusercontent.com/6945229/155611423-ad0381f0-7877-491f-b5ac-fb725f9c8150.png)

On the next page, you can select whether you would like to do a dry-run as well as schedule when you would like the job to run.  With a dry-run, you can see what information will be brought from ACI into Nautobot without actually performing the synchronization. The job can be run immediately, scheduled to run at a later date/time, or configured to run hourly, daily, or weekly at a specified date/time. 

![image](https://user-images.githubusercontent.com/6945229/155612395-afca143d-1805-414b-a3c6-9f59566ba46a.png)

Once you click **Run Job Now**, you will see the logs as the job progresses. When finished, you can click the **SSoT Sync Details** button to view the changes (or proposed changes, in case of a dry run).  

![image](https://user-images.githubusercontent.com/6945229/155612666-5488e5a3-92cb-44f1-af9b-83a6cb55b379.png)

![image](https://user-images.githubusercontent.com/6945229/155613017-74163984-ba88-4cb3-a1ce-0fd2430a75ee.png)

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

### Development Environment

The development environment can be used in 2 ways. First, with a local poetry environment if you wish to develop outside of Docker with the caveat of using external services provided by Docker for PostgresQL and Redis. Second, all services are spun up using Docker and a local mount so you can develop locally, but Nautobot is spun up within the Docker container.

Below is a quick start guide if you're already familiar with the development environment provided, but if you're not familiar, please read the [Getting Started Guide](GETTING_STARTED.md).

#### Invoke

The [PyInvoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment.  There are a few configuration parameters which can be passed to PyInvoke to override the default configuration:

* `nautobot_ver`: the version of Nautobot to use as a base for any built docker containers (default: 1.1.4)
* `project_name`: the default docker compose project name (default: nautobot_ssot_aci)
* `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.6)
* `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers)
* `compose_dir`: the full path to a directory containing the project compose files
* `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information)

Using **PyInvoke** these configuration options can be overridden using [several methods](http://docs.pyinvoke.org/en/stable/concepts/configuration.html).  Perhaps the simplest is simply setting an environment variable `INVOKE_NAUTOBOT_SSOT_ACI_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override.  The only exception is `compose_files`, because it is a list it must be overridden in a yaml file.  There is an example `invoke.yml` (`invoke.example.yml`) in this directory which can be used as a starting point.

#### Local Poetry Development Environment

1. Copy `development/creds.example.env` to `development/creds.env` (This file will be ignored by Git and Docker)
2. Uncomment the `POSTGRES_HOST`, `REDIS_HOST`, and `NAUTOBOT_ROOT` variables in `development/creds.env`
3. Create an `invoke.yml` file with the following contents at the root of the repo (you can also `cp invoke.example.yml invoke.yml` and edit as necessary):

```yaml
---
nautobot_ssot_aci:
  local: true
  compose_files:
    - "docker-compose.requirements.yml"
```

3. Run the following commands:

```shell
poetry shell
poetry install --extras nautobot
export $(cat development/dev.env | xargs)
export $(cat development/creds.env | xargs) 
invoke start && sleep 5
nautobot-server migrate
```

> If you want to develop on the latest develop branch of Nautobot, run the following command: `poetry add --optional git+https://github.com/nautobot/nautobot@develop`. After the `@` symbol must match either a branch or a tag.

4. You can now run nautobot-server commands as you would from the [Nautobot documentation](https://nautobot.readthedocs.io/en/latest/) for example to start the development server:

```shell
nautobot-server runserver 0.0.0.0:8080 --insecure
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

It is typically recommended to launch the Nautobot **runserver** command in a separate shell so you can keep developing and manage the webserver separately.

#### <a name="docker"></a>Docker Development Environment

This project is managed by [Python Poetry](https://python-poetry.org/) and has a few requirements to setup your development environment:

1. Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2. Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.

Once you have Poetry and Docker installed you can run the following commands to install all other development dependencies in an isolated python virtual environment:

```shell
poetry shell
poetry install
invoke start
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

To either stop or destroy the development environment use the following options.

- **invoke stop** - Stop the containers, but keep all underlying systems intact
- **invoke destroy** - Stop and remove all containers, volumes, etc. (This results in data loss due to the volume being deleted)

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`.

Each command can be executed with `invoke <command>`. Environment variables `INVOKE_NAUTOBOT_SSOT_ACI_PYTHON_VER` and `INVOKE_NAUTOBOT_SSOT_ACI_NAUTOBOT_VER` may be specified to override the default versions. Each command also has its own help `invoke <command> --help`

#### Docker dev environment

```no-highlight
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart Nautobot and its dependencies.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

#### Utility

```no-highlight
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
  shell-plus       Launch a shell_plus session, which uses iPython and automatically imports all models.
```

#### Testing

```no-highlight
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           This will run flake8 for the specified name and Python version.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

### Project Documentation

Project documentation is generated by [mkdocs](https://www.mkdocs.org/) from the documentation located in the docs folder.  You can configure [readthedocs.io](https://readthedocs.io/) to point at this folder in your repo.  A container hosting the docs will be started using the invoke commands on [http://localhost:8001](http://localhost:8001), as changes are saved the docs will be automatically reloaded.

## Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)

