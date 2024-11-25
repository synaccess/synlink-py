import json
import requests
# import time

from requests_toolbelt.multipart.encoder import MultipartEncoder

__version__ = "0.0.14"

DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 0

__all__ = ['Error', 'Response', 'BaseAPI', 'Outlets', 'Inlets', 'SynLinkPy']

class Error(Exception):
    pass

class BaseAPI(object):
    def __init__(self, token=None, cookie=None, host=None, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES):
        self.token = token
        self.host = host
        self.timeout = timeout
        self.retries = retries
        self.cookie = cookie
        # self.username = username
        # self.password = password

    def get(self, resource, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token
        if self.cookie:
            kwargs.setdefault('headers', {})['Cookie'] = 'SPID=' + self.cookie

        url = self.host + "/api/" + resource
        response = requests.get(url, timeout=self.timeout, **kwargs)
        
        if not response.status_code == 200:
            raise Error(response.reason)

        return response.json()

    def put(self, resource, resource_id, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        if self.cookie:
            kwargs.setdefault('headers', {})['Cookie'] = 'SPID=' + self.cookie
        url = self.host + "/api/" + resource + '/' + resource_id
        response = requests.put(url, **kwargs)
        if not response.status_code == 200:
            if response.text:
                try:
                    error_message = response.json()
                except (KeyError, ValueError):
                    error_message = response.text
            else:
                error_message = "Error: No response received from server."
            raise Error(error_message)

        return response.json()

    def post(self, resource, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        if self.cookie:
            kwargs.setdefault('headers', {})['Cookie'] = 'SPID=' + self.cookie

        url = self.host + "/api/" + resource
        response = requests.post(url, **kwargs)

        if not response.status_code == 200:
            if response.text:
                try:
                    error_message = response.json()
                except (KeyError, ValueError):
                    error_message = response.text
            else:
                error_message = "Error: No response received from server."
            raise Error(error_message)

        # if not response.status_code == 200:
            # raise Error(response.reason)
        return response.json()

    def remove(self, resource, resource_id, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        if self.cookie:
            kwargs.setdefault('headers', {})['Cookie'] = 'SPID=' + self.cookie
        url = self.host + "/api/" + resource + '/' + resource_id
        response = requests.delete(url, **kwargs)
        if not response.status_code == 200:
            raise Error(response.reason)
        return response.text


class Outlets(BaseAPI):
    def set_state(self, outlet, state):
        """Set the state of an outlet.

        :param outlet: The outlet number or outlet ID to set.
        :param state: The state to set the outlet to. Can be "ON" or "OFF", or "REBOOT".
        :return: The response from the API.
        """
        if state != "REBOOT" and state != "ON" and state != "OFF":
            raise Error("State must be 'ON', 'OFF', or 'REBOOT'")

        data_json_string = json.dumps({"state": state})
        return self.put("outlets", str(outlet), data=data_json_string)
    
    def change_config(self, outlet, config):
        """Change the configuration of an outlet.

        :param outlet: The outlet number or outlet ID to set.
        :param config: The configuration to set the outlet to.
        :return: The response from the API.
        """
        data_json_string = json.dumps(config)
        return self.put("outlets", str(outlet), data=data_json_string)

    def list(self):
        """List all outlets.

        :return: The response from the API.
        """

        return self.get("outlets")

class Inlets(BaseAPI):
    def list(self):
        """List all inlets.

        :return: The response from the API.
        """

        return self.get("inlets")

class Banks(BaseAPI):
    def list(self):
        """List all banks.

        :return: The response from the API.
        """

        return self.get("banks")

class Device(BaseAPI):
    def info(self):
        """Get device information.

        :return: The response from the API.
        """

        return self.get("device")

class System(BaseAPI):

    def fwUpdate(self, file_path):
        """Upload firmware update file to the device and reboot.

        :param file_path: The path to the firmware file (.swu).
        :return: The response from the API.
        """
        if not self.host or not file_path:
            raise Error("Host and file path must be provided.")
        
        try:
            print("Firmware update in progress... Please do not power off. This may take a few minutes.")
            # Create the multipart form-data payload
            with open(file_path, 'rb') as file:
                form_data = MultipartEncoder(fields={'file': (file_path, file, 'application/octet-stream')})
                headers = {
                    'Content-Type': form_data.content_type
                }
                if self.token:
                    headers['Authorization'] = 'Bearer ' + self.token
                if self.cookie:
                    headers['Cookie'] = 'SPID=' + self.cookie

                # Perform the firmware update
                url = f"{self.host}/api/system/firmware"
                response = requests.post(url, data=form_data, headers=headers, timeout=480)
                if response.status_code == 200:
                    print("Firmware update successful.")
                else:
                    print("Firmware update failed.")
                    raise Error(response.text)

            # Reboot the device after firmware update
            print("Rebooting the device...")
            reboot_url = f"{self.host}/api/system/reboot"
            reboot_headers = {}
            if self.cookie:
                reboot_headers['Cookie'] = 'SPID=' + self.cookie

            reboot_response = requests.post(reboot_url, headers=reboot_headers, timeout=30)
            if reboot_response.status_code == 200:
                print("Device reboot successful.")
                return True
            else:
                print("Device reboot failed.")
                raise Error(reboot_response.text)

        except Exception as e:
            raise Error(f"Firmware update error: {str(e)}")

class Groups(BaseAPI):
    def list(self):
        """List all groups.

        :return: The response from the API.
        """

        return self.get("groups")
    def create(self, name ):
        """Create a group.
        :return: The response from the API.
        """
        data_json_string = json.dumps({"groupName": name})
        return self.post("groups", data=data_json_string)

    def modify(self, id, config):
        """Modify a group.
        modify outlets in group, change name, and/or modify sequencing time
        :return: The response from the API.
        """
        data_json_string = json.dumps(config)
        return self.put("groups", str(id), data=data_json_string)

    def delete(self, id):
        """Delete a group.
        :return: The response from the API.
        """
        return self.remove("groups", str(id))

    def set_state(self, id, state):
        """Set the state of a group.

        :param id: The group ID to set.
        :param state: The state to set the group to. Can be "ON" or "OFF", or "REBOOT".
        :return: The response from the API.
        """
        if state != "REBOOT" and state != "ON" and state != "OFF":
            raise Error("State must be 'ON', 'OFF', or 'REBOOT'")

        data_json_string = json.dumps({"state": state})
        return self.put("groups", str(id), data=data_json_string)

class Events(BaseAPI):
    def list(self):
        """List all events.

        :return: The response from the API.
        """

        return self.get("events")
    def create(self, eventObject ):
        """Create a event.
        :return: The response from the API.
        """
        data_json_string = json.dumps(eventObject)
        return self.post("events", data=data_json_string)
    def modify(self, id, eventObject):
        """Modify a event.
        :return: The response from the API.
        """
        data_json_string = json.dumps(eventObject)
        return self.put("events", str(id), data=data_json_string)
    def delete(self, id):
        """Delete a event.
        :return: The response from the API.
        """
        return self.remove("events", str(id))
    
class Actions(BaseAPI):
    def list(self):
        """List all actions.

        :return: The response from the API.
        """

        return self.get("actions")
    def create(self, actionObject ):
        """Create a action.
        :return: The response from the API.
        """
        data_json_string = json.dumps(actionObject)
        return self.post("actions", data=data_json_string)
    def modify(self, id, actionObject):
        """Modify a action.
        :return: The response from the API.
        """
        data_json_string = json.dumps(actionObject)
        return self.put("actions", str(id), data=data_json_string)
    def delete(self, id):
        """Delete a action.
        :return: The response from the API.
        """
        return self.remove("actions", str(id))


class Configuration(BaseAPI):
    def list(self):
        """List all configuration.

        :return: The response from the API.
        """

        return self.get("conf")
    
    def set(self, config):
        """Set configuration.

        :return: The response from the API.
        """
        data_json_string = json.dumps(config)
        return self.post("conf", data=data_json_string)

class Sensors(BaseAPI):
    def list(self):
        """List all sensors.

        :return: The response from the API.
        """

        return self.get("sensors")

class SynLinkPy(object):
  def __init__(self, host, credentials, timeout=DEFAULT_TIMEOUT):
      credentials.get("username")
      credentials.get("token")
      api_args = {
          'host': host,
          'timeout': timeout,
      }
      # if no token, then login and with user name and password and set cookie
      if (credentials.get("token") != None):
          # print("Token used")
          api_args["token"] = credentials["token"]

      elif (credentials.get("token") == None and credentials.get("username") != None and credentials.get("password") != None):
          # print("No token, username and password though")
          res = requests.post(host + "/login", data=json.dumps({ "username": credentials["username"], "password": credentials["password"] }))
          if res.status_code != 200:
              raise Error("Login failed")
          api_args["cookie"] = res.cookies["SPID"]

      else:
          raise Error("No token or username and password provided.")

      self.outlets = Outlets(**api_args)
      self.inlets = Inlets(**api_args)
      self.banks = Banks(**api_args)
      self.device = Device(**api_args)
      self.system = System(**api_args)
      self.groups = Groups(**api_args)
      self.conf = Configuration(**api_args)
      self.sensors = Sensors(**api_args)
      self.events = Events(**api_args)
      self.actions = Actions(**api_args)
    
