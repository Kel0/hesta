import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from .database.db import session
from .database.models import Groups

logger = logging.getLogger(__name__)


async def create_group(group_name: str) -> bool:
    sqlalchemy_session: Session = session()

    try:
        sqlalchemy_session.add(Groups(group=group_name))
        sqlalchemy_session.commit()
        return True
    except Exception as e_info:
        logger.error(e_info)
        return False


async def get_groups() -> Optional[List[Groups]]:
    sqlalchemy_session: Session = session()

    try:
        groups: List[Groups] = sqlalchemy_session.query(Groups).all()
        return groups
    except Exception as e_info:
        logger.error(e_info)
        return None
