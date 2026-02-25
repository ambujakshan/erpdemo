from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ✅ Change this to your real Postgres settings
DATABASE_URL = "postgresql+psycopg2://erp:erp123@localhost:5432/erp_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()