import pynetbox
import os

class NetBoxHandler:
    """
    A class to handle connections and operations with NetBox.
    """

    def __init__(self):
        self.netbox_url = os.getenv("NETBOX_URL")
        self.netbox_token = os.getenv("NETBOX_TOKEN")
        if not self.netbox_url or not self.netbox_token:
            raise ValueError("NETBOX_URL and NETBOX_TOKEN environment variables must be set.")
        self.netbox = pynetbox.api(self.netbox_url, token=self.netbox_token)

    def get_endpoint(self, endpoint_name):
        """
    Retrieve a specific endpoint from NetBox.
    """
        try:
            # Split the endpoint_name into parts (e.g., "dcim.devices" -> ["dcim", "devices"])
            parts = endpoint_name.split(".")
            endpoint = self.netbox
            for part in parts:
                endpoint = getattr(endpoint, part)
            return endpoint
        except AttributeError:
            raise ValueError(f"Endpoint '{endpoint_name}' does not exist in NetBox.")
        
    def get_from_netbox(self, endpoint_name, name):
        """
        Fetch an object from NetBox by its name.
        """
        endpoint = self.get_endpoint(endpoint_name)
        try:
            return endpoint.get(name)
        except pynetbox.RequestError as e:
            print(f"Error fetching {name} from NetBox: {e}")
            return None

    def create_in_netbox(self, endpoint_name, name, data):
        """
        Create an object in NetBox.
        """
        endpoint = self.get_endpoint(endpoint_name)
        try:
            return endpoint.create(data)
        except pynetbox.RequestError as e:
            print(f"Error creating {name} in NetBox: {e}")
            return None

    def update_in_netbox(self, endpoint_name, obj_id, data):
        """
        Update an existing object in NetBox.
        """
        endpoint = self.get_endpoint(endpoint_name)
        try:
            obj = endpoint.get(obj_id)
            if obj:
                return obj.update(data)
            else:
                print(f"Object with ID {obj_id} not found.")
                return None
        except pynetbox.RequestError as e:
            print(f"Error updating object in NetBox: {e}")
            return None
