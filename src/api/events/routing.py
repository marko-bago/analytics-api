from fastapi import APIRouter, Depends
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)
from settings import settings
from sqlmodel import Session, select

router = APIRouter()

""" @router.get("/", response_model=EventListSchema)
def read_events(
    session : Session = Depends(get_session)):

    query = select(EventModel).order_by(EventModel.id).limit(2)
    results = session.exec(query).all()
    return {"results":results, "count": len(results)}

@router.post("/", response_model=EventModel)
def create_event(
    payload:EventCreateSchema, 
    session : Session = Depends(get_connection)):

    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{event_id}")
def read_event(event_id : int) -> EventModel:
    return {
        "id":event_id
    } 

@router.put("/{event_id}")
def update_event(event_id : int, payload:EventUpdateSchema) -> EventModel:

    data = payload.model_dump()
    return {"id":event_id, **data}  """