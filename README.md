# Employee Management System

The Employee Management System is a Python application that allows you to manage employees, jobs, and departments. The application uses a PostgreSQL database to store the data and provides a REST API to interact with the data.

## Installation

To install the Employee Management System, follow these steps:

1. Clone this repository to your local machine:


```bash
git clone https://github.com/example/employee-management-system.git
```

The Employee Management System provides the following API endpoints:

- `/employees` - allows you to create, read, update, and delete employees
- `/jobs` - allows you to create, read, update, and delete jobs
- `/departments` - allows you to create, read, update, and delete departments

Each endpoint supports the following methods:

- `GET` - retrieves a list of records or a single record
- `POST` - creates a new record
- `PUT` - updates an existing record
- `DELETE` - deletes an existing record


### Examples

To create a new employee, make a `POST` request to the `/employees` endpoint with the following payload:

```json
{
    "name": "John Doe",
    "job_id": 1,
    "department_id": 1
}
```

###  Backup and Restoration
The database is automatically backed up every 6 hours using a cron job running inside the container. The backups are stored in the backups directory in the root of the project, and are named with a timestamp indicating when the backup was taken.

To restore the database from a backup, you can use the /restore endpoint provided by the API. This endpoint accepts a POST request with a JSON payload containing the filename of the backup you want to restore. Here's an example of how to use the endpoint to restore a backup:

```bash
$ curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"filename": "2022-04-10-12-00-00.sql"}' \
    http://localhost:5000/restore
```