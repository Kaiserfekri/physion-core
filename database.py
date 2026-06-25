from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///physion.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()


class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    steps = Column(Integer)
    avg_voltage = Column(Float)
    max_temperature = Column(Float)


def init_db():
    Base.metadata.create_all(bind=engine)
