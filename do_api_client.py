import json
import requests

class Do():
    '''
    Call the DigitalOcean API
    '''
    def __init__(self, base_url, token, verify_ssl = True):
        '''
        Initiate the Session object with all the parameters
        '''
        self.session = requests.Session()
        self.base_url = base_url
        self.headers = { 'Content-Type': 'application/json' }
        self.headers.update( { 'Authorization': 'Bearer ' + token })
        self.verify_ssl = verify_ssl

    def call(self, method, path, parameters = None):
        '''
        Call the given path with the given parameters
        '''
        url = self.base_url + path

        if method == 'POST':
            call = self.session.post(url, headers = self.headers,
                data = json.dumps(parameters), verify = self.verify_ssl)
        elif method == 'GET':
            call = self.session.get(url, headers = self.headers,
                verify = self.verify_ssl)
        elif method == 'DELETE':
            call = self.session.delete(url, headers = self.headers,
                verify = self.verify_ssl)
        else:
            # Raise a system exit on unspecified method
            raise SystemExit('HTTP method unspecified')

        if call.status_code == 200 or call.status_code == 201:
            # Return the response body on 200 or 201
            return call.json()
        elif call.status_code == 204:
            # Return nil on 204 for empty response body
            pass
        else:
            # Raise a system exit on error
            raise SystemExit(call.json())
