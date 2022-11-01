import json
import requests
# import time

__version__ = "0.1.0"

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
            raise Error(response.reason)

        return response.json()

    def post(self, resource, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        if self.cookie:
            kwargs.setdefault('headers', {})['Cookie'] = 'SPID=' + self.cookie

        url = self.host + "/api/" + resource
        response = requests.post(url, **kwargs)
        if not response.status_code == 200:
            raise Error(response.reason)
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
        print(data_json_string)
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
          print("Token used")
          api_args["token"] = credentials["token"]

      elif (credentials.get("token") == None and credentials.get("username") != None and credentials.get("password") != None):
          print("No token, username and password though")
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
      self.groups = Groups(**api_args)
      self.conf = Configuration(**api_args)
      self.sensors = Sensors(**api_args)
