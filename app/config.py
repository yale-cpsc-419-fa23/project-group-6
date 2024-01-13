import os

basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     RDS_USERNAME = os.getenv('RDS_USERNAME', 'default_username')
#     RDS_PASSWORD = os.getenv('RDS_PASSWORD', 'default_password')
#     RDS_HOST= os.getenv('RDS_HOST', 'localhost')
#     RDS_PORT = os.getenv('RDS_PORT', '3306')
#     RDS_DB_NAME = os.getenv('RDS_DB_NAME')

#     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB_NAME}'

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'music_data.sqlite')

class DevelopmentConfig(Config):
    DEBUG = True
