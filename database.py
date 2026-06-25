from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# SQLite database file
DATABASE_URL = "sqlite:///physion.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()


# ==========================
# USER MODEL (با نقش‌ها)
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # NEW: نقش‌ها
    role = Column(String, default="user")   # user یا admin

    # NEW: ارتباط با SimulationResult
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

    # NEW: اتصال به کاربر
    user_id = Column(Integer, ForeignKey("users.id"))

    # NEW: ارتباط ORM
    user = relationship("User", back_populates="simulations")


# ==========================
# INIT DB
# ==========================
def init_db():
    Base.metadata.create_all(bind=engine)
