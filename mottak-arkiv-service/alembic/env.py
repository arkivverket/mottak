import os
import sys
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("dotenv loaded")
except ModuleNotFoundError:
    print("Failed to load dotenv file. Assuming production")


def get_url():
    try:
        return "%s://%s:%s@%s/%s" % (
            os.environ["DB_DRIVER"],
            os.environ["DB_USER"],
            os.environ["DB_PASSWORD"],
            os.environ["DB_HOST"],
            os.environ["DB_NAME"],
        )
    except KeyError as exception:
        logging.error(f"Environment variable not set {exception}")
        sys.exit(1)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# When creating a migration import all the classes and point target_metadata to Base:
# import os, sys
# sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
# from app.db.schemas.mottak import Arkivuttrekk, Invitasjon, Lokasjon, Metadatafil, Overforingspakke, Tester
# from app.db.baseclass import Base
# target_metadata = Base.metadata
# Default:
target_metadata = None


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url()
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
