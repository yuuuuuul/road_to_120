import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task10(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_10'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task12(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_12'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task13(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_13'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task15(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_15'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task16(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_16'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task19(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_19'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adding = sqlalchemy.Column(sqlalchemy.String)
