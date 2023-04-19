import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task4(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_4'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task5(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_5'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task6(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_6'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task9(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_9'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task10(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_10'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task11(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_11'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task12(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_12'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task13(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_13'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task14(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_14'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task15(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_15'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task16(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_16'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)


class Task17(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_17'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text_of_the_task = sqlalchemy.Column(sqlalchemy.String)
    answers = sqlalchemy.Column(sqlalchemy.String)
    done_by = sqlalchemy.Column(sqlalchemy.String, default="")
    adding = sqlalchemy.Column(sqlalchemy.String)
