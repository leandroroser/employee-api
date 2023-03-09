from minio import Minio
from minio.error import ResponseError
from datetime import datetime
from datetime import date
from typing import List
from fastavro import writer
from io import BytesIO
from api.src.connector import Connector
from api.src.models import Employee,Department,Job

def backup_to_avro(connector: Connector, bucket_name: str):
    table_name = connector.model.__tablename__
    backup_filename = f"{table_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.avro"

    data = connector.read_all()
    schema = connector.model.avro_schema()
    buffer = BytesIO()
    writer(buffer, schema, data)
    buffer.seek(0)

    client = Minio("minio:9000", access_key="access_key", secret_key="secret_key", secure=False)
    try:
        client.put_object(bucket_name, backup_filename, buffer, length=buffer.getbuffer().nbytes)
        print(f"Backup of table {table_name} uploaded to MinIO: { bucket_name}")
    except ResponseError as err:
        print(f"Error uploading backup of table {table_name} to MinIO: {err}")
    print("Backup process completed.")


if __name__ == "__main__":
    connector = Connector(Employee)
    backup_to_avro(connector, "backup")

    connector = Connector(Job)
    backup_to_avro(connector, "backup")
    
    connector = Connector(Department)
    backup_to_avro(connector, "backup")
    
    