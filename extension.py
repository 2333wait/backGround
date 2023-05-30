from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_cors import CORS


pymysql.install_as_MySQLdb()
db = SQLAlchemy()
cors = CORS()
