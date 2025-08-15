import http.client
import json

class CustomHTTPClient:
    _instance = None
    
    def __new__(cls, host):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = http.client.HTTPSConnection(host)
        return cls._instance

    def post_request_html(self, endpoint, payload, headers):
        payload = json.dumps(payload)
        self.conn.request("POST", endpoint, payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    
    def post_request_json(self, endpoint, payload, headers):
        payload = json.dumps(payload)
        self.conn.request("POST", endpoint, payload, headers)
        res = self.conn.getresponse()
        return res
