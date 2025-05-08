from sqlalchemy import select, desc, func, distinct
from db.models import SensorData, Node
from typing import List, Optional
from datetime import datetime

async def get_nodes_history(session, nodeid: Optional[int] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[dict]:
    try:
        if not nodeid:
            # Получаем список узлов с историей
            history_nodes_query = select(distinct(SensorData.nodeid))
            if date_from:
                history_nodes_query = history_nodes_query.where(SensorData.time >= date_from)
            if date_to:
                history_nodes_query = history_nodes_query.where(SensorData.time <= date_to)
            
            history_node_ids = (await session.execute(history_nodes_query)).scalars().all()
            if not history_node_ids:
                return []
            
            # Получаем информацию о узлах
            nodes = (await session.execute(
                select(Node).where(Node.nodeid.in_(history_node_ids))
            )).scalars().all()
            
            result = []
            for node in nodes:
                # Получаем историю для узла
                subquery = (
                    select(SensorData)
                    .where(SensorData.nodeid == node.nodeid)
                    .order_by(desc(SensorData.time))
                    .limit(50)
                )
                
                if date_from:
                    subquery = subquery.where(SensorData.time >= date_from)
                if date_to:
                    subquery = subquery.where(SensorData.time <= date_to)
                
                history = (await session.execute(subquery)).scalars().all()
                
                if history:
                    result.append({
                        "nodeid": node.nodeid,
                        "tagname": node.tagname,
                        "history": [{
                            "time": item.time.isoformat(),
                            "actualtime": item.actualtime.isoformat() if item.actualtime else None,
                            "valdouble": item.valdouble,
                            "valint": item.valint,
                            "valuint": item.valuint,
                            "valbool": item.valbool,
                            "valstring": item.valstring,
                            "quality": item.quality,
                            "recordtype": item.recordtype,
                            "appid": str(item.appid) if item.appid else None
                        } for item in history]
                    })
            
            return result
            
        # Если указан nodeid
        node = (await session.execute(
            select(Node).where(Node.nodeid == nodeid)
        )).scalar_one_or_none()
        
        if not node:
            return []
            
        # Получаем историю для узла
        query = select(SensorData).where(SensorData.nodeid == nodeid)
        
        if date_from:
            query = query.where(SensorData.time >= date_from)
        if date_to:
            query = query.where(SensorData.time <= date_to)
            
        query = query.order_by(desc(SensorData.time)).limit(50)
        history = (await session.execute(query)).scalars().all()
        
        if not history:
            return []
            
        return [{
            "nodeid": node.nodeid,
            "tagname": node.tagname,
            "history": [{
                "time": item.time.isoformat(),
                "actualtime": item.actualtime.isoformat() if item.actualtime else None,
                "valdouble": item.valdouble,
                "valint": item.valint,
                "valuint": item.valuint,
                "valbool": item.valbool,
                "valstring": item.valstring,
                "quality": item.quality,
                "recordtype": item.recordtype,
                "appid": str(item.appid) if item.appid else None
            } for item in history]
        }]
        
    except Exception:
        return []

async def get_all_tagnames(session) -> List[dict]:
    try:
        # Получаем список узлов с историей
        history_node_ids = (await session.execute(
            select(distinct(SensorData.nodeid))
        )).scalars().all()
        
        if not history_node_ids:
            return []
        
        # Получаем информацию о узлах
        nodes = (await session.execute(
            select(Node).where(Node.nodeid.in_(history_node_ids))
        )).scalars().all()
        
        return [{"nodeid": node.nodeid, "tagname": node.tagname} for node in nodes]
    except Exception:
        return [] 