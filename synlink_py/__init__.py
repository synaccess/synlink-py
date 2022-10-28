import json
import requests
# import time

__version__ = "0.1.0"

DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 0

__all__ = ['Error', 'Response', 'BaseAPI', 'Outlets', 'SynLinkPy']

class Error(Exception):
    pass

class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')

    def __str__(self):
        return json.dumps(self.body)



class BaseAPI(object):
    def __init__(self, token=None, host=None, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES):
        self.token = token
        self.host = host
        self.timeout = timeout
        self.retries = retries

    # def _request(self, request_method, resource, resource_id, **kwargs):
    #     if self.token:
    #         kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token
    #     if resource_id:
    #         url = self.host + "/api/" + resource + '/' + resource_id
    #     else:
    #         url = self.host + "/api/" + resource
        
    #     response = request_method(url, timeout=self.timeout, **kwargs)

    #     if not response.status_code == 200:
    #         raise Error(response.reason)

    #     return response.json()

    def get(self, resource, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        url = self.host + "/api/" + resource
        response = requests.get(url, timeout=self.timeout, **kwargs)
        
        if not response.status_code == 200:
            raise Error(response.reason)

        return response.json()

    # def post(self, resource, **kwargs):
    #     return self._request(
    #       # self._session_post if self.session else requests.post,
    #       requests.post,
    #       resource,
    #       **kwargs
    #     )

    def put(self, resource, resource_id, **kwargs):
        if self.token:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        url = self.host + "/api/" + resource + '/' + resource_id
        response = requests.put(url, **kwargs)

        if not response.status_code == 200:
            raise Error(response.reason)

        return response.json()


class Outlets(BaseAPI):
    def set_state(self, outlet, state):
        """Set the state of an outlet.

        :param outlet: The outlet number or outlet ID to set.
        :param state: The state to set the outlet to. Can be "ON" or "OFF", or "REBOOT".
        :return: The response from the API.
        """
        # TODO check if state is correct
        
        data_json_string = json.dumps({"state": state})
        return self.put("outlets", str(outlet), data=data_json_string)
    
    def list(self):
        """List all outlets.

        :return: The response from the API.
        """

        return self.get("outlets")


class SynLinkPy(object):
  def __init__(self, host, token, timeout=DEFAULT_TIMEOUT):

      api_args = {
          'host': host,
          'token': token,
          'timeout': timeout,
      }
      self.outlets = Outlets(**api_args)
      # self.inlets = Inlets(**api_args)
