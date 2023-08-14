import logging
import os

from alembic import command, util
from alembic.config import Config
from auth_service.config import DB_DSN, LOGGING_FORMAT

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
log = logging.getLogger(__name__)


def run_migrations() -> None:
    current_path = os.path.dirname(os.path.realpath(__file__))
    migrations_path = f"{current_path}/migrations"
    versions_path = f"{migrations_path}/versions"

    if os.path.exists(path=versions_path) is False:
        os.makedirs(name=versions_path)

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", migrations_path)
    alembic_cfg.set_main_option("sqlalchemy.url", DB_DSN)

    try:
        command.revision(alembic_cfg, autogenerate=True)
        command.upgrade(alembic_cfg, "head")
    except util.CommandError as e:
        log.error(e)
    except Exception as e:
        log.error(e)
