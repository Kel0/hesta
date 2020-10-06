from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import base


class Groups(base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(length=10), unique=True, index=True)

    # relationship
    students = relationship("Students", back_populates="group")


class Students(base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    name = Column(String(length=225))
    github_link = Column(String(length=500), default="no_link")

    # relationship
    group = relationship("Groups", back_populates="students")
