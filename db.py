from flask_sqlalchemy import SQLAlchemy

# DATABASE CONFIG
DATABASE_PATH = "postgres://hpxvduqlxldsep:4869d5663e8caee811fdb93136886477b3182a1b072ee384ac4b324ae06655b5@ec2-35-169-254-43.compute-1.amazonaws.com:5432/d1c5i2uf74qjq4"

db = SQLAlchemy()


# Setup db by providing the app and database path
def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Drop all the tables and create them again
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
