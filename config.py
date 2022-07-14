import os


class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cannot-be-guess'

    SQLALCHEMY_DATABASE_URI = "postgresql://ozshdksajahhgd:fb294a7d17cd4625d476205043ba83969fcb9fe0938d83bf0a3577e791abdd5f@ec2-34-225-159-178.compute-1.amazonaws.com:5432/d3p0f4imfgeqmq"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
