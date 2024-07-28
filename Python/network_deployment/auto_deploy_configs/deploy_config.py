from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_napalm.plugins.tasks import napalm_configure
from jinja2 import Environment, FileSystemLoader
import yaml

# Initialize Nornir
nr = InitNornir(config_file="nornir_config.yaml")

# Load configuration data from YAML
with open("config_data/config.yaml") as f:
    config_data = yaml.safe_load(f)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("csw_config.j2")

# Render configuration
config = template.render(config_data)

def deploy_config(task: Task) -> Result:
    # Deploy configuration using NAPALM
    result = task.run(task=napalm_configure, configuration=config)
    return Result(host=task.host, result=result.result)

# Run the task on all devices
result = nr.run(task=deploy_config)

# Print the results
for host, host_result in result.items():
    print(f"Host: {host}")
    print(host_result[1].result)