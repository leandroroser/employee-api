import csv
from faker import Faker
import pytz

DATA_PATH="./api-data"

def generate_employee_csv(file_path: str) -> None:
    fake = Faker()
    utc = pytz.UTC
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'name', 'datetime', 'job_id', 'department_id'])
        for i in range(1000):
            writer.writerow([i+1, fake.name(), fake.iso8601(tzinfo=utc), fake.random_int(min=1, max=3),
                             fake.random_int(min=1, max=3)])

def generate_job_csv(file_path: str) -> None:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'job'])
        writer.writerow([1, 'Recruiter'])
        writer.writerow([2, 'Manager'])
        writer.writerow([3, 'Analyst'])
        
def generate_department_csv(file_path: str) -> None:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'department'])
        writer.writerow([1, 'Supply Chain'])
        writer.writerow([2, 'Maintenance'])
        writer.writerow([3, 'Staff'])


if __name__ == "__main__":
    print(f"Generating data...")
    generate_employee_csv(f"{DATA_PATH}/Employees.csv")
    generate_job_csv(f"{DATA_PATH}/Jobs.csv")
    generate_department_csv(f"{DATA_PATH}/Departments.csv")