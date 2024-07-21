from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select, text, delete

from ..dependencies import get_session, validate_user

from ..entities.db_model import Employe, EmployeCreateIn, EmployeCreateOut, EmployeOut,EmployeUpdateIn
from pydantic import ValidationError

router = APIRouter(prefix="/employes")
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeCreateOut)
async def create( *, session: Session = Depends(get_session), user=Depends(validate_user), employee: EmployeCreateIn):
            
    employee_db = Employe(**employee.model_dump())
    employee_db.id = uuid4()
    session.add(employee_db)
    session.commit()
    session.refresh(employee_db)
    return employee_db

@router.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping(*, session: Session = Depends(get_session)):
    session.exec(text("SELECT 1"))
    return "PONG"


@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset(*, session: Session = Depends(get_session)):
    session.exec(delete(Employe))
    session.commit()
    return {"msg": "Todos los datos fueron eliminados"}


@router.get("/{id}", response_model=EmployeOut)
async def get_employee(
    id: str, session: Session = Depends(get_session), user=Depends(validate_user)
):
    is_valid_uuid4(id)
    employ = session.exec(select(Employe).filter_by(id=id)).first()

    if not employ :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El empleado con ese ID no existe.",
        )
    return employ


@router.patch("/{id}")
async def update(
    *, session: Session = Depends(get_session), id: UUID, employe: EmployeUpdateIn
):
    db_employe = session.get(Employe, id)
    if not db_employe:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    hero_data = employe.model_dump(exclude_unset=True)
    if len(hero_data) == 0:
        raise HTTPException(
            status_code=400, detail="Debe enviar la modificación de al menos un campo"
        )
    for key, value in hero_data.items():
        setattr(db_employe, key, value)
    session.add(db_employe)
    session.commit()
    session.refresh(db_employe)
    return {"msg": "el empleado ha sido actualizado"}


def is_valid_uuid4(id):
    try:
        UUID(id, version=4)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El id no es un valor string con formato uuid.",
        )
