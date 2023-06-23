
SECRET_KEY = "njksdhiodgnlkuhsao"
# CONNECT DATABASE
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "mwboa"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "460255750@qq.com"
MAIL_PASSWORD = "yrszmbwqbirbbjbe"
MAIL_DEFAULT_SENDER = "460255750@qq.com"