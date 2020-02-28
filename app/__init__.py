from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import parser
import babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        #format="EE dd.MM.y HH:mm"
        format = "MM/dd/y"

    if value:
        return babel.dates.format_datetime(value, format)
    else:
        return ''

app.jinja_env.filters['datetime'] = format_datetime



from app import routes, models

#db.drop_all()
#db.create_all()
#db.session.commit()

if __name__ == '__main__':
    print(__name__)
    parser.parseData(db,'cc_sample.csv',True)