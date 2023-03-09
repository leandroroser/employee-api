from api.src.models.employee import EmployeeModel
from fastapi import APIRouter



router = APIRouter(prefix="/employee", tags=["employee"])


@router.get("employee")
async def employee():
    pass


@router.post("employee")
async def employee_post():
    pass

