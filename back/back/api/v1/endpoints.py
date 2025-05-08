from fastapi import APIRouter, Depends, Query
from db.database import AsyncSessionLocal
from crud.nodes import get_nodes_history, get_all_tagnames
from schemas.nodes import NodeSchema, NodeShortSchema
from typing import List, Optional
from datetime import datetime

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/data", response_model=List[NodeSchema])
async def read_data(
    db=Depends(get_db),
    nodeid: Optional[int] = Query(None, description="ID узла (node)"),
    date_from: Optional[datetime] = Query(None, description="Дата и время начала периода (ISO 8601)"),
    date_to: Optional[datetime] = Query(None, description="Дата и время конца периода (ISO 8601)")
):
    return await get_nodes_history(db, nodeid, date_from, date_to)

@router.get("/tagnames", response_model=List[NodeShortSchema])
async def get_tagnames(db=Depends(get_db)):
    return await get_all_tagnames(db)
