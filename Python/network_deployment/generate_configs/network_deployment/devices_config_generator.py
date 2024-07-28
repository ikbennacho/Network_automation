from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('csw_config_test.j2')

with open('devices_info_test.yml') as f:
    csw = yaml.safe_load(f)

for sw in csw:
    r1_conf = sw['hostname'] + '_r1.txt'
    with open(r1_conf, 'w') as f:
        f.write(template.render(sw))