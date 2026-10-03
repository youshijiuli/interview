SECRET_KEY = 'WANGXIN'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    'root',
    '',
    'localhost',
    '3306',
    'test'
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
