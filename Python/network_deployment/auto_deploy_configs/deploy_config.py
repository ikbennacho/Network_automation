from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_napalm.plugins.tasks import napalm_configure
from jinja2 import Environment, FileSystemLoader
import yaml

# Initialize Nornir
nr = InitNornir(config_file="nornir_config.yaml")

# Load Jinja2 template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("csw_config.j2")

# Load configuration data from YAML
with open("config_data/config.yaml") as f:
    devices_config = yaml.safe_load(f)

def deploy_config(task: Task) -> Result:
    # Deploy configuration using NAPALM
    result = task.run(task=napalm_configure, configuration=config)
    return Result(host=task.host, result=result.result)

for device in devices_config:
    sw_conf = device['hostname'] + '_config.txt'
    with open(sw_conf, 'w') as f:
        f.write(template.render(device))
    
    # Render configuration
    config = template.render(device)

# Run the task on all devices
result = nr.run(task=deploy_config)  

