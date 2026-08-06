from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_yjtd1HvP9wQh@ep-silent-credit-a7v65vz6-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require"



engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

import models

Base.metadata.create_all(bind=engine)
