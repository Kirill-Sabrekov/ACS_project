from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from ..db.session import get_db
from ..crud import nodes
from ..schemas import NodeData, NodeHistory

router = APIRouter()

@router.get("/tagnames", response_model=List[NodeData])
async def get_tagnames(db: AsyncSession = Depends(get_db)):
    try:
        tagnames = await nodes.get_all_tagnames(db)
        return tagnames
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data", response_model=List[NodeHistory])
async def get_sensor_data(
    nodeid: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: Optional[int] = 50,
    db: AsyncSession = Depends(get_db)
):
    try:
        if limit and (limit < 1 or limit > 50):
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 50")
            
        history = await nodes.get_nodes_history(db, nodeid, date_from, date_to)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 