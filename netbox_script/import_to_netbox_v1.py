from scrapli.driver.core import EOSDriver
from ntc_templates.parse import parse_output
from nb_endpoints import get_from_netbox, create_in_netbox, update_in_netbox
import pynetbox
import json


CMDS = [
    ("show hostname", "arista_eos_show_hostname"),
    ("show version", "arista_eos_show_version"),
    ("show inventory", "arista_eos_show_inventory"),
    ("show interface", "arista_eos_show_interface"),
]       

def get_devive_facts(device_creds):
    with EOSDriver(**device_creds) as conn:
        facts = {}
        # template needs to bedeclared for parse_output to work   
        for cmd, template in CMDS:
            output = conn.send_command(cmd).result
            parsed = parse_output(platform="arista_eos", command=cmd, data=output)
            facts[cmd] = parsed
        return facts

def build_netbox_payload(parsed):
    hostname = parsed["show hostname"][0].get("hostname", "unknown")
    interfaces = parsed["show interface"]
    serial = parsed["show version"][0].get("serial_number", "unknown")
    device_type = parsed["show version"][0].get("model", "unknown")

    device = {
        "name": hostname,
        "device_type": device_type.lower(),
        "device_role": "l3-switch",  
        "platform": "arista_eos",
        "site": "test-site2",
        "status": "active",
        "serial_number": serial
    }

    iface_list = []
    ip_list = []
    for iface in interfaces:
        name = iface.get("interface")
        if not name:
            continue
        iface_list.append({
            "name": name,
            "enabled": iface.get("link_status", "up") == "up",
            "description": iface.get("description", "")
        })
        ip = iface.get("ip_address")
        if ip:
            ip_list.append({
                "address": ip,
                "assigned_object": name
            })

    return {
        "device": device,
        "interfaces": iface_list,
        "ip_addresses": ip_list
    }
    
def main():
        # Connect to the device and collect facts
        print("Collecting device facts...")
        my_device = {
        "host": "172.100.100.13",
        "auth_username": "admin",
        "auth_password": "admin",
        "auth_strict_key": False,
        }
            
        device_facts = get_devive_facts(my_device)
        netbox_payload = build_netbox_payload(device_facts)
        print(json.dumps(netbox_payload, indent=4))

if __name__ == "__main__":
    main()