from conftest import backend_url
from endpoints.base_endpoint import Endpoint
from datetime import datetime


class Record(Endpoint):
    def __init__(self):
        super().__init__()
        self.schema = {
            "title": str,
            "description": str,
            "createdAt": datetime
        }

    def create_record(self, payload, session, backend_url):
        if "createdAt" not in payload:
            payload["createdAt"] = datetime.now().isoformat()

        self.response = session.post(backend_url, json=payload)
        self.response_json = self.response.json()
        record_id = self.response_json.get('_id')
        return record_id

    def get_records(self, session, backend_url):
        self.response = session.get(backend_url)
        self.response_json = self.response.json()
        return self.response

    def get_record_id(self):
        record_id = self.response_json.get('_id')
        return record_id

    def delete_record(self, session, url, record_id):
        url = f'{url}/{record_id}'
        self.response = session.delete(url)
        self.response_json = self.response.json()
