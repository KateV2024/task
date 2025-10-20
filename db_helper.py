from bson import ObjectId
from pymongo.database import Database


class DatabaseHelper:

    def __init__(self, db_connection: Database, collection_name, backend_url):
        self.db = db_connection
        self.collection_name = collection_name
        self.collection = self.db[collection_name]
        self.backend_url = backend_url

    def find_record_by_id(self, record_id):
        if isinstance(record_id, str):
            try:
                record_id = ObjectId(record_id)
            except Exception as e:
                raise ValueError(f"Invalid record ID format: {record_id}, Error: {e}")

        return self.collection.find_one({"_id": record_id})

    def verify_record_exists(self, record_id):
        db_record = self.find_record_by_id(record_id)
        return db_record

    def delete_record(self, record_id):
        if isinstance(record_id, str):
            try:
                record_id = ObjectId(record_id)
            except Exception:
                return False
        result = self.collection.delete_one({"_id": record_id})
        return result.deleted_count > 0
