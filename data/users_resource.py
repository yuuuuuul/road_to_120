from flask import jsonify, request
from flask_restful import Resource, abort

from .users_parser import parser
from . import db_session
from .users import User


def abort_if_users_not_found(user_id):
    sess = db_session.create_session()
    work = sess.query(User).get(user_id)
    sess.close()
    if not work:
        abort(404, message=f"User {user_id} not found")


def abort_if_mail_retry(user_mail):
    sess = db_session.create_session()
    email = sess.query(User).filter(User.email == user_mail).first()
    sess.close()
    if email:
        abort(404, message=f"User with this email ({user_mail}) exists")


def abort_if_nickname_retry(user_nickname):
    sess = db_session.create_session()
    nickname = sess.query(User).filter(User.nickname == user_nickname).first()
    sess.close()
    if nickname:
        abort(404, message=f"User with this nickname ({user_nickname}) exists")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.close()
        return jsonify({
            "user": user.to_dict(only=("id", "nickname", "task_completed", "email", "picture"))
        })

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        sess.close()
        return jsonify({"success": "OK"})


class UsersListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        users = sess.query(User).all()
        sess.close()
        return jsonify({
            "users": [item.to_dict(only=("id", "nickname", "task_completed", "email", "picture")) for item in users]
        })

    def post(self):
        args = parser.parse_args()
        abort_if_mail_retry(args["email"])
        abort_if_nickname_retry(args["nickname"])
        sess = db_session.create_session()
        user = User(
            nickname=args["nickname"],
            email=args["email"],
        )
        user.set_password(args["password"])
        sess.add(user)
        sess.commit()
        sess.close()
        return jsonify({"success": "OK"})
