from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument("text_of_the_task", required=True, type=str)
parser.add_argument("answers", required=True, type=str)
parser.add_argument("adding", required=True, type=str)
