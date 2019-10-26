from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import parser

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)



from app import routes, models

#db.drop_all()
#db.create_all()
#db.session.commit()

if __name__ == '__main__':
    print(__name__)
    parser.parseData(db,'cc_sample.csv',True)