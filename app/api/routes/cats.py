from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.cat import SpyCat
from app.schemas.cat import CatCreate, CatOut, CatUpdateSalary
from app.services.breed_validation import BreedValidator
from app.core.config import settings

router = APIRouter(prefix="/cats", tags=["cats"])
breed_validator = BreedValidator(api_key=settings.THECATAPI_KEY)

@router.post("", response_model=CatOut, status_code=status.HTTP_201_CREATED)
async def create_cat(payload: CatCreate, db: Session = Depends(get_db)):
    if not await breed_validator.is_valid_breed(payload.breed):
        raise HTTPException(status_code=422, detail="Invalid breed (TheCatAPI)")

    cat = SpyCat(
        name=payload.name,
        years_of_experience=payload.years_of_experience,
        breed=payload.breed,
        salary=float(payload.salary),
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("", response_model=list[CatOut])
def list_cats(db: Session = Depends(get_db)):
    return db.query(SpyCat).order_by(SpyCat.id.desc()).all()

@router.get("/{cat_id}", response_model=CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Cat not found")
    return cat

@router.patch("/{cat_id}/salary", response_model=CatOut)
def update_salary(cat_id: int, payload: CatUpdateSalary, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Cat not found")
    cat.salary = float(payload.salary)
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "Cat not found")
    # опционально: запрещать удалять если есть назначенная миссия
    if cat.mission and not cat.mission.is_completed:
        raise HTTPException(409, "Cat has an active mission")
    db.delete(cat)
    db.commit()
