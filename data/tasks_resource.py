from flask import jsonify, request
from flask_restful import Resource, abort

from .tasks_parser import parser
from . import db_session
from .tasks import *

CLASS_DICT = {4: Task4, 5: Task5, 6: Task6, 9: Task9, 10: Task10, 11: Task11, 12: Task12,  13: Task13, 14: Task14, 15: Task15, 16: Task16, 17: Task17}


def abort_if_tasks_not_found(category_id, task_id):
    sess = db_session.create_session()
    work = sess.query(CLASS_DICT[category_id]).get(task_id)
    sess.close()
    if not work:
        abort(404, message=f"Task {category_id}.{task_id} not found")


class TasksResource(Resource):
    def get(self, category_id, task_id):
        abort_if_tasks_not_found(category_id, task_id)
        sess = db_session.create_session()
        task = sess.query(CLASS_DICT[category_id]).get(task_id)
        sess.close()
        return jsonify({
            "tasks": task.to_dict(only=("id", "text_of_the_task",
                                        "answers", "done_by", "adding"))
        })

    def delete(self, category_id, task_id):
        abort_if_tasks_not_found(category_id, task_id)
        sess = db_session.create_session()
        task = sess.query(CLASS_DICT[category_id]).get(task_id)
        sess.delete(task)
        sess.commit()
        sess.close()
        return jsonify({"success": "OK"})


class TasksListResource(Resource):
    def get(self, category_id):
        sess = db_session.create_session()
        tasks = sess.query(CLASS_DICT[category_id]).all()
        sess.close()
        return jsonify({
            "tasks": [item.to_dict(only=("id", "text_of_the_task",
                                         "answers", "done_by", "adding")) for item in tasks]
        })

    def post(self, category_id):
        args = parser.parse_args()
        sess = db_session.create_session()
        task = CLASS_DICT[category_id](
            text_of_the_task=args["text_of_the_task"],
            answers=args["answers"],
            adding=args["adding"]
        )
        sess.add(task)
        sess.commit()
        sess.close()
        return jsonify({"success": "OK"})
