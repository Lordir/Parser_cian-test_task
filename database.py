from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

engine = create_engine("postgresql://postgres:1z3q2w@localhost/cian")
Base = declarative_base()


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    year_house = Column(Integer)
    floors_count = Column(Integer)
    house_material_type = Column(String)
    object = relationship("Object")


class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    total_area = Column(DECIMAL(5, 2), nullable=False)
    floor_num = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
    offer_id = Column(Integer, nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id"))


Base.metadata.create_all(engine)
