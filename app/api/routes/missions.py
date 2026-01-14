from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.mission import Mission, Target
from app.models.cat import SpyCat
from app.schemas.mission import (
    MissionCreate,
    MissionAssign,
    MissionOut,
    TargetUpdateNotes,
)

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("", response_model=MissionOut, status_code=201)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    mission = Mission()
    for t in payload.targets:
        mission.targets.append(
            Target(name=t.name, country=t.country, notes=t.notes)
        )

    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.get("", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")
    return mission


@router.delete("/{mission_id}", status_code=204)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")
    if mission.cat_id is not None:
        raise HTTPException(409, "Mission already assigned to a cat")

    db.delete(mission)
    db.commit()


@router.post("/{mission_id}/assign", response_model=MissionOut)
def assign_cat(
    mission_id: int,
    payload: MissionAssign,
    db: Session = Depends(get_db),
):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")

    cat = db.get(SpyCat, payload.cat_id)
    if not cat:
        raise HTTPException(404, "Cat not found")

    active = (
        db.query(Mission)
        .filter(Mission.cat_id == payload.cat_id, Mission.is_completed == False)
        .first()
    )
    if active:
        raise HTTPException(409, "Cat already has an active mission")

    mission.cat_id = payload.cat_id
    db.commit()
    db.refresh(mission)
    return mission


@router.patch("/{mission_id}/targets/{target_id}/notes", response_model=MissionOut)
def update_notes(
    mission_id: int,
    target_id: int,
    payload: TargetUpdateNotes,
    db: Session = Depends(get_db),
):
    target = db.get(Target, target_id)
    if not target or target.mission_id != mission_id:
        raise HTTPException(404, "Target not found")

    if target.is_completed or target.mission.is_completed:
        raise HTTPException(409, "Notes are frozen")

    target.notes = payload.notes
    db.commit()
    return target.mission


@router.patch("/{mission_id}/targets/{target_id}/complete", response_model=MissionOut)
def complete_target(
    mission_id: int,
    target_id: int,
    db: Session = Depends(get_db),
):
    target = db.get(Target, target_id)
    if not target or target.mission_id != mission_id:
        raise HTTPException(404, "Target not found")

    target.is_completed = True

    mission = target.mission
    if all(t.is_completed for t in mission.targets):
        mission.is_completed = True

    db.commit()
    return mission
