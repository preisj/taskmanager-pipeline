import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Task
from app.db import db
from dotenv import load_dotenv

load_dotenv()

# this is the Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set SQLAlchemy URL from environment
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = db.metadata

def run_migrations_offline():
    context.configure(
        url=os.getenv("DATABASE_URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
