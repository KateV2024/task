from conftest import backend_url
from datetime import datetime


class Record():
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
        return self.get_record_id()

    def get_records(self, session, backend_url):
        self.response = session.get(backend_url)
        self.response_json = self.response.json()
        return self.response

    def get_record_id(self):
        record_id = self.response_json.get('_id')
        return record_id

    def delete_record(self, record_id, session, backend_url):
        url = f'{backend_url}/{record_id}'
        self.response = session.delete(url)
        self.response_json = self.response.json()

    def check_status_code(self, expected_status_code):
        assert self.response.status_code == expected_status_code, \
        f'Expected {expected_status_code}, got {self.response.status_code}'

