from sqlalchemy import (
    create_engine, Column, Integer, Float, String, Boolean,
    ForeignKey, Text, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///physion.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ==========================
# USER MODEL
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    role = Column(String, default="user")

    simulations = relationship("SimulationResult", back_populates="user")


# ==========================
# SIMULATION RESULT MODEL
# ==========================
class SimulationResult(Base):
    __tablename__ = "simulation_results"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    steps = Column(Integer)
    avg_voltage = Column(Float)
    max_temperature = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="simulations")

    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    job = relationship("Job", back_populates="simulation", uselist=False)


# ==========================
# JOB MODEL
# ==========================
class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    simulation = relationship("SimulationResult", back_populates="job", uselist=False)
    results = relationship("JobResult", back_populates="job")


# ==========================
# JOB RESULT MODEL
# ==========================
class JobResult(Base):
    __tablename__ = "job_results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"), index=True)

    result = Column(Text)
    metrics = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="results")


def init_db():
    Base.metadata.create_all(bind=engine)
