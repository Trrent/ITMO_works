import sqlalchemy
from sqlalchemy import orm
from datetime import datetime as dt
from .db_session import SqlAlchemyBase


class Report(SqlAlchemyBase):
    __tablename__ = 'reports'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=dt.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tasks.id"), nullable=True)
    is_right_answer = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    def __repr__(self):
        return f"Report (user_id={self.user_id}, is_right_answer={self.is_right_answer}, date={self.datetime.date()})"
