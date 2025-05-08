from sqlalchemy import Column, BigInteger, Float, DateTime, Boolean, Text, PrimaryKeyConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "nodes_history"
    nodeid = Column(BigInteger, index=True)
    actualtime = Column(DateTime)
    time = Column(DateTime)
    valint = Column(BigInteger)
    valuint = Column(BigInteger)
    valdouble = Column(Float)
    valbool = Column(Boolean)
    valstring = Column(Text)
    quality = Column(BigInteger)
    recordtype = Column(Text)
    appid = Column(UUID(as_uuid=True))

    __table_args__ = (
        PrimaryKeyConstraint('nodeid', 'time'),
        Index('idx_nodes_history_nodeid_time', 'nodeid', 'time'),
        Index('idx_nodes_history_time', 'time')
    )

class Node(Base):
    __tablename__ = "nodes"
    nodeid = Column(BigInteger, primary_key=True, index=True)
    tagname = Column(Text)
    description = Column(Text)
    unit = Column(Text)
    appid = Column(UUID(as_uuid=True)) 