from sqlalchemy import Column, Integer, String

from .db import base


class Groups(base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(length=10))
