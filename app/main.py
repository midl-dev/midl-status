from flask import Flask
from flask_migrate import Migrate

from app.dash import status
from app.models import db
from app.scheduler import scheduler

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config.Config")

with app.app_context():
    db.init_app(app)
    migrate = Migrate(app, db)
    scheduler.init_app(app)
    status.init_dash(app)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=8080)
