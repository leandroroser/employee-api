# Employee Management System

The Employee Management System is a Python application that allows you to manage employees, jobs, and departments. The application uses a PostgreSQL database to store the data and provides a REST API to interact with the data.

## Installation

To install the Employee Management System, follow these steps:

1. Clone this repository to your local machine:


```bash
git clone https://github.com/example/employee-management-system.git
```
### Usage

1. Generate data:

```bash
cd employee-api
pip install pyenv
pyenv install 3.10.6
pyenv virtualenv 3.10.6 testapi 
pyenv local testapi
pip install -r requirements.txt
python -m data_generator
```

2. Run the api:

```bash
make start
```

3. Navigate to http://localhost:8000/docs to access the Swagger UI and interact with the API endpoints.

4. To interact with the MinIO object storage service used in this project, you can access the MinIO UI by visiting http://localhost:9001 in your web browser. User/Pass: minio/minio1234. The MinIO UI provides a web-based user interface that allows you to browse, upload, and manage files stored in your MinIO instance.

### API Endpoints

`GET /status`: Returns the status of the API.

`GET /{table}`: Retrieves all records from a specified table. Supported tables are employees, departments, and jobs.

`POST /{table}`: Creates a batch of new records in the specified table. The request body must contain a list of dictionaries, where each dictionary represents a record.

`GET /restore_data/{table}/{date}`: Restores data from MinIO for the specified table and date. Valid table names are employees, departments, and jobs. The date should be in YYYY-MM-DD format.

`GET /counts_quarter`: Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

`GET /higher_than_average`: List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

### Technologies Used

- **FastAPI**: a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **uvicorn**: a lightning-fast ASGI server implementation, using uvloop and httptools.
- **docker-compose**: a tool for defining and running multi-container Docker applications.
- **PostgreSQL**: a powerful, open-source relational database system.
- **MinIO**: a high-performance, distributed object storage system.


### Examples

To create a new employee, make a `POST` request to the `/employees` endpoint with the following payload:

```bash
$ curl -X 'POST' \
  'http://0.0.0.0:8000/employees' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    {
    "id":1001,
    "name": "John Doe",
    "datetime": "1980-10-16T04:36:04+00:00",
    "job_id": 1,
    "department_id": 3
    }
]'
```

###  Backup and Restoration

The database is automatically backed up every 1 minute (for testing, so don't leave it running too long!) using a cron job running inside the container. The backups are stored in the backups directory in the root of the project, and are named with a timestamp indicating when the backup was taken.

To restore the database from a backup, you can use the /restore endpoint provided by the API. This endpoint accepts a POST request with a JSON payload containing the filename of the backup you want to restore. Here's an example of how to use the endpoint to restore a backup:

```bash
$ curl -X GET http://localhost:8000/restore_data/employees/2023-03-10_10-03
```