import logging
from typing import List, Optional, Union

import aiogram.utils.markdown as md
from sqlalchemy.orm import Session

from .database.db import session
from .database.models import Groups, Students

logger = logging.getLogger(__name__)


async def create_group(group_name: str) -> bool:
    sqlalchemy_session: Session = session()

    try:
        sqlalchemy_session.add(Groups(group=group_name.upper()))
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


async def get_students(group: str) -> Optional[List[Students]]:
    sqlalchemy_session: Session = session()

    try:
        groups: List[Groups] = (
            sqlalchemy_session.query(Groups).filter(Groups.group == group.upper()).all()
        )

        return groups[0].students
    except Exception as e_info:
        logger.error(e_info)
        return None


def formalize_students_text(students: List[Students]) -> str:
    reply_text = [md.text(f"Students count: {len(students)}")]
    for index, student in enumerate(students):
        reply_text.append(
            md.text(f"{index + 1}. {student.name} | Github link: {student.github_link}")
        )

    return md.text(*reply_text, sep="\n")


async def create_students(students) -> Union[str, bool]:
    sqlalchemy_session: Session = session()

    for student in students:
        try:
            group: List[Groups] = (
                sqlalchemy_session.query(Groups)
                .filter(Groups.group == student["group"])
                .all()
            )

            if len(group) == 0:
                return "No group"

            sqlalchemy_session.add(
                Students(
                    group_id=group[0].id,
                    name=student["name"],
                    github_link=student["link"],
                )
            )
            sqlalchemy_session.commit()
        except Exception as e_info:
            logger.error(e_info)
            return False
    return True
