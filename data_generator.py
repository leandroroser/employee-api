from typing import List
import csv
from faker import Faker


def generate_employee_csv(file_path: str) -> None:
    fake = Faker()
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'name', 'hire_date', 'job_id', 'department_id'])
        for i in range(1000):
            writer.writerow([i+1, fake.name(), fake.iso8601(tzinfo='UTC'), fake.random_int(min=1, max=3),
                             fake.random_int(min=1, max=3)])


def generate_job_csv(file_path: str) -> None:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'name'])
        writer.writerow([1, 'Recruiter'])
        writer.writerow([2, 'Manager'])
        writer.writerow([3, 'Analyst'])
        

def generate_department_csv(file_path: str) -> None:
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['id', 'name'])
        writer.writerow([1, 'Supply Chain'])
        writer.writerow([2, 'Maintenance'])
        writer.writerow([3, 'Staff'])